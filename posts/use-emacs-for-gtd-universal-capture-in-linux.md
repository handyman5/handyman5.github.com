---
title: Use Emacs for GTD Universal Capture in Linux
slug: use-emacs-for-gtd-universal-capture-in-linux
date: 2023-03-16 12:00:00 UTC-07:00
tags: emacs, howto
category:
link:
description:
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx56ftt22"
---

![image](/images/1_Lnnoxld_wCdF0TfxCU_Ufg.webp)

I like having a system-wide keyboard shortcut that activates some form of text editor. That allows me to press the shortcut, type whatever I have in mind, navigate away from the editor, and get back to what I was doing. (This is sometimes called “universal capture” or “[ubiquitous capture](https://zenhabits.net/tips-for-gtds-ubiquitous-capture/)” in [GTD](https://gettingthingsdone.com/)-land.)

I’ve used lots of different programs to accomplish this over the years: NotationalVelocity/[nvALT](https://brettterpstra.com/projects/nvalt/), [SimpleNote](https://simplenote.com/), [Obsidian](https://obsidian.md/), just to name a few. However, I wanted to combine the quick access of universal capture with the editing power of Emacs. I spent some time recently setting up my Linux laptop to accomplish this.

<!-- TEASER_END -->

## A Script to Activate or Launch Emacs

The first thing I needed was a script to summon an Emacs frame. If a frame already exists, it should be brought forward; if it doesn’t already exist, one should be created and then brought forward.

Here’s what I wrote to accomplish this task:

``` bash
#!/bin/bash
candidate=$(xdotool search --name "GNU Emacs" | tail -1)
active=$(xdotool getwindowfocus)
if [[ $candidate -eq $active ]]; then
    xdotool windowminimize $candidate
    exit 0
fi
if [[ -z $candidate ]]; then
    emacsclient -c -n
    candidate=$(xdotool search --name "GNU Emacs" | tail -1)
fi
xdotool windowactivate $candidate
```

This uses xdotool to find the Emacs frame, if it exists, and also to get the ID of the currently active window. If no Emacs frame exists, emacsclient creates one and then xdotool windowactivate raises it. If an Emacs frame exists but is not the currently active window, xdotool windowactivate raises it. Finally, if a frame exists and *is *the currently active window, xdotool windowminimize hides it away. (This latter allows us to press the keyboard shortcut again to vanish the universal capture window and return focus to whatever was focused previously.)

## A Global Keyboard Short to Run It

The script isn’t much good if I have to open a terminal and type it in by hand every time, so I also set up a keyboard shortcut to execute it. These instructions are for KDE, but the same script should work for any Linux system.

1. Launch **System Settings** > **Custom Shortcuts**

1. Right-click on the left-hand side list and select **New** > **Global Shortcut** > **Command/URL**

1. Name the new shortcut, and for its “Trigger”, pick the keyboard shortcut of your choice. (I tend to use Alt+Shift+<key> since that’s not usually taken by most applications.)

1. For “Action”, point it to the script above as saved somewhere on your filesystem and made executable

## Closing Thoughts

I can’t overstate the usefulness of having a simple, system-wide keyboard shortcut that you can use to summon a text editor to write down whatever is currently distracting you. It will save you a lot of time and focus to get all of that out of your head and onto paper.
