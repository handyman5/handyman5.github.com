---
title: Creating an EPUB from a Wordpress blog
slug: creating-an-epub-from-a-wordpress-blog
date: 2017-11-26 12:00:00 UTC-07:00
tags: code
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx5uixp2t"
---

Recently, I wanted to create epubs of some reading material, specifically some Wordpress-hosted blogs. Rather than implementing a separate script for each blog I wanted an epub from, I wrote a tool to figure it all out for me: [trivialpub](https://github.com/handyman5/trivialpub).

<!-- TEASER_END -->

Usage is simple: provide a YAML config file, such as:

``` yaml
toc_url: https://practicalguidetoevil.wordpress.com/table-of-contents/
toc_parser: |
  [x.get('href') for x in soup.select('div.entry-content a') if 'class' not in x.attrs]

```

And trivialpub will do the rest:

``` shell
$ ./trivialpub.py -c practicalguide.yaml 
Processing chapter https://practicalguidetoevil.wordpress.com/2015/03/25/prologue/
Processing chapter https://practicalguidetoevil.wordpress.com/2015/04/01/chapter-1-knife/
Processing chapter https://practicalguidetoevil.wordpress.com/2015/04/08/chapter-2-invitation/
Processing chapter https://practicalguidetoevil.wordpress.com/2015/04/16/chapter-3-squire/
[...]
$ ls -l build/
total 9216
-rw-r--r--  1 acompton  admin  2004507 Nov 26 15:05 practicalguide.epub

```

I’ve included a number of examples in the repo, but basically, you either need to feed it a list of URLs to transform or a Python expression which, when eval’ed in context, will generate a list of URLs. (Yes, yes, eval() is the devil, I know.)

PRs and suggestions welcome.
