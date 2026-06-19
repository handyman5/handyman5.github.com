---
title: ProgressTwitch!
slug: progresstwitch
date: 2015-06-07 12:00:00 UTC-07:00
tags: howto
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20220521094735/http://ajcsystems.com/blog/blog/2015/06/07/progresstwitch/>)_

In the immortal words of Samuel L. Jackson, hold on to your butts. I’m going to explain, in painful detail, just exactly what it took to get [ProgressTwitch](https://web.archive.org/web/20220521094735/http://www.twitch.tv/comptona5 "https://web.archive.org/web/20220521094735/http://www.twitch.tv/comptona5") off the ground.

<!-- TEASER_END -->

[Watch live video from Comptona5 on www.twitch.tv](https://web.archive.org/web/20220521094735/http://www.twitch.tv/comptona5?tt_medium=live_embed&tt_content=text_link "https://web.archive.org/web/20220521094735/http://www.twitch.tv/comptona5?tt_medium=live_embed&tt_content=text_link")


Genesis
-------


This all started when my friend [Camarice](https://web.archive.org/web/20220521094735/http://www.twitch.tv/camarice "https://web.archive.org/web/20220521094735/http://www.twitch.tv/camarice") explained to me what Twitch was and how it worked. I was impressed by the technology, but it all seemed a bit frivolous to me at first. I thought, “Wouldn’t it be funny if there was a Twitch stream that just broadcast some static image, 24/7?” I was wracking my brain trying to think of things that would be appropriate to broadcast, and suddenly I remembered [Progress Quest](http://progressquest.com/"). For those of you who are not old, Progress Quest is a satire of the role-playing game genre. Like any RPG, you roll up a character and set out on your quest; but unlike any other RPG, Progress Quest plays itself for you, randomly generating a variety of quests, encounters, and loot. You just leave it running and check in every now and again to see how powerful your character has become.


This immediately seemed like a perfect fit: set up a system to run Progress Quest and stream it to Twitch 24/7.


What Didn’t Work
----------------


### Twitch Streaming in Linux


The only computer that I leave on 24/7 is my homemade DVR, running Linux. My first thought was to set up Twitch streaming from Linux directly, to set up a virtual screen and run Progress Quest in WINE, and then to stream the whole shebang to Twitch. That plan disintegrated almost immediately; I was unable to get any Twitch broadcasting software running on my Linux box. It’s not particularly powerful, and it’s running a distribution that’s about three years old, so I wasn’t really surprised; nevertheless, this was definitely a dead end.


### Virtualbox Windows VM in Linux


Next, I decided to try setting up a portable virtual machine with a Windows guest, configuring everything in it to start Twitch streaming at boot up, and then run *that* on my Linux server. Spoiler alert: this was also unsuccessful, although for a long time it seemed like it was going to work out OK.


I started by configuring a Virtualbox VM with a completely legitimate and legal copy of Windows 7. Once that was installed and running, I started installing the Twitch streaming software. It turns out that [Open Broadcaster Software](https://obsproject.com/) requires some DirectX features that are not supported by the DirectX emulation available in Virtualbox, even with the guest extensions and custom drivers installed. I then tried [XSplit Gamecaster](https://www.xsplit.com/products/gamecaster), with which I was able to get most of the way to a working setup. It took a lot of tweaking to get everything running the way it was supposed to, looking right, and starting up on boot, but eventually I had a working portable VM that would stream Progress Quest to Twitch automatically. I copied that VM to the Linux server and launched it, and lo and behold… a strange graphics corruption bug that put a big black rectangle near the middle of my screen, and also in the stream. I tried to update the drivers on my Linux box, but short of a full distribution upgrade to something more recent, it wasn’t going to happen; and I don’t want to tweak my DVR too hard for fear of blowing it up and having to rebuild it. On to the next option!


What Did Work
-------------


### Amazon Web Services Windows VM


When that failed, I decided to abandon my plan of running anything on my existing Linux server, and instead set up a Windows VM in Amazon EC2. That actually went relatively smoothly, with one big exception: EC2 virtual machines do not have sound hardware, and OBS requires a sound card be present in order to function. [VB-CABLE Virtual Audio Device](https://web.archive.org/web/20220521094735/http://vb-audio.pagesperso-orange.fr/Cable/index.htm "https://web.archive.org/web/20220521094735/http://vb-audio.pagesperso-orange.fr/Cable/index.htm") to the rescue! After installing that virtual device driver and setting it as the default, I was able to leave OBS running even when I wasn’t connected to the Remote Desktop session.


One setup note here: the VPC Amazon made for me did not have a default route out to the internet, as pointed to [here](http://stackoverflow.com/a/25555470). I was unable to access my VM until I went in to the VPC configuration and added one by hand.


Final Setup
-----------


For future reference, this is what I’ve got running now:


* Windows Server 2012 (ami-830ee0c7) on a t2.micro EC2 instance
* Open Broadcaster Software 0.651 beta
* Progress Quest 6.2
* VB-CABLE Virtual Audio Device v.42b
