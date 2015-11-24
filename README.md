# LIFX Strobe
### CS 5435: Security and Privacy in the Wild (Fall 2015)
### Cindy Luu, Anas Bouzoubaa, Sean Herman

The LIFX Strobe script scans the network for any connected LIFX smart bulbs, and passively logs the state of each in a loop. When the script detects a user attempting to control the bulb (e.g., change colors), the bulb new settings are briefly overriden with a new strobe command.

## Instructions

    pip install -r requirements.txt
    python bulbcontrol.py [NUM_BULBS]
