---
title: Magic SysRq to the Rescue!
slug: magic-sysrq-to-the-rescue
date: 2012-10-02 12:00:00 UTC-07:00
tags: linux
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150422203246/http://ajcsystems.com/blog/page/2/>)_

I recently had to fix a server which had been knocked off the network due to some bad configuration (very long story). When I logged into the remote graphical console, I was greeted with constant, unremitting spam from the kernel log! I wasn’t able to log in because the screen would clear instantly when I started typing.

This calls for [the Magic SysRq key](http://en.wikipedia.org/wiki/Magic_SysRq_key)! A simple press of `Alt+SysRq+0` to set the console log level to 0 silenced all of the log spam and let me log in and get the server back on its feet.

All hail Magic SysRq!
