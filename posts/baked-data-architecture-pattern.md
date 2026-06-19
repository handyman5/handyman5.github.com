---
title: The “Baked Data” architecture pattern
slug: baked-data-architecture-pattern
date: 2021-01-15 12:00:00 UTC-07:00
tags: patterns
category: 
link: 
description: 
type: text
---

I learned about this recently from this blog post, and it seems like a really robust tool to have in my tool belt:

<!-- TEASER_END -->

> [M]ost of the site content lives in a SQLite database, and I use custom Jinja templates to implement the site’s different pages.
> This is effectively a variant of the static site generator pattern. The SQLite database is built by scripts as part of the deploy process, then deployed to Google Cloud Run as a binary asset bundled with the templates and Datasette itself.
> I call this the **Baked Data** architectural pattern — with credit to Kevin Marks for [helping me](https://chat.indieweb.org/dev/2020-11-15#t1605478365993400) coin the right term. You bake the data into the application.
> It’s comparable to static site generation because everything is immutable, which greatly reduces the amount of things that can go wrong — and any content changes require a fresh deploy. It’s extremely easy to scale — just run more copies of the application with the bundled copy of the database. Cloud Run and other serverless providers handle that kind of scaling automatically.
> Unlike static site generation, if a site has a thousand pages you don’t need to build a thousand HTML pages in order to deploy. A single template and a SQL query that incorporates arguments from the URL can serve as many pages as there are records in the database.
