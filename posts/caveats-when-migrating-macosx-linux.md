---
title: Caveats when migrating from Mac OS X to Linux for serving Mac OS X home folders
slug: caveats-when-migrating-macosx-linux
date: 2007-02-12 12:00:00 UTC-07:00
tags: linux, mac os x, til
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150422203246/http://ajcsystems.com/blog/page/2/>)_

Also known as, “Things I wish I’d known about on Friday, part 1″. ![:-P](/images/icon_razz.gif)

1. Mac OS X is, generally speaking, case-insensitive. It’s possible to format a disk with a case-sensitive version of HFS+, but that’s not usually done and (I imagine) not well supported or documented. The underlying BSD layer will accept any case for filenames, and preserves the case of files as they are created, but does not actually care about it when accessing them.

    Samba hosted on a Linux box, on the other hand, cares quite a bit about case. By default, the “case sensitive” parameter is set to “auto”, which means “no for Windows clients and yes for everybody else”. Mac OS X reports itself as a Samba client, of course, which means that the Samba server assumes it is asking for a case-sensitive file or folder and attempts to serve it. Unfortunately, it’s not.

    As a workaround, it’s possible to set “case sensitive = no” as a share-level option for shares accessed in Mac OS X, which works to a point. Finder will properly ignore the case of files when requesting them from the Samba server (or, more likely, will accept a filename of any case as a successful open), but other apps in OS X do not honor this setting. Notably among them in my testing is Microsoft Word.

    Dealbreaker. =( I had to go manually rename the home folders of each user that uses the Samba server to match the case of their usernames in the Active Directory (which is CamelCase).

1. Network mounts over the AFP protocol will permit users to save files which contain various scary characters in their names (such as slashes, question marks, asterisks, etc.). Network mounts over Samba do not permit these characters, and mangle the filenames for display by the user agent. The mangled filenames look much like the Windows backward-compatible-long-file-names (i.e. 6CHARS~1), probably on purpose. Mac OS X Server does its magic by way of the UTF-8-MAC file encoding, which as far as I can tell is supported only on Mac OS X Server’s version of Samba. :'(

    I have 5,000 or so files to rename now.

There’s more, but I have to take a call, so that’ll all be in part 2.
