#!/usr/bin/env python

import sys
import time
import logging
import lifxlan
from datetime import datetime, timedelta

LOG_NAME = 'bulb_control'
NANOSECONDS_PER_SECOND = 10 ** 9
MILLISECONDS_PER_SECOND = 1000

# create logger with 'spam_application'
logger = logging.getLogger(LOG_NAME)
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('%s.log' % LOG_NAME)
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def parse_args():
    if len(sys.argv) == 2:
        logger.debug('Number of bulbs: %s' % sys.argv[1])
        return int(sys.argv[1])
    return None


class BulbState:
    HSBK_HUE_INDEX = 0
    HSBK_SATURATION_INDEX = 1
    HSBK_BRIGHTNESS_INDEX = 2
    HSBK_KELVIN_INDEX = 3

    def __init__(self, hsbk, logger):
        # bulb.get_color() returns Hue Saturation Brightness Kelvin (HSBK) tuple
        self._logger = logger
        self._apply_state(hsbk)

    def _apply_state(self, hsbk):
        self._hue = hsbk[BulbState.HSBK_HUE_INDEX]
        self._saturation = hsbk[BulbState.HSBK_SATURATION_INDEX]
        self._brightness = hsbk[BulbState.HSBK_BRIGHTNESS_INDEX]
        self._kelvin = hsbk[BulbState.HSBK_KELVIN_INDEX]
        self._logger.debug('Applying HSBK %s -- %s' % (hsbk, self))

    def _is_state_changed(self, hsbk):
        return (self._hue != hsbk[BulbState.HSBK_HUE_INDEX] or
                self._saturation != hsbk[BulbState.HSBK_SATURATION_INDEX] or
                self._brightness != hsbk[BulbState.HSBK_BRIGHTNESS_INDEX] or
                self._kelvin != hsbk[BulbState.HSBK_KELVIN_INDEX])

    def process_new_state(self, new_hsbk, bulb):
        if (self._is_state_changed(new_hsbk)):
            self._logger.info('Bulb state changed: %s' % [v for v in new_hsbk])
            strobe_bulb(bulb)
            self._apply_state(new_hsbk)
            return

    def __str__(self):
        return ("Hue=%s Saturation=%s, Brightness=%s, Kelvin=%s"
                % (self._hue, self._saturation, self._brightness, self._kelvin))


class BulbMonitor:
    LOG_INTERVAL_MS = 1000

    def __init__(self, logger, log_interval_ms=LOG_INTERVAL_MS):
        self._last_log_time = None
        interval = log_interval_ms if log_interval_ms else BulbMonitor.LOG_INTERVAL_MS
        self._log_timedelta = timedelta(milliseconds=interval)
        self._logger = logger

    def should_log(self):
        if (self._last_log_time is None or (self._last_log_time + self._log_timedelta) < datetime.now()):
            return True
        return False

    def log_bulb(self, bulb, num=None):
        self._last_log_time = datetime.now()
        self._logger.info("Bulb state: %s" % self._get_bulb_meta(bulb))

    def _get_bulb_meta(self, bulb):
        bulb_info = bulb.get_info_tuple()
        uptime_seconds = bulb_info[1] / NANOSECONDS_PER_SECOND
        downtime_seconds = bulb_info[2] / NANOSECONDS_PER_SECOND
        return ('Color=%s, Power=%s, Uptime=%s seconds, Downtime=%s seconds'
                % (bulb.get_color(), bulb.get_power(), uptime_seconds,
                   downtime_seconds))


def strobe_bulb(bulb, num_strobes=10):
    logger.info('Beginning bulb strobe')
    original_color = bulb.get_color()
    original_power = bulb.get_power()
    bulb.set_color(lifxlan.WHITE, 0.5, True)

    for i in xrange(num_strobes):
        bulb.set_power("off", 0.0001, False)
        time.sleep(0.0000001)
        bulb.set_power("on", 0.0001, False)
    logger.info('Finished bulb strobe')

    logger.info('Restoring original bulb state')
    bulb.set_color(original_color)
    bulb.set_power(original_power)


def run_bulb_controller(devices, bulb_states, monitor):
    # Check for state changes for all discovered bulbs
    for i, bulb in enumerate(devices):
        bulb_state = bulb_states[i]
        bulb_state.process_new_state(bulb.get_color(), bulb)

    # Log state for bulbs
    if monitor.should_log():
        for i, bulb in enumerate(devices):
            monitor.log_bulb(bulb)

    time.sleep(0.1)


def main():
    num_bulbs = parse_args()

    logger.info('Searching for bulbs on network')
    lifx = lifxlan.LifxLAN(num_bulbs)

    devices = lifx.get_lights()
    logger.info("Found %d Bulbs" % len(devices))

    monitor = BulbMonitor(logger, 2 * MILLISECONDS_PER_SECOND)
    bulb_states = []
    for i, bulb in enumerate(devices):
        bulb_states.append(BulbState(bulb.get_color(), logger))

    while(1):
        run_bulb_controller(devices, bulb_states, monitor)


if __name__ == '__main__':
    main()
