import logging

import neopixel
from flask import current_app as app

import hardware.utils as utils

log = logging.getLogger('led_stripe')


class LedStripe:

    def __init__(self) -> None:

        self.pixels = neopixel.NeoPixel(app.config['LED_STRIPE_PIN'],
                                        app.config['LED_STRIPE_SIZE'],
                                        brightness=1,
                                        auto_write=False,
                                        pixel_order=app.config['LED_STRIPE_ORDER'])
        self.led_stripe_mode = app.config['LED_STRIPE_MODE']
        self.max_pollution = app.config['MAX_POLLUTION']
        self.min_pollution = app.config['MIN_POLLUTION']

    def set_led_stripe(self, current_pollution_grade):
        if self.led_stripe_mode == 1:
            self.__fade_lights(current_pollution_grade)
        # TODO Add other led stripe modes
        else:
            self.__fade_lights(current_pollution_grade)

    def __fade_lights(self, current_pollution_grade):
        relative_pollution = utils.calculate_pollution_grade(current_pollution_grade,
                                                             255,
                                                             self.max_pollution,
                                                             self.min_pollution)
        logging.info("Led Stripe Relative Pollution: {}".format(relative_pollution))
        self.pixels.fill((relative_pollution, 255 - relative_pollution, 0))
        self.pixels.show()
