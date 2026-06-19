---
title: Creating an ePub from a list of links
slug: creating-an-epub-from-list-of-links
date: 2017-01-22 12:00:00 UTC-07:00
tags: howto
category: 
link: 
description: 
type: text
---

I’ve read and enjoyed parts of [Michael O. Church’s](https://web.archive.org/web/20201205012321/https://michaelochurch.wordpress.com/ "https://web.archive.org/web/20201205012321/https://michaelochurch.wordpress.com/") take on Venkatesh Rao’s [Gervais Principle](https://web.archive.org/web/20201205012321/http://www.ribbonfarm.com/the-gervais-principle/ "https://web.archive.org/web/20201205012321/http://www.ribbonfarm.com/the-gervais-principle/"), but he took his blog offline before I was able to read them all. I decided to snag copies of all of the posts from [the Wayback Machine](https://web.archive.org/web/20201205012321/https://archive.org/web/ "https://web.archive.org/web/20201205012321/https://archive.org/web/") and turn them into an ebook for convenient reading. This appears to be a solved problem thanks to [this handy little Python library, pypub](https://web.archive.org/web/20201205012321/https://pypub.readthedocs.io/en/latest/ "https://web.archive.org/web/20201205012321/https://pypub.readthedocs.io/en/latest/"), but just in case it winds up being useful to someone here is what I did.

<!-- TEASER_END -->

### Building the list of links


I googled for the first post, looked it up in the Wayback Machine, noted a working URL, and kept following links until I found all of the posts in the series.


For reference, here they are.

```

1: https://web.archive.org/web/20150325112004/https://michaelochurch.wordpress.com/2013/02/19/gervais-principle-questioned-macleods-hierarchy-the-technocrat-and-vc-startups/
2: https://web.archive.org/web/20150705103513/https://michaelochurch.wordpress.com/2013/02/20/1410/
3: https://web.archive.org/web/20151221082352/https://michaelochurch.wordpress.com/2013/02/22/gervais-rehash-part-iii-markov-and-management-plus-a-4th-culture/
4: https://web.archive.org/web/20151221143632/https://michaelochurch.wordpress.com/2013/02/26/gervais-macleod-4-a-world-without-losers/
5: https://web.archive.org/web/20151221143322/https://michaelochurch.wordpress.com/2013/02/28/gervais-macleod-5-interfaces-meritocracy-and-the-effort-thermocline/
6: https://web.archive.org/web/20151221143806/https://michaelochurch.wordpress.com/2013/03/01/gervais-macleod-6-morality-civility-and-chaos/
7: https://web.archive.org/web/20151018091056/https://michaelochurch.wordpress.com/2013/03/11/gervais-macleod-7-defining-organizational-health-the-mike-test-and-vc-istans-fate/
8: https://web.archive.org/web/20151221083041/https://michaelochurch.wordpress.com/2013/03/12/gervais-macleod-8-human-nature-theories-x-y-z-and-a/
9: https://web.archive.org/web/20151221144342/https://michaelochurch.wordpress.com/2013/03/14/gervais-macleod-9-convexity/
10: https://web.archive.org/web/20151221143541/https://michaelochurch.wordpress.com/2013/03/17/gervais-macleod-10-the-pull-of-lawful-evil/
11: https://web.archive.org/web/20151225141206/https://michaelochurch.wordpress.com/2013/03/18/gervais-macleod-11-alignment-and-careers/
12: https://web.archive.org/web/20151221143250/https://michaelochurch.wordpress.com/2013/03/19/gervais-macleod-12-growth-chaos-and-risk/
13: https://web.archive.org/web/20151221143502/https://michaelochurch.wordpress.com/2013/03/20/gervais-macleod-13-separability-work-and-play/
14: https://web.archive.org/web/20151221144410/https://michaelochurch.wordpress.com/2013/03/21/gervais-macleod-14-expanding-alignment-plus-well-adjustedness/
15: https://web.archive.org/web/20151221144210/https://michaelochurch.wordpress.com/2013/03/22/gervais-macleod-15-what-is-being-rich/
16: https://web.archive.org/web/20151221143221/https://michaelochurch.wordpress.com/2013/03/25/gervais-macleod-16-healthy-culture-vs-why-you/
17: https://web.archive.org/web/20151018092426/https://michaelochurch.wordpress.com/2013/03/26/gervais-macleod-17-building-the-future-and-financing-lifestyle-businesses/
18: https://web.archive.org/web/20151221144309/https://michaelochurch.wordpress.com/2013/03/28/gervais-macleod-18-more-on-trust-square-root-syndrome-brownian-and-progressive-time/
19: https://web.archive.org/web/20151221144051/https://michaelochurch.wordpress.com/2013/03/29/gervais-macleod-19-living-in-truth-fighting-the-lie/
20: https://web.archive.org/web/20150919091259/https://michaelochurch.wordpress.com/2013/04/01/gervais-macleod-20-bozo-bit-vs-simple-trust/
21: https://web.archive.org/web/20150910154001/https://michaelochurch.wordpress.com/2013/04/03/gervais-macleod-21-why-does-work-suck/
22: https://web.archive.org/web/20150919133351/https://michaelochurch.wordpress.com/2013/04/16/gervais-macleod-22-inferno/
23: https://web.archive.org/web/20151221143922/https://michaelochurch.wordpress.com/2013/04/30/gervais-macleod-23-managers-mentors-executives-cops-and-thugs/
24: https://web.archive.org/web/20151221082517/https://michaelochurch.wordpress.com/2013/06/04/gervais-macleod-24-fundamental-theorem-of-employment/
25: https://web.archive.org/web/20151221083106/https://michaelochurch.wordpress.com/2013/06/08/gervais-macleod-25-state-and-truth-seekers-plus-the-emergence-of-the-technocrat/
26: https://web.archive.org/web/20151221082619/https://michaelochurch.wordpress.com/2013/08/06/gervais-macleod-26-r-and-k-selection-in-organizations-and-capitalism/

```


### Creating the ebook


[pypub](https://web.archive.org/web/20201205012321/https://pypub.readthedocs.io/en/latest/ "https://web.archive.org/web/20201205012321/https://pypub.readthedocs.io/en/latest/") made this bit super easy!



```
import pypub, os
epub = pypub.Epub('Gervais Principle Questioned')
urls = open('links.txt').read()
real_urls = [x for x in urls.split() if x.startswith('https:')]
for u in real_urls:
  c = pypub.create_chapter_from_url(x)                                                                                                     
  epub.add_chapter(c)          
epub.create_epub(os.getcwd())  

```

Et voila!
