---
title: How to get a count of Github PRs, by author
slug: count-github-prs-by-author
date: 2023-02-08 12:00:00 UTC-07:00
tags: howto
category: 
link:
description:
type: text
---

![image](/images/0_0bbs-1ZwaSaEImTQ.webp)

_Photo by Luke Chesser on Unsplash_

I was curious about who was creating the highest number of PRs in a specific git repo, and I couldn’t find a good way to figure it out. So here’s what I did.

<!-- TEASER_END -->

First off, I had to get the count of PRs by author and date. That took me a while to figure out, but the magic wound up being (using the [GitHub CLI tool](https://cli.github.com/)):

    $ gh api /repos/<org>/<repo>/pulls?state=all --template '{{ range . }}{{ printf "%s,%s\n" .user.login .created_at }}{{end}}' --paginate > tmp/prs.csv

That gave me a CSV I could load into a SQLite database [like so](https://www.sqlitetutorial.net/sqlite-import-csv/). I then used [datasette](https://datasette.io/) to run some queries.

The following query is a breakdown of which person created the most PRs in each year:

    select year, author, prs, rank from (

    select ROW_NUMBER() over (PARTITION BY year ORDER BY sum(total) desc) as rank, sum(total) as prs, author, year from ( select count(1) as total, author, strftime('%Y', created) as year from pr_authors group by author, year
     ) group by author, year order by total desc

    )
    where rank <= 1
    order by year asc;

The result looks like:

    year,author,prs,rank
    2018,alice,369,1
    2019,bob,680,1
    2020,claire,858,1
    2021,donald,1260,1
    2022,emily,801,1
    2023,frank,1127,1
