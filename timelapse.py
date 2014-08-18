#!/usr/bin/env python

import datetime
import time
from astral import Astral
from sh import gphoto2


def start(city_name="Los Angeles"):
    dawn, dusk = get_interesting_times(city_name)
    delay = get_timelapse_delay(dawn, dusk)
    tzinfo = dawn.tzinfo

    while datetime.datetime.now(tzinfo) < dusk:
        print "Taking picture at %s" % datetime.datetime.now(tzinfo)
        take_picture()
        time.sleep(delay)


def get_interesting_times(city_name):
    """Determine the times that the sun will rise and set for locale."""
    astral = Astral()
    city = astral[city_name]

    # Get time that the sun will rise / set.
    sun = city.sun(date=datetime.date.today(), local=True)
    dawn = sun['dawn']
    dusk = sun['dusk']
    tzinfo = dawn.tzinfo
    print "Dawn: %s" % dawn
    print "Dusk: %s" % dusk
    print "Now: %s" % datetime.datetime.now(tzinfo)
    return dawn, dusk


def get_timelapse_delay(dawn, dusk, total_runtime="00:00:06", fps=24):
    """Figure out how long we should delay between shooting frames.

    Returns a delay in float.
    """
    # The times from Astral are a day ahead, even though we explicitly set it.
    time_til_dusk = dusk - datetime.datetime.now(dusk.tzinfo)
    time_til_dusk -= datetime.timedelta(days=1)

    hours, minutes, seconds = total_runtime.split(":")

    print "Time until Dusk: %s" % time_til_dusk
    total_seconds = time_til_dusk.total_seconds()
    frame_delay = float(total_seconds) / (int(seconds) * fps)
    print "Delay: %s" % frame_delay
    return frame_delay


def take_picture():
    """Use gphoto2 to interact with our camera and take the picture."""
    output = gphoto2("--capture-image-and-download")
    print "Result: %s" % output


if __name__ == "__main__":
    # Run this as soon as we load.
    start()

