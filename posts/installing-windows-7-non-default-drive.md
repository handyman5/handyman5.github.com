---
title: "TIL: Installing Windows 7 on a non-default drive"
slug: installing-windows-7-non-default-drive
date: 2013-09-15 12:00:00 UTC-07:00
tags: ["windows", "til"]
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150423071752/http://ajcsystems.com/blog/blog/2013/09/15/til-installing-windows-7-on-a-non-default-drive/>)_

Quick one: today I learned that, when installing Windows 7 on a machine with multiple hard drives, it will refuse to install to a drive which is not set as the default boot device in the BIOS.

It doesn’t tell you this is why it won’t install, of course. It just says “I couldn’t find a valid drive to install to, go read the setup log to find out more.” If you’re inclined to figure out this problem, you then have to Google around a bit to actually find the location of the setup log files, read them through “type setupact.log”, and then happen to run into an error that could be interpreted as being related to BIOS boot order.

Hopefully this note saves somebody the several hours that I wasted today on this. =P
