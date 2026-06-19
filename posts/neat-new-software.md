---
title: Neat new software I’ve written recently
slug: neat-new-software
date: 2011-11-13 12:00:00 UTC-07:00
tags: code
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150422203246/http://ajcsystems.com/blog/page/2/>)_

I’ve been on a bit of a coding tear lately. I’ve written a FUSE filesystem for Amazon Cloud Drive, and also made a lot of improvements to my Toodledo API library, including writing a command-line tool modeled on Tom Limoncelli’s Cycle System from [Time Management for System Administrators](http://www.amazon.com/Management-System-Administrators-Thomas-Limoncelli/dp/0596007833).

### FUSE Filesystem for Amazon Cloud Drive

[Github](https://github.com/handyman5/acd_fuse "Github"); does what it says on the tin. I couldn’t find a supported way to upload music from Linux, so I made one. Currently I’m a bit hesitant to call it production-ready, as Amazon has an eight-device-per-account limit and this appears to consume multiple slots instead of counting as just one extra device. I’m hopeful I can get that sorted soon.

### Poodledo (Toodledo API Library)

[Github](https://github.com/handyman5/poodledo "Github"); I wrote (well, forked and extended) a Python library for interacting with the web-based task management system [Toodledo](http://www.toodledo.com/). Toodledo has quite an extensive ecosystem, including a light version of the website suitable for embedding, SMS and Twitter integration, an official iOS client, and several Android clients ([Due Today](http://www.lakeridgesoftware.com/products/android/DueToday/) is what I use). However, there was no easy way to add tasks from a command line, and also it wasn’t possible to create tasks with metadata (due date, project name, priority, etc.).

With the Python library in hand, I wrote a couple of tools to add and manage tasks from a command line. tdcli implements a super-fancy lexer which can add metadata to a task while creating it, e.g. “Create a task that’s due today and part of the Poodledo project #today \*Poodledo”.

### “cycle” for Toodledo

The other tool I wrote for interacting with Toodledo is [cycle](https://github.com/handyman5/poodledo/blob/master/README-cycle.markdown), modeled after Tom Limoncelli’s **Cycle System** from [Time Management for System Administrators](http://www.amazon.com/Management-System-Administrators-Thomas-Limoncelli/dp/0596007833). It would take a while to explain; you should read the book, as it’s excellent. [Here are some examples of its use](https://github.com/handyman5/poodledo/blob/master/README-cycle.markdown).
