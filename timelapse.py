#!/usr/bin/env python

import os
import datetime
import time
from subprocess import Popen, PIPE

# For easier datetimes.
import arrow
# For sunrise / sunset data
from astral import Astral


def start(city_name="Los Angeles", folder="images"):
    dawn, dusk = get_interesting_times(city_name)
    delay = get_timelapse_delay(dawn, dusk)
    tzinfo = dawn.tzinfo

    if not os.path.exists(folder):
        os.makedirs(folder)

    shot = 0
    while arrow.now(tzinfo) < dusk:
        raw_time = arrow.now(tzinfo)
        formatted_time = raw_time.format("YYYY-MM-DD_HH:mm:ss")
        print("Taking picture {0} at {1}".format(shot, formatted_time))
        filename = "timelapse_{0}.jpg".format(formatted_time)
        imgpath = os.path.join(folder, filename)
        take_picture(imgpath)
        shot += 1
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

    hours, minutes, seconds = total_runtime.split(":")

    print "Time until Dusk: %s" % time_til_dusk
    total_seconds = time_til_dusk.total_seconds()
    frame_delay = float(total_seconds) / (int(seconds) * fps)
    print "Delay: %s" % frame_delay
    return frame_delay


def take_picture(filename):
    """Use gphoto2 to interact with our camera and take the picture."""
    print filename
    process = Popen([
        "/usr/local/bin/gphoto2", "--capture-image-and-download",
        "--filename", filename
        ], stdout=PIPE, stderr=PIPE
    )
    output = process.communicate()
    print "Result:", output


if __name__ == "__main__":
    # Run this as soon as we load.
    start()

