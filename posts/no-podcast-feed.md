---
title: "What do you mean, there's no podcast feed?"
slug: no-podcast-feed
date: 2012-10-22 12:00:00 UTC-07:00
tags: 
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150421230946/http://ajcsystems.com/blog/blog/2012/10/22/what-do-you-mean-theres-no-podcast-feed/>)_

Yahoo runs a little-known service called [Yahoo Pipes](https://web.archive.org/web/20150421230946/http://pipes.yahoo.com/), which lets you take inputs from a wide variety of sources (including, but specifically not limited to, RSS feeds), spindle, fold, and mutilate them, and then get an RSS feed out the other end. This is particularly useful if you have an RSS feed from a source that does some of what you want it to do, but isn’t quite perfect.

Case in point: the head designer for **Magic: The Gathering** started posting podcast episodes on [his Tumblr blog](https://web.archive.org/web/20150421230946/http://markrosewater.tumblr.com/). However, they’re mixed in with other non-podcast posts, and Tumblr’s RSS feed doesn’t link the podcast files up properly so they work in a podcast reader. Obviously, this situation cannot abide. I created a pipe to magically transmute the plain RSS feed into a fancy podcast feed, and this post will _show you how!_

<!-- TEASER_END -->

**TL;DR**: This is [the podcast feed](https://web.archive.org/web/20150421230946/http://pipes.yahoo.com/blahblahblah33/blogatog) I wound up with.

Quick Introduction to Yahoo Pipes
---------------------------------

Per Yahoo’s description:

> Pipes is a powerful composition tool to aggregate, manipulate, and mashup content from around the web.
> 
> Like Unix pipes, simple commands can be combined together to create output that meets your needs:
> 
> *   combine many feeds into one, then sort, filter and translate it.
> *   geocode your favorite feeds and browse the items on an interactive map.
> *   power widgets/badges on your web site.
> *   grab the output of any Pipes as RSS, JSON, KML, and other formats.

Getting Started
---------------

You’ll need a Yahoo account to create a pipe; that’s beyond the scope of this tutorial. Click on **Create a pipe** to get started.

The basic mechanism of this tool is adding new components from the left-hand pane (by either dragging-and-dropping them into the canvas, or clicking on the little “+” button next to each component). You can also link components together by dragging from the circle at the bottom of one component to the circle at the top of another component; the canvas will draw a nice line to indicate the flow of data within the pipe.

The other important thing to know is that clicking on a pipe component will change its color (to orange) and display whatever the pipe’s current output would be at that point in the “Pipe Output” pane at the bottom of the window.

When you’re done making a pipe, click **Save**, and then **Back to My Pipes** to see how it worked out.

Fetching Feed Items
-------------------

For this feed, I used the **XPath Fetch Page** “Source” component, with an XPath expression that gave me just the body DIVs I wanted:

*   URL: [http://markrosewater.tumblr.com/tagged/Drive-to-Work](https://web.archive.org/web/20150421230946/http://markrosewater.tumblr.com/tagged/Drive-to-Work)
*   XPath: `//div[@class="post-content"]`

Building a RSS Feed
-------------------

The next step is to turn that list of XPath results into a proper RSS feed. Add the **Create RSS** “Operator” component, and link it to the **XPath Fetch Path** component. Here are the parameters I used to create the RSS feed:

*   Title: `item.div.0.h3.a.content`
*   Description: `item.div.1.p`
*   Link: `item.div.0.h3.a.href`
*   media:content url: `item.div.0.h3.a.href`
*   media:content type: item.”audio/mp4a-latm”

To break this down a little bit, each result from the **XPath Fetch Page** component becomes an _item_ in the **Create RSS** component. You can poke around the original page content to figure out exactly how to specify the particular bits you want to use to fill the various fields. **Create RSS** will then iterate through each XPath result and make a new post in the RSS feed with that XPath item as its source.

### Simple example

Let’s say the **XPath Fetch Page** component returned three items, which looked like so:

``` html
<div>
    <h1>First Post Title</h1>
    <p>Wonderfully clever post goes here.</p>
</div>
<div>
    <h1>Second Post Title</h1>
    <p>Second post; slightly less clever</p>
</div>
<div>
    <h1>Third Post Title</h1>
    <p>At this point we're just phoning it in.</p>
</div>
```

For this example, the **Create RSS** component will make three objects. If you specify the _Title_ as `item.div.h1`, then the resulting RSS feed will have three <item>s, each of which will have a `title` child node with the appropriate title text.

Making the RSS feed into a Podcast
----------------------------------

It’s not enough to have a fancy RSS feed of your posts; if you want to get them recognized by most podcast readers, you’ll need to add some metadata that indicates where the podcast file can be found, what kind of media it is, etc. etc.

For this step, you’ll need a **Loop** “Operator” component. Within the **Loop** component, drag and drop a **Item Builder** “Sources” component.

We want to add two attributes to each item in the RSS feed: `url` and `type`.

*   url: `item.div.0.h3.a.href`
*   type: `audio/mp4a-latm`
*   assign **first** results to `item.enclosure`

Note that this `url` definition is the same as the “Link” and “media:content:url” definitions of the **Create RSS** component. Probably at least one of these is overkill.

Link this component to the **Pipe Output** component, and enjoy your new podcast feed!

Other Applications
------------------

Yahoo Pipes is wildly flexible; I’ve used it to create RSS feeds for lots of different things:

*   Pages which update regularly in a structured format but which do not provide an RSS feed
*   Excluding authors I don’t care to hear from in an existing RSS feed
*   Replacing the short text slug in an abridged RSS feed with the full article text from the page (**Loop** + **Fetch Page** are your friends here)

Feel free to post in the comments any pipes you make with these instructions, or any suggestions you have to improve them (or the podcast feed I made).
