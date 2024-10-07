<!--
.. title: Magic Address Book
.. slug: magic-address-book
.. date: 2024-10-06 23:27:44 UTC-07:00
.. tags: howto
.. category: 
.. link: 
.. description: 
.. type: text
-->

I have young children, and keeping track of their friends' contact information is hard for me. Every year I get a list from each kid's teacher of their classmates and the classmates' parents' names and contact information, but translating that into contacts on my phone so I can text another parent to organize a playdate is a gigantic hassle. What I really wanted was something magical, a spreadsheet where I could copy those class rosters and have the contacts just appear on my phone. I looked around a lot, and nothing of the sort exists.

So I built one.
<!-- TEASER_END -->

[TOC]

## tl;dr

This post details how to set up a system where you can enter folks' contact information in a spreadsheet, and have that information automatically appear as contacts on your phone. Once it's set up, creating a new contact or modifying an existing contact is as simple as editing a field in the spreadsheet with no additional effort required.

## Main Components

This system has three main components:

1. A Google Sheet spreadsheet that collects folks' contact information you enter
2. A backend service that translates that spreadsheet into CardDAV data
3. A mechanism to sync that data to your phone's contact list automatically

These components are not super trivial to set up, but the whole thing does work, and if there's any interest I can put some time into building some glue to make this easier to get started with.

### Contact Information Spreadsheet

The first component is a Google Sheets spreadsheet. The sheet needs the following fields, but they can be in any order:

* **Name**: contact's full name
* **Email**: contact's email address
* **Phone**: contact's phone number
* **Address**: contact's street address
* **Kids**: contact's childrens' names (such as "Zoe MacPherson, Wren MacPherson")
* **Contact**: this field controls whether a contact is synced to the address book; use `1` for the primary contact for a family and to enable address book synchronization, `2` for the secondary contact, and leave it blank to keep this contact from being synced

Example:

| Name | Email | Phone | Address | Kids | Contact |
|------|-------|-------|---------|------|---------|
| Darryl MacPherson | dmac@example.com | 555-1234 | 405 Example Ave. | Zoe MacPherson, Hammie MacPherson, Wren MacPherson | 1 |
| Wanda MacPherson | wanda@me.com | 555-6789 | 405 Example Ave. | Zoe MacPherson, Hammie MacPherson, Wren MacPherson | |

You will also need to set up Google Sheets for API access. That's out of scope for this post, but [the gspread docs](https://docs.gspread.org/en/latest/oauth2.html#) explain it fairly well.

#### Bonus: Kids' Contact Information

There's a bonus additional sheet you can set up if you're so inclined. The main sheet tracks parents' contact information, but there isn't a great way to store reference information about their kids. It's possible to set up an additional sheet that uses Google Sheets formulas to create a useful reference for the kids too.

