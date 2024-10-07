<!--
.. title: Blog Setup Notes
.. slug: blog-setup-notes
.. date: 2024-07-05 16:30:22 UTC-07:00
.. devstatus: 4e
.. status: featured
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

This page details the things I had to do to set up this blog.

## Initial Setup

References:

* <https://getnikola.com/handbook.html>
* <https://getnikola.com/getting-started.html>

## Automated Build

Using the [`nikola-action` Github Action](https://github.com/getnikola/nikola-action). Notably, I had to reference `v8` even though the README says `v4`.

Source: [main.yml](../../.github/workflows/main.yml)

I had to use a custom action to do the Nikola build; see [this page](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow) for how to do so.

Additional references:

* <https://getnikola.com/blog/automating-nikola-rebuilds-with-github-actions.html>

## Backfilling old posts

I have some old blogs which have vanished from the internet (but not from the Internet Archive). I used [this tool](https://www.minifier.org/html-to-markdown) to convert their HTML to Markdown so I could import them here.

## Style References

* [The Cloistered Monkey](https://necromuralist.github.io/) - <https://github.com/necromuralist/necromuralist.github.io>

## Technical References

* <https://github.com/snorremd/snorreio/tree/main>
* <https://jrvcomputing.wordpress.com/2023/03/29/setting-up-my-personal-website-using-nikola/>
* <https://randomgeekery.org/post/2020/01/building-a-starter-blog-with-nikola/>
* <https://necromuralist.github.io/posts/converting-nikola-from-a-blog-to-a-site/>
* <https://www.ctrl.blog/entry/nikola-sections.html>
* <https://adriaanrol.com/posts/2020/building-a-site-using-nikola/>
* <https://chriswarrick.com/blog/2014/10/13/revamping-my-projects-page-with-nikola/>

## Custom Domain

* <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages#using-an-apex-domain-for-your-github-pages-site>
* <https://stackoverflow.com/questions/9082499/custom-domain-for-github-project-pages>


## Bluesky Comments

Still in progress. Prior art:

* <https://graysky.app/blog/2024-02-05-adding-blog-comments>
* <https://graysky.app/blog/2023-10-17-getting-started-atproto>
* <https://snorre.io/blog/2023-08-19-atproto-bluesky-comment-system/>
* <https://bsky.app/profile/did:plc:sq6aa2wa32tiiqrbub64vcja/post/3kkobhar5qk2e>
