<!--
.. title: Creating a Bluesky Bot
.. slug: creating-a-bluesky-bot
.. date: 2024-11-21 00:36:04 UTC-08:00
.. tags: howto, bluesky
.. category: 
.. link: 
.. description: 
.. type: text
-->

I've been experiencing some burnout recently, and one of the best ways for me to fix that is to build something. Couple that with my opinions about the recent US election[^1], and I wanted to do something to learn about Bluesky and spark a little discussion if I could.

So I built a bot that posts once an hour about which countries various billionaires could buy.

![image](/images/Screenshot_20241121_003817.png)

<!-- TEASER_END -->

tl;dr the repo is <https://github.com/handyman5/bsky-buy-a-country-bot>

This was an interesting Journey of Discovery ™️, which was both easier and harder than I expected. I knew the basic algorithm would be to get a list of billionaires, a list of countries' GDP, compare them, generate some post content, and trigger a post. I originally thought about using some fixed data sources like [Kaggle](https://www.kaggle.com/datasets), but then I realized I could use [Wikidata's SPARQL](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial) to pull all the data I needed from a source which would stay up to date indefinitely and not require me to periodically redownload new data sets.

I did have to use ChatGPT to help me figure out the query format. SPARQL was very difficult for me to figure out by myself, and having a helping hand to generate some sample queries that I could tweak and extend was invaluable.

I spent some time trying to figure out how to get the profile images of the billionaires (that information is in the Wikidata dataset), but eventually I decided that the work of supporting attaching and uploading images with each post was probably more than the additional value that the images would provide.

The last thing I worked on was the posting trigger mechanism. I knew I didn't want to run it by hand, so it had to be some hands-off automation. I originally thought to use [Github Actions schedules](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule), but it turns out that workflows scheduled this way (at least from organizations on the free tier) have very little in the way of timeliness guarantees. I was waiting for tens of minutes with nothing happening, so I abandoned that idea and replaced it with a simple cron task running on my local homelab server. That did mean that I needed to make the invocation as simple as possible, so I used [`uv` to set the script up to install its dependencies automatically](https://docs.astral.sh/uv/guides/scripts/#running-a-script-with-dependencies). This allowed me to write a very simple cronjob, using [`act` to trigger the workflow](https://github.com/nektos/act) (and leverage all the setup work I'd done for the Github Actions step.)

With this infrastructure in place, my homelab triggers the bot once an hour, it queries Wikidata and gets the relevant datasets, and then generates a post.

One thing I've considered doing in the future is setting up some sort of cache that either leverages a local file or searches Bluesky for the bot's other posts, and identifies which pairings it's made before to avoid duplicates. I don't think it's worth it at this point, but if the bot gets popular I'll probably bother.

[^1]: We can have billionaires or society, but not both.