First, set up some [named ranges](https://support.google.com/docs/answer/63175?hl=en&co=GENIE.Platform%3DDesktop) in the parents' sheet. Each named range should be the column where that field exists; for example, if you have **Email** as the second column after the name, it'll be in `B` with the range `B2:B` to capture all rows that exist.

* `parent_names`
* `parent_email`
* `parent_phone`
* `parent_kids`
* `parent_contact`

Once you've created these named ranges, you can reference them in formulas.

We're going to use a bunch of formulas that look like this:

```
=IFERROR(FILTER(parent_phone, parent_contact=1, SEARCH($A2, parent_kids)),"")
```

This formula uses `SEARCH` to find the first field in the `parent_kids` named range which contains this kid's name (`$A2` in this case, so the first column), and for which the `parent_contact` field is equal to `1`, and returns either the value of the `parent_phone` field for that row or an empty string if there's no match.

(_Note_: We leverage `parent_contact` so that we know which parent to use if there's more than one available for a given kid.)

Next, create an additional sheet in the same document as the parents' sheet, with the following fields:

* **Name**: kid's name
* **Parents' Names**: use the formula:
  ```
  =IFERROR(TEXTJOIN(", ", TRUE, FILTER(parent_names, SEARCH($A2, parent_kids))),"")
  ```
  This formula finds all of the parents which contain this kid's name and joins them with commas
* **Main Contact Phone**: use the formula:
  ```
  =IFERROR(FILTER(parent_phone, parent_contact=1, SEARCH($A2, parent_kids)),"")
  ```
* **Main Contact Email**: use the formula:
  ```
  =IFERROR(FILTER(parent_email, parent_contact=1, SEARCH($A2, parent_kids)),"")
  ```

You can add additional fields if you like.

The result should be a record that looks like:

| Name | Parents' Names | Main Contact Phone | Main Contact Email |
| ---- | -------------- | ------------------ | ------------------ |
| Zoe MacPherson | Darryl MacPherson, Wanda MacPherson | 555-1234 | dmac@example.com |

### CardDAV Service

The next component is a backend service that serves address book data so it can be retrieved and updated on your phone. This guide uses [Radicale](https://radicale.org/v3.html) because it stores its data on the filesystem in a well-defined structure, so we can populate it via a script and have it served.

Setting up Radicale is also outside the scope of this post. The project's docs have lots of setup examples.

#### Google Sheets export script

In addition to the CardDAV service, we need a piece that reads data out of the Google Sheet and puts it where the service can get to it. I haven't taken the time to make a proper Github repo for this, but I use the following script (be sure to install the [gspread](https://github.com/burnash/gspread) library).

<details>
<summary><tt>sheet_to_vcf.py</tt></summary>

``` python
#!/usr/bin/env python

from pathlib import Path
import os
import sys
import uuid
import gspread


def get_sheet():
    gc = gspread.oauth()
    return gc.open("Magic Address Book")


def get_uuid(name):
    return uuid.uuid5(uuid.NAMESPACE_X500, name)


def make_kids_names(kids):
    return " ".join([x.split(" ")[0] for x in kids.split(", ")])


def make_name(parent):
    try:
        first, last = parent["Name"].split(" ")
    except ValueError:
        first = parent["Name"].split(" ")
        last = ""
    if len(first) == 1:
        first = first[0]
    kids_firsts = make_kids_names(parent["Kids"])
    if kids_firsts:
        return f"{last};{first} ({kids_firsts})"
    return f"{last};{first}"


def make_formatted_name(parent):
    try:
        first, last = parent["Name"].split(" ")
    except ValueError:
        first = parent["Name"].split(" ")
        last = ""
    if len(first) == 1:
        first = first[0]
    kids_firsts = make_kids_names(parent["Kids"])
    if kids_firsts:
        return f"{first} ({kids_firsts}) {last}"
    return f"{first} {last}"


def make_address(parent):
    if not parent["Address"]:
        return None
    return f"ADR:;;{parent['Address']};;;;"


def make_vcf(row):
    output = ["BEGIN:VCARD", "VERSION:4.0"]
    output.append(f"UID:{get_uuid(row['Name'])}")
    output.append(f"EMAIL;PREF=1;TYPE=home:{row['Email']}")
    output.append(f"FN:{make_formatted_name(row)}")
    output.append(f"N:{make_name(row)};;;")
    if row["Phone"]:
        output.append(f"TEL;TYPE=home;VALUE=TEXT:1-{row['Phone']}")
    if row["Address"]:
        output.append(f"ADR:;;{row['Address']};;;;")

    output.append("END:VCARD\n")
    return "\n".join(output)


if __name__ == "__main__":
    try:
        Path(sys.argv[1]).stat()
    except IndexError:
        print(
            "Must provide as the first argument a path to a pre-existing directory to place VCF files in"
        )
        sys.exit(2)
    except (FileNotFoundError, TypeError):
        print(f"The provided path ({sys.argv[1]}) does not exist!")
        sys.exit(2)

    root = Path(sys.argv[1])
    for f in root.iterdir():
        if f.name.endswith("vcf"):
            os.remove(f)
    for p in get_sheet().get_worksheet(0).get_all_records():
        if p["Contact"] not in [1, 2]:
            continue
        current = root / f"{get_uuid(p['Name'])}.vcf"
        with current.open("w") as f:
            print(make_vcf(p))
            f.write(make_vcf(p))
```
</details>

This script reads the data out of the Google Sheet and turns it into `.vcf` vcard files suitable for use by Radicale. It takes a directory as the sole argument, which should be the spot on the filesystem where you've configured Radicale to store its data.

### CardDAV Synchronization

The last component is relatively straightforward: synching a CardDAV address book to your phone's contact list. I found [DAVx5](https://www.davx5.com/) to be the easiest way to set this up. (Note that the Google Play version costs $6.50 or so, but you can install it [via the open-source F-Droid app store](https://f-droid.org/en/packages/at.bitfire.davdroid/) for free.)

Install DAVx5, open it, and add a new CardDAV service. Point it to the URL of the Radicale service you set up, and your phone will have a new contacts list containing all of the data from your spreadsheet.

If you want to have the synchronization happen automatically and continuously, you'll need to set up Radicale somewhere with a URL that DAVx5 can reach (i.e. on a web server somewhere), but if you want to just do the sync once, you can run Radicale on your laptop and provide its IP address to DAVx5.

## Conclusion

Having this resource is going to be incredibly useful for me in keeping track of my kids' friends and managing their lives. Hopefully this guide is at least a tiny bit useful to someone else as well.
