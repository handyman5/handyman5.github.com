---
title: The Little Ol’ Wiki From Pasadena
slug: the-little-ol-wiki-from-pasadena
date: 2013-08-22 12:00:00 UTC-07:00
tags: code
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150422203816/http://ajcsystems.com/blog/blog/2012/10/30/the-little-ol-wiki-from-pasadena/>)_

It seemed like a simple enough desire. I wanted a small, functional wiki with (roughly) the following features:

*   Use a git repository for page storage and version control
*   Map files on the filesystem directly to web pages (making it equally easy to edit from a CLI or from the web UI)
*   Render various wikitexts (particularly Markdown) into some appropriate output format
*   Support intra-page links and image includes, etc.
*   Be written in a language I am comfortable with

I considered several projects, including:

*   [Hatta](http://hatta-wiki.org/About): Backed by a Mercurial repo, non-trivial to change
*   [Giit](http://gitit.net/): Written in Haskell. I had neither the time nor the inclination to learn that for this project.
*   [Gollum](https://github.com/github/gollum): Mostly suitable, but written in Ruby (which isn’t my strong suit). Plus I wasn’t super-fond of the way it handled subdirectories and other complex filetypes.

But none of them quite scratched my itch. Thus, I was left with no choice but to write my own.

### Introducing `valet`

`valet` is [a script that turns any directory into a simple wiki](https://github.com/handyman5/valet), complete with wikitext rendering, editing, and automatically committing changes to version control.

Here’s a short list of `valet`‘s features:

*   Single file, depending only on [bottle](http://bottlepy.org/docs/dev/)
*   Handles navigating around the filesystem rooted where you start it
*   Automagically detects the type of various files, and (if you have the supporting Python libraries installed) renders them as they ought to appear. As a bonus, if you have `pygments` installed, source code will be syntax-highlighted where possible.
*   Changes from the web UI are automatically saved into the git repo (if desired)
*   Runs as a standalone service, serving from your local machine
*   Optionally supports CGI and WSGI; rename the script to `something.cgi` or `something.fcgi` and it will Do The Right Thing TM. This makes it suitable(-ish) for serving through Apache or some such with SSL, authentication, access control, etc. etc.
*   Installable with `pip`!

``` shell
pip install valet
```

Hopefully this proves as useful to other people as it has been for me.
