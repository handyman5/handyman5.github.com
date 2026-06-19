---
title: How I reinstalled Windows 10 on a Surface Go
slug: reinstall-windows-10-surface-go
date: 2020-06-03 12:00:00 UTC-07:00
tags: howto, windows
category: 
link: 
description: 
type: text
---

I purchased a Microsoft Surface Go recently. The other day, it blue-screened and refused to start up again (cycling through the “Automatic Repair” screen and failing repeatedly). I write this as a reference for myself for how to fix this if it happens again, and also to explain some of the dead ends I encountered along the way.

<!-- TEASER_END -->

## First Obstacle

I first tried using the built-in recovery environment to “reset” and “recover” the operating system. Neither worked and neither told me why not, so I decided to go with a clean reinstall. That led me to the first problem: how to make a Windows 10 USB boot disk. Microsoft has a built-in “[Recovery Media Creator](https://support.microsoft.com/en-us/help/15088/windows-10-create-installation-media)”, but that only works if you have a working Windows machine and all I had to hand was a Mac. After lots and lots of false starts, I found [these instructions](https://www.freecodecamp.org/news/how-make-a-windows-10-usb-using-your-mac-build-a-bootable-iso-from-your-macs-terminal/) that walked me through downloading a Windows 10 64-bit ISO, formatting the USB disk as GPT:FAT32, and copying the ISO files over (including the step where I had to split one of the files that was larger than 4 GB so it’d fit on a FAT32 filesystem). At the end of those instructions, I had a bootable USB disk that I could use to install Windows 10… or so I thought.

## Second Obstacle

Booting the Surface Go from the USB boot disk was easy; the computer was configured to check USB first, so it flowed cleanly into the install. However, that failed too. The closest description of what I ran into was in [this TechNet post](https://social.technet.microsoft.com/Forums/windowsserver/en-US/3ce7e9fa-e308-42bd-97e7-daca836daf27/unattented-install-on-hp-gen9-fail-in-bfs?forum=winserver8setup). As far as I understand it, the installer was able to set up partitions appropriately on the internal drive, but when it moved on to the next step, it thought it was trying to install Windows *on the USB boot disk*, and (reasonably) refused to do so. This stymied me for a couple of days, but eventually I stumbled on [this article](https://neosmart.net/wiki/setup-was-unable-to-create-a-new-system-partition/#Fix_1_Eject_and_re-insert_the_USB) which laid out a complex choreography of stepping through the install, letting it fail, removing the USB boot disk entirely, retracing part of the install and letting it fail again, reinserting the USB boot disk, and then restarting the install *again* in a context that would allow it to proceed. Fortunately, that all worked as described, and the install completed successfully.

## What Didn’t Work

The narrative above makes it seem like this was a straightforward process, but it was nothing of the sort. Here are some of the things I tried that didn’t work.

* **Using a standard bootable-USB creation tool.** I generally use [balenaEtcher](https://www.balena.io/etcher/) for this task, but it failed here (likely because of the file that was larger than 4 GB).

* **Creating a USB drive partitioned with MBR.** One of the suggestions I ran into was using MBR instead of GPT to partition the USB boot disk, but the Surface Go refused entirely to boot from that because it’s a UEFI computer. (I learned *so many new things* these past few days.)

* **Using Rufus to create a NTFS-formatted USB boot disk.** I ran into several recommendations like [this one](https://www.windowscentral.com/how-create-windows-10-usb-bootable-media-uefi-support) that suggested the tool [Rufus](https://rufus.ie/) would allow me to format the USB boot disk with NTFS instead of FAT32, and that that might un-confuse the Windows installer. I made such a disk (after setting up a virtualized Windows machine with [VirtualBox](https://www.virtualbox.org/)), but the Surface Go initially refused to boot from it until I [disabled Secure Boot](https://github.com/pbatard/rufus/wiki/FAQ#Why_do_I_need_to_disable_Secure_Boot_to_use_UEFINTFS), and even afterward the installer claimed it was unable to find a valid disk to install to at all.

* **Using a DVD drive.** The bug occurs when installing from a USB boot disk because it’s seen as a potential install destination. Theoretically, installing from a DVD would get around this problem. However, the Windows 10 setup ISO is ~5 GB in size, so it would only fit on a dual-layer DVD and I didn’t have any in the house; and I couldn’t think of an essential retailer that would sell me one and didn’t want to wait several days to buy one online.

* **Copying the Windows installer to a partition on the drive.** I found several instances of [guidance](https://neosmart.net/wiki/setup-was-unable-to-create-a-new-system-partition/#Fix_2_Manually_create_the_boot_partition) to copy the USB boot disk’s contents to a bootable partition on the target hard drive, start the installation from there, partition around the installer, and then go back later and erase the installer partition. None of these worked because they were all written to use MBR partitions, which the Surface Go refused to boot from; and I was not able to figure out how to create a bootable GPT partition (bcdedit was giving me all sorts of static at this point).

## Conclusion

This was a hundred thousand times harder than it should have been, and anyone who isn’t both a) an experienced IT tech and b) unwilling to quit trying new things to fix it would have been profoundly fucked. Buying a Surface Go was a poor decision and if this happens again I’m going to drop-kick it and buy a Chromebook.
