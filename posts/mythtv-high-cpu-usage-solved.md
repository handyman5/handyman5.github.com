---
title: MythTV high CPU usage - solved!
slug: mythtv-high-cpu-usage-solved
date: 2013-10-02 12:00:00 UTC-07:00
tags: fix, mythtv
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx63wjy2n"
---

_(originally from <https://web.archive.org/web/20220521093228/http://ajcsystems.com/blog/blog/2013/10/02/mythtv-high-cpu-usage-solved/>)_

I’ve been dealing with a very strange problem with my [MythTV](http://www.mythtv.org/) HTPC for a while now. Occasionally, for no good reason that I could see, both the frontend and backend processes would spike to 100% CPU utilization and hang out there until they were restarted. This caused the fans to spin up, which was annoying.

I had some time today to investigate this problem, and it turns out (at least so far) to be related to the [UPnP](http://www.mythtv.org/wiki/UPnP) feature. Read on for more about how I fixed it.

<!-- TEASER_END -->

What Was Wrong
--------------

The problem was simple: some seemingly arbitrary amount of time after starting up, both the `mythfrontend` and `mythbackend` processes would each start taking up 100% of a CPU, and spinning their wheels (per `strace`) on a series of `select()` and `ioctl()` calls. This behavior would persist until the processes were restarted. It happened to the backend even if the frontend wasn’t running (I didn’t test the converse). Also, the HTPC bits still worked fine and played videos; it seemed like the CPU utilization was at a lower priority than actually doing useful work.

That said, it was still really annoying, and it had an actual impact in terms of excess heat and noise, along with power consumption. I sat down today to beat my head against it until something broke.

What Didn’t Work
----------------

I tried a lot of different things to figure out what might be causing this problem. I upgraded my HTPC to the recently-released 0.27 version of MythTV; I tried rebooting several times; I even sat with an `strace` running on the backend and frontend processes to see what happened when they wigged out. (That’s how I noticed the `select()` and `ioctl()` behavior.)

However, none of this investigation pointed me towards a real culprit.

What Did Work (at least so far)
-------------------------------

I happened to stumble upon [this post](http://www.mythtv.org/pipermail/mythtv-users/2013-September/353299.html) which indicated that turning off UPnP fixed his issue on both the front- and backend processes. That was an important find, because most of the other information I ran into only talked about one or the other process misbehaving.

I disabled UPnP on both processes, and they’ve been working great so far. This is a significant improvement from before; I could be pretty confident that the high CPU utilization would begin within ~10 minutes of the processes starting up, and without fail within ~30 minutes.

How To Make It Stick
--------------------

### Backend

I’m running [Mythbuntu](http://www.mythbuntu.org/), so the underlying system is a Debian derivative using `upstart`. The `mythtv-backend` service isn’t actually written as an upstart job; instead, it uses the configuration file `/etc/init/mythtv-backend.conf`. I added “`--noupnp`” to that file:

``` shell
adam@mythtv:~$ diff -ub mythtv-backend.conf{.orig,}
— mythtv-backend.conf.orig    2013-10-02 21:58:46.000000000 -0700
+++ mythtv-backend.conf         2013-10-02 21:58:16.000000000 -0700
@@ -27,5 +27,5 @@

 script
        test -f /etc/default/locale &amp;&amp; . /etc/default/locale || true
–       LANG=$LANG exec /usr/bin/mythbackend –syslog local7 –user mythtv –daemon
+       LANG=$LANG exec /usr/bin/mythbackend –syslog local7 –user mythtv –daemon –noupnp
 end script
```

and restarted the service, and that seems to have fixed things right up.

### Frontend

Mythbuntu automatically runs the frontend process on session startup, so all I needed to do was change the startup file in `~/.config/autostart/mythtv.desktop`:

``` shell
adam@mythtv:~/.config/autostart$ diff -ub mythtv.desktop*
+++ mythtv.desktop.orig          2013-10-02 22:05:16.000000000 -0700
--- mythtv.desktop               2013-10-02 22:05:29.000000000 -0700
@@ -2,7 +2,7 @@
 Name=MythTV Frontend
 Comment=A frontend for all content on a mythtv-backend
 GenericName=MythTV Viewer
-Exec=mythfrontend –service
+Exec=mythfrontend –service –noupnp
 Type=Application
 Encoding=UTF-8
 Icon=mythtv
```

This did the trick on the frontend side.

What I Learned
--------------

MythTV is ludicrously complicated. I didn’t even realize it had a UPnP feature, and that turned out to be what was causing all my trouble. On the plus side, the program guide in 0.27 is much more stable, so the day turns out not to have been a total waste.
