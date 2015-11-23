#!/usr/bin/env python

from lifxlan import *
import sys


def main():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_lights()
    print("Found %d Bulbs" % len(devices))
    bulb = devices[0]

    original_power = bulb.get_power()
    original_color = bulb.get_color()
    print('Power=%s, Color=%s' % (original_power, original_color))
    print bulb
    print('Bulb info')
    print(bulb.get_info_tuple())


if __name__ == '__main__':
    main()
