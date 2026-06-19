---
title: How to Restore Terminal Contents on Linux (Yes, Like iTerm2)
slug: restore-terminal-contents-on-linux
date: 2023-06-22 12:00:00 UTC-07:00
tags: linux, howto
category: 
link: 
description: 
type: text
---

I recently switched to using a Linux desktop from a Mac as my primary work computer. I had grown quite accustomed to iTerm2’s session restoration feature, and I wanted something similar for Linux. Here is how I made it happen.

<!-- TEASER_END -->

![image](/images/1_WFHs5GplD-TWhhbK7qa_lQ.gif)

## Introducing tmux

[tmux](https://github.com/tmux/tmux/wiki), or “terminal multiplexer”, is designed to decouple the output of a terminal process (such as a shell or a terminal-based UI) from the window it happens to appear on. It allows you to attach multiple programs to a single window, to detach and run them in the background, and to reattach them later to view their output.

tmux is very configurable and has a strong community which has written many additional features in the form of tmux plugins. The two that are relevant to this story are [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) and [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum). tmux-resurrect can save and restore the state of a tmux session, and tmux-continuum triggers that save process continuously. There’s lots of documentation about setting up these plugins; see the READMEs in those repos for more.

My ~/.tmux.conf wound up looking like:

    set -g @plugin 'tmux-plugins/tpm'
    set -g @plugin 'tmux-plugins/tmux-resurrect'
    set -g @resurrect-capture-pane-contents 'on'
    set -g @continuum-restore 'on'
    set -g @continuum-save-interval '1'
    set -g @plugin 'tmux-plugins/tmux-continuum'

## iTerm2 capability

All of the documentation I could find was geared towards saving and restoring a single window, which is not what I wanted. I wanted all of my windows *and* tabs restored, with current directories and full scrollback. That took a little more work.

First, I set my terminal emulator’s startup command to:

    bash -c "(tmux ls | grep -vq attached && tmux at) || tmux"

This command lists the open tmux sessions, and either reattaches to an existing tmux session (if there are any that are detached) or starts a brand new one.

Then, I wrote this script and saved it as ~/bin/tmux-restoring.sh:

``` shell
    #!/bin/sh

    restoring=$(tmux ls | grep -v attached | wc -l)
    [ $restoring -gt 0 ] && echo "restoring"
```

It counts the number of tmux sessions that are detached and prints the word “restoring” if there’s more than zero of them. This lets me know that there’s saved sessions available after a restart if the terminal emulator does not automatically reopen all of the windows or tabs.

I added code to call this to my ~/.tmux.conf :

    set -g @theme-status-left-suffix ' #(~/bin/tmux-restoring.sh) '

(I am using [tmux-themepack](https://github.com/jimeh/tmux-themepack) to customize the status line, but this can be added with tmux set-option -ag status-left ‘ #(~/bin/tmux-restoring.sh)’ as well.)

You can see the result of this in the gif at the top of the page; it briefly shows restoring in the tmux status bar after the window is reopened.

## Final thoughts

This was more complex than I expected it to be, given that Mac users have had the luxury of this feature in iTerm2 for a long time. However, it’s nice to have it sorted in Linux finally.

## P.S. — tmux Control Mode

tmux has a special “[Control Mode](https://github.com/tmux/tmux/wiki/Control-Mode)” which allows for deep integration with a terminal emulator; in that mode, tmux sessions and windows are manipulated directly by the emulator instead of being represented by separate windows and tabs. I could not find a terminal emulator on Linux which supported this, but if one exists, that’d be an even nicer experience.
