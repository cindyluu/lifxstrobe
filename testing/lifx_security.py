#!/usr/bin/env python

from lifxlan import *
import sys
from time import sleep


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

    original_colors = lifx.get_color_all_lights()
    original_powers = lifx.get_power_all_lights()

    print("Turning on all lights...")
    lifx.set_power_all_lights(True)
    sleep(1)

    # print("Toggling flashy color...")
    # toggle_light_color(lifx, 0.1)

    print("Strobe: Making it White...")
    lifx.set_color_all_lights(WHITE, 5000, True)

    sleep(3)

    print("Strobe: Toggling power...")
    toggle_device_power(lifx, 0.25, False, 10)


    print("Toggling flashy colors")
    toggle_light_color(lifx, 1, False, num_cycles=1)

    print("Toggling slow color")
    toggle_light_color(lifx, 1, smooth=True, num_cycles=1)
    lifx.set_power_all_lights("on", 2500, True)

    print("Restoring original color to all lights...")
    for light, color in original_colors:
        light.set_color(color)
    sleep(1)

    print("Restoring original power to all lights...")
    for light, power in original_powers:
        light.set_power(power)


def toggle_light_color(device, duration_secs=0.5, smooth=False, num_cycles=3):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    transition_time_ms = duration_secs*1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for i in range(num_cycles):
        for color in colors:
            device.set_color_all_lights(color, transition_time_ms, rapid)
            print(device.get_color())
            sleep(duration_secs)
            sleep(1)
    sleep(1)


def toggle_device_power(device, duration_secs=0.5, smooth=False, num_cycles=3): #TEST
    device.set_power_all_lights("off")
    transition_time_ms = duration_secs*1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for i in range(num_cycles):
        device.set_power_all_lights("on", transition_time_ms, rapid)
        sleep(duration_secs)
        device.set_power_all_lights("off", transition_time_ms, rapid)
        sleep(duration_secs)
    device.set_power_all_lights("on")


if __name__=="__main__":
    main()