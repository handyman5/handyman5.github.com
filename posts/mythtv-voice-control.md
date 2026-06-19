---
title: "New project: MythTV voice control"
slug: mythtv-voice-control
date: 2013-08-22 12:00:00 UTC-07:00
tags: mythtv
category: 
link:
description:
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx6fvkz2u"
---

_(originally from <https://web.archive.org/web/20161024021737/http://ajcsystems.com/blog/blog/2012/06/11/new-project-mythtv-voice-control/>)_

From the [README](https://github.com/handyman5/mythtv-vc):

> This script listens to a small set of voice commands in US English and translates them into instructions for a MythTV frontend. The intention is to emulate the voice control capabilities of an Xbox360 with a Kinect (e.g., you can say “Xbox pause” and it will cause the currently playing video to pause).

This post will detail some of the process I’ve gone through to get this working as far as it is, and what’s left to do.

<!-- TEASER_END -->

Initial idea
------------

My wife and I recently had a baby, so we find ourselves a) watching a lot of TV in the middle of the night, b) with our hands full. I’ve become a huge fan of the voice control capabilities of our Xbox360, and I wanted to add that functionality to my homebrew HTPC running MythTV.

Background: Sphinx / Pocketsphinx
---------------------------------

[CMU Sphinx](http://cmusphinx.sourceforge.net/) is an open-source toolkit for speech recognition. The project has several parts, but the one we’re concerned with here is called “Pocketsphinx”. It’s a programmable library that can take a variety of language models and use them to recognize speech patterns from audio data.

Building the listening daemon
-----------------------------

I started out by following the tutorial [Using PocketSphinx with GStreamer and Python](http://cmusphinx.sourceforge.net/wiki/gstreamer) and setting up the demo code it provides. I stripped out the GTK app part of it and replaced it with a `gobject.MainLoop()`, since I didn’t care about having a GUI interface. The pocketsphinx library requires two components, a language model and a dictionary; I used the [lmtool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) web-based utility provided by CMU to generate them for a small text corpus of simple voice commands (e.g. “tivo pause”). After adding some manual tweaks to the dictionary file to account for my personal speech patterns (such as the way I pronounce “pause”), I had a working recognizer.

Next step: controlling the MythTV frontend. This was actually pretty easy, thanks to the [MythTV python bindings](http://www.mythtv.org/wiki/Python_bindings#Frontend.28host.2C_port.29). I wired up a quick dispatch-table-ish structure to handle the different voice commands I wanted to use and their implementations in the MythTV API, and I was able to start controlling my MythTV HTPC with voice commands.

Echo cancellation
-----------------

When I started this project, I thought the hardest part would be getting the speech recognition working. Thanks to CMU Sphinx, that part has actually been fairly simple. The really hard part (which I’ve not yet solved) has been trying to get echo cancellation working on the MythTV audio output and the audio input of the listening daemon.

Some background on echo cancellation may be in order (since I didn’t know any of this when I started). When you use a speakerphone in a meeting, the voices of the people at the other end of the line that the speakerphone plays technically count as audio inputs to the microphones; and since the speakers are much closer to the mics on the device than the humans sitting around the table, the audio output can easily overwhelm the listening capability of the phone. This can cause feedback (ugly painful squealing noises), echo, poor sound quality, etc., and make it hard to have a conversation. Thus, speakerphones implement a class of algorithm called _echo cancellation_; these algorithms take the recently output audio stream into account as part of the input audio processing step, and attempt to remove those components to prevent rebroadcasting them to the other party (i.e. echo), feedback, and all the other bad consequences I mentioned.

The first iteration of the listening daemon had a lot of trouble operating while a TV show was playing. It would listen to the audio track of the show and attempt to parse that stream for voice commands; any actual voice commands I issued were lost in the noise (since the speaker output is much closer to the mic than I am and thus much louder). I solicited help on Twitter, and received some suggestions from [@louiswu](https://web.archive.org/web/20161024021737/http://twitter.com/#!/louiswu) about using Pulseaudio 2.0 and enabling both the “phone” media type and the “echo-cancel” filter on both the MythTV frontend and the listening daemon:

    PULSE_PROP="filter.want='echo-cancel' media.type='phone'" ./livefrontend.py


This improved the daemon’s recognition some, but not enough; it went from not understanding my commands at all while audio was playing to occasionally picking out a word or two, but still not getting a full command together. Arun further suggested I use the WebRTC echo-cancelling algorithm instead of the one that comes built-in with Pulseaudio 2.0, but I haven’t yet figured out either a) where to put the webrtc plugin files, or b) how to tell pulseaudio that there are some plugin files in a nonstandard location.

Other improvements
------------------

There are several other improvements I want to make to this tool:

*   Echo cancellation, obviously
*   Tweaking the voice recognition thresholds for loudness differential and fall-off time to better suit this use case (i.e., since commands are short, we should recognize a command almost immediately and stop trying to listen to the output audio stream for an extended period of time)
*   Adding more commands, such as more playback keys and jumping to different parts of the interface
*   Adding a more general-purpose audio processing language model. The current model is limited to just the small subset of commands I’ve trained it on, but I’d love to be able to issue searches for particular shows that haven’t been pre-trained (“tivo, play latest episode of ‘suits'”) instead of having to issue voice commands to poke around the on-screen menus and select an item.
*   Testing on a wider variety of platforms. I run [Mythbuntu](http://mythbuntu.org/), so that’s where I’ve tested, but I imagine this could be made to work on non-Debian-family Linuxes.
*   Using the latest version of pocketsphinx. The latest packaged version I can find is 0.5; 0.7 was released recently, so I’d love to roll in the improvements it has.
*   Hooking up an IR blaster to let me issue voice commands for other system components, e.g. “TV, power on” or “TV, input 2”
