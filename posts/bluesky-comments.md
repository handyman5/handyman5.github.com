<!--
.. title: Bluesky Comments
.. slug: bluesky-comments
.. date: 2024-12-06 00:29:47 UTC-08:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
.. bluesky: 3lcmsvl47k22t
-->

As of this post, posts on this blog will each be associated with a Bluesky post and display that post and its responses inline.

<!-- TEASER_END -->

I was inspired to do this by [several](https://blahg-bsky.netlify.app/post/bsky-comments/) [example](https://graysky.app/blog/2024-02-05-adding-blog-comments) [implementations](https://emilyliu.me/blog/comments). It's particularly appealing for a static blog to manage comments in this way, since I don't have to set up Disqus or maintain any kind of backend service myself to handle comments.

I started with the Nikola [mastodoncomments](https://plugins.getnikola.com/v8/mastodoncomments/) plugin. My implementation of the Bluesky version is in the repo for this blog at <https://github.com/handyman5/handyman5.github.com/tree/src/plugins/blueskycomments>; I don't have the time to pretty it up and submit a PR, but it's available if anybody wants to purloin it and do so.

I ran into quite a bit of trouble though, since Nikola doesn't support any modern Javascript frontend systems (like React) out of the box. I had to write my own implementation and my Javascript is very rusty. I like what I wound up with, though; since it's using the [oEmbed widget](https://docs.bsky.app/docs/advanced-guides/oembed), the posts will always be rendered with the newest features, and I didn't have to go to the trouble of tinkering with the Bluesky API apart from getting the post responses in the first place. I could have added support for `npm` to my automated build pipeline and used [this npm package](https://www.npmjs.com/package/bluesky-comments) but I don't know npm well and I worried it'd be overkill. If I run into any problems with my code, though, I'll probably switch to that rather than pouring lots of time into tinkering.

The other trouble I ran into is that the logic uses a `fetch` function to grab each comment, and it was appending them into the body in an arbitrary order based on when the functions returned. It took me a while to figure out a good strategy for ensuring that the comments appear in the correct order (i.e. the way the API returns the set initially). I don't have an implementation of nesting the replies, but I can't imagine any of my posts will get _that_ many responses so I'm not super worried about it. 😅

At any rate, it's working, and I'm jazzed.
