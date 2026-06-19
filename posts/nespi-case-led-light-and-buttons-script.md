---
title: NESPi Case LED Light and Buttons Script
date: 2026-06-14
author: Adam Compton
categories: [howto]
tags: [emulation]
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3moho6hmy5y2b"
description: I have a NESPi Case for my RetroPie emulation console. It has a little red LED light on the front and I wanted it to work.
reading_time: 10
---

I have a [NESPi Case](https://retroflag.com/nespi-case-plus.html) for my [RetroPie](https://retropie.org.uk/) emulation console. It has a little red LED light on the front and I wanted it to work. However, after I installed [Lakka](https://www.lakka.tv/) (which is great in all other respects), I couldn't figure out how.

I spent some time figuring it out, and now you get to reap the benefits of my investigation.
<!-- TEASER_END -->

## Setup

First things first, I should list what hardware I'm using so you have an idea of whether this might be relevant for you.

* **Board**: Raspberry Pi 3 Model B Plus Rev 1.3
* **Case**: [NESPi Case Plus](https://retroflag.com/nespi-case-plus.html)
* **OS**: [Lakka](https://www.lakka.tv/), a Linux distribution that packages [RetroArch](https://www.retroarch.com/) and basically nothing else

The case has a red LED light and `Power` and `Reset` buttons, along with a GPIO header for the Raspberry Pi that connects them. The case manufacturers have [a repo](https://github.com/RetroFlag/retroflag-picase) that includes a script to read those headers and do useful things (reboot when the buttons are pressed, turn on the light, etc.). I wanted the red light to turn on while the machine is running, because of course.

## Investigation

Unfortunately, that script is not designed to work on Lakka, which (as I mentioned before) does not include many of the niceties of a modern Linux distribution like a package manager.

Someone put together [a version of the script](https://github.com/marcelonovaes/lakka_nespi_power) that _is_ supposed to work on Lakka, but it hasn't been touched in 8 years and it didn't work on my machine when I tried:

```bash
Lakka:~ # python /storage/scripts/shutdown.py
Traceback (most recent call last):
  File "/storage/scripts/shutdown.py", line 3, in <module>
    import RPi.GPIO as GPIO
ImportError: /storage/lib/RPi/GPIO.so: wrong ELF class: ELFCLASS32
```

The repo includes a precompiled version of the GPIO library that doesn't work with the current version of the kernel (Lakka [switched to aarch64 in 2021](https://www.lakka.tv/articles/2021/05/22/lakka-3.0/), which postdates this repo), and there aren't any trivial ways to get a new version cross-compiled and uploaded. But, luckily for us, Lakka started including the `python-raspberry-gpio` package [in 2021](https://github.com/libretro/Lakka-LibreELEC/issues/1227), which installs the [lgpio python package](https://pypi.org/project/lgpio/) ([relevant package docs](https://abyz.me.uk/lg/py_lgpio.html)). This is not a drop-in replacement for the `RPi.GPIO` library (which is what the precompiled binary includes); if you do need such a replacement, apparently [rpi-lgpio](https://pypi.org/project/rpi-lgpio/) will do the trick. But as I mentioned, Lakka does not have a package installation mechanism (including `pip`), so I had to rewrite the manufacturers' script to use `lgpio` instead of `RPi.GPIO`.

## Script

To save you all the trouble, here's the new script:

<details>
<summary>said script</summary>
```python
#!/usr/bin/env python3

import lgpio
import time
import os
import signal
import sys

# =====================
# Pin definitions (BCM)
# =====================
powerPin   = 3
resetPin   = 2
ledPin     = 14
powerenPin = 4

GPIOCHIP = 0
DEBOUNCE_US = 200_000  # 200 ms

chip = None

# =====================
# Cleanup
# =====================
def cleanup(signum=None, frame=None):
    global chip
    try:
        if chip is not None:
            lgpio.gpio_write(chip, ledPin, 0)  # LED off on exit
            lgpio.gpiochip_close(chip)
    finally:
        sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# =====================
# Main
# =====================
def main():
    global chip

    chip = lgpio.gpiochip_open(GPIOCHIP)

    # Power enable (always HIGH)
    lgpio.gpio_claim_output(chip, powerenPin, 1)

    # LED output — ON at startup
    lgpio.gpio_claim_output(chip, ledPin, 1)

    # Inputs with pull-ups
    lgpio.gpio_claim_input(chip, powerPin, lgpio.SET_PULL_UP)
    lgpio.gpio_claim_input(chip, resetPin, lgpio.SET_PULL_UP)

    # Debounce
    lgpio.gpio_set_debounce_micros(chip, powerPin, DEBOUNCE_US)
    lgpio.gpio_set_debounce_micros(chip, resetPin, DEBOUNCE_US)

    print("NESPi shutdown controller running (LED ON)")

    last_power = lgpio.gpio_read(chip, powerPin)
    last_reset = lgpio.gpio_read(chip, resetPin)

    while True:
        time.sleep(0.01)

        # ---- Power button ----
        power = lgpio.gpio_read(chip, powerPin)
        if power == 0 and last_power == 1:
            # Blink LED while held
            while lgpio.gpio_read(chip, powerPin) == 0:
                lgpio.gpio_write(chip, ledPin, 0)
                time.sleep(0.2)
                lgpio.gpio_write(chip, ledPin, 1)
                time.sleep(0.2)

            # Ensure LED returns to ON state
            lgpio.gpio_write(chip, ledPin, 1)

            os.system("shutdown -h now")

        last_power = power

        # ---- Reset button ----
        reset = lgpio.gpio_read(chip, resetPin)
        if reset == 0 and last_reset == 1:
            os.system("shutdown -r now")

        last_reset = reset

if __name__ == "__main__":
    main()
```
</details>

This enables the power LED and also the button functionality (which I don't ever use, but while I was in the neighborhood).

## Installation

I put the new script in `/storage/scripts/shutdown.py` like the old Lakka-installing repo's [installation script](https://github.com/marcelonovaes/lakka_nespi_power/blob/master/install.sh) did. That script also adds a line to `/storage/.config/autostart.sh` which is Lakka's mechanism for [automatically starting programs on boot](https://wiki.libreelec.tv/configuration/startup-shutdown#autostart.sh). The only change I had to make was to have the autostart bit `cd` to `/tmp` before running the new python script, because otherwise I was getting weird permissions errors:

```yaml
Jan 04 18:10:55 Lakka systemd[1]: retroarch-autostart.service: Deactivated successfully.
Jan 04 18:10:55 Lakka systemd[1]: Stopped retroarch-autostart.service.
Jan 04 18:10:55 Lakka systemd[1]: Starting retroarch-autostart.service...
Jan 04 18:10:55 Lakka systemd[1]: Finished retroarch-autostart.service.
Jan 04 18:10:55 Lakka sh[1158]: 2026-01-04 18:10:55 xCreatePipe: Can't set permissions (436) for //.lgd-nfy0, No such file or directory
Jan 04 18:10:55 Lakka sh[1158]: Traceback (most recent call last):
Jan 04 18:10:55 Lakka sh[1158]:   File "/storage/scripts/shutdown_lgpio.py", line 3, in <module>
Jan 04 18:10:55 Lakka sh[1158]:     import lgpio
Jan 04 18:10:55 Lakka sh[1158]:   File "/usr/lib/python3.11/site-packages/lgpio.py", line 562, in <module>
Jan 04 18:10:55 Lakka sh[1158]:   File "/usr/lib/python3.11/site-packages/lgpio.py", line 504, in __init__
Jan 04 18:10:55 Lakka sh[1158]: FileNotFoundError: [Errno 2] No such file or directory: '.lgd-nfy-3'
```

Running the script from a working directory where it has proper permissions did the trick.

## Wrapup

This was a fun evening's investigation and hopefully it'll prove useful to somebody someday. Good luck and happy emulating!
