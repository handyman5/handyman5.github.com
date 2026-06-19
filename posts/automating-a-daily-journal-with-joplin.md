---
title: Automating a daily journal with Joplin
slug: automating-a-daily-journal-with-joplin
date: 2019-11-30 12:00:00 UTC-07:00
tags: personal knowledge management
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx5rxsl2b"
---

![image](/images/1_5qpcOrSwad1u-jE5Ls8Fsg.webp)

I have a long-standing interest in [personal knowledge management](https://en.wikipedia.org/wiki/Personal_knowledge_management) (PKM). I’ve tried lots and lots of different tools, and I recently learned about [Joplin](https://joplinapp.org/) and decided to try it out.

<!-- TEASER_END -->

## Requirements, or “Is that too much to ask?”

There’s not a lot of specific things I want out of a PKM tool, but I’ve had a hard time getting them all together in a single product. My must-haves are:

* Absolutely minimal time-to-capture, so as not to interrupt flow

* Some sort of hierarchical organization, so I have a place to stash notes that aren’t currently pertinent but are worth keeping around for future reference

* Some sort of search functionality (I’m not above running grep -r on a directory of text files)

* Some sort of backup or sync mechanism (similarly, */5 * * * * git commit -a && git push would suffice)

* Some mechanism for tracking a daily journal so I know what I accomplished over the last day/week/month; this was a habit I picked up from [PlannerMode](https://www.emacswiki.org/emacs/PlannerMode), which should give you an idea of how long I’ve been shaving this particular yak

Joplin manages most of these:

* I used Automator to make a [global keyboard shortcut](https://appleinsider.com/articles/18/03/14/how-to-create-keyboard-shortcuts-to-launch-apps-in-macos-using-automator) to get quick access to write a new note

* Notebooks and sub-notebooks are arbitrarily nestable, QED

* Search works fine, and the cmd-G “Goto anything” feature is handy (if incomplete since you cannot “go” to notebooks)

* Dropbox sync, that works

However, Joplin does not have a daily journal built-in. Since this was the only major shortcoming, I decided to hack something together.

## tl;dr show me the code

Joplin does have [an API](https://github.com/laurent22/joplin/blob/master/readme/api.md), but reading through the docs for it was painful so I decided to just run the command-line version too and automate it. I created a script named journal.sh that I can run at any time to create a new template-based file with today’s date in the appropriate notebook, and then I can go fill it out with the day’s work.

    $ cat ~/bin/journal.sh
    #!/bin/bash

    TMPDIR=`mktemp -d`
    TMPFILE=$TMPDIR/$(date +"%Y-%m-%d")

    cat >$TMPFILE <<EOF
    ## To do today:

    ## Completed today:

    ## Notes:

    EOF

    joplin import --format md $TMPFILE "1. Daily Journal"
    joplin sync
    rm -rf $TMPDIR

This gets the job done, and if I were feeling really ambitious I could set up a cron job to run this once a day. Note that the command-line and GUI versions are completely separate and need to be logged into separately, which is why the script calls joplin sync (as the new note would not be promptly visible in the GUI otherwise).

I’ve been enjoying working with Joplin so far, and although history indicates that I’ll probably eventually chafe at its limitations and try to find something else, hope springs eternal.
