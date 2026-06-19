---
title: Solved! Terminal Emacs screen tearing/corruption with Unicode characters
slug: solved-terminal-emacs-screen-tearingcorruption-with-unicode-characters
date: 2025-03-10 13:42:48 UTC-07:00
tags: emacs, solved
category:
link:
description:
type: text
bluesky: 3lk2jkumclc2g
---

I was running into a _very_ strange glitch with terminal Emacs, showing up as all sorts of weird screen tearing and graphical corruption while moving around within and between files.

tl;dr It turns out that I had inadvertently included a [Unicode variation selector](https://en.wikipedia.org/wiki/Variation_Selectors_(Unicode_block)), which is a zero-width character (so I couldn't see it in the code) but which was throwing Emacs for an absolute loop. Removing that character fixed the problem. Follow along below the fold to learn how I figured it out.

<!-- TEASER_END -->

## Something isn't right here; let's investigate!

The first hint of trouble I saw was seeing some terminal lines be repeated as I scrolled around within and between files. I've recently been doing some work to improve my Emacs python IDE configuration, so my first suspect was something in that area. I used `emacs -Q` (which disables all customizations) to edit some files, and the graphical corruption persisted. I noticed the glitching most consistently with a specific file, so I used that as my comparison test case while investigating. (This turns out to be important later on.)

Ok, so if it isn't the customization, perhaps it's the version of Emacs? I'm running 30.1, installed via snap, so I tried rolling it back. I used `snap info emacs` to get the list of available channels and `snap refresh emacs --channel=28.x/beta` to grab an older one. Sadly, I still had graphical glitching with that older version, even when running without customizations.

After ruling out the Emacs version, I thought perhaps it was related to the console somehow. I use Konqueror as my daily driver, but I also have [Ghostty](https://ghostty.org/) installed to try it out. I saw the same issues in both terminals, but interestingly enough, not in xterm. (I didn't realize the significance of that at the time.)

I also wanted to rule out interference from tmux. I [automatically load tmux in every terminal window](https://handyman5.github.io/posts/restore-terminal-contents-on-linux/) to preserve the terminal contents, so I tried disabling that functionality. No luck, still got the graphical corruption.

## Choosing the right test case, even by accident

Once I'd ruled all of those things out, I considered my test case. Was there something wrong with that specific file that was causing the trouble? I tried examining some other nearby files in the same repo, and noticed quickly that none of the other files in the module caused any sort of problems. It was all down to this one specific file. Why?

As it happens, the files in this module have a logging configuration that associates each file's work with an emoji to more easily disambiguate them while visually skimming log lines. Although all of the files had emoji, it was just this one test case file that caused problems. I decided to see if I could figure out what was different between the emojis used by a working file and those used by my broken test case. I selected each emoji in the terminal, copied it, and pasted it into the search box in [Emojipedia](https://emojipedia.org/). For the working files, I got an appropriate search result with the original emoji. For the broken file, however, I got nothing. I noticed that the URL looked like this:

![image](/images/broken-emojipedia-search.png)

_That's_ suspicious. What is that garbage at the end of the query? Searching for "efb88f unicode" took me right to [Unicode character 'VARIATION SELECTOR-16'](https://www.fileformat.info/info/unicode/char/fe0f/index.htm). I immediately went back to the broken file and arrowed around, and sure enough, there was an additional invisible cursor stop after each emoji. I removed and rewrote the relevant text with a fresh copy of the emoji, and with the variation selector removed, my graphical corruption problems went away.

## Diff hates unicode non-printable characters

I had one more thing to do, though. I needed to create a pull request with the changed file, and the PR diff looked like a no-op (since the removed character was non-printable). In order to make the case that I had actually changed something important, I used [this script](https://superuser.com/a/377805) to show the codepoints for each character and then diffed _that_ output before and after the fix:

```
$ diff -ub orig fixed
--- orig        2025-03-10 13:59:41.980971068 -0700
+++ fixed       2025-03-10 13:59:51.052771460 -0700
@@ -397,7 +397,6 @@
 U+0020
 U+0022 "
 U+1F986 🦆
-U+FE0F ️
 U+0022 "
 U+0029 )
 U+000A
```

And with that, I had found and fixed one of the weirdest problems I've ever had to troubleshoot.

## Postscript

Oh, you wanted me to pay off the foreshadowing of the significance of xterm not glitching? Although I never did realize it before figuring out the problem a different way, it's simply because xterm doesn't render emoji. If it can't show any emoji at all, it can't show a non-printable emoji that nevertheless breaks Emacs' screen rendering.
