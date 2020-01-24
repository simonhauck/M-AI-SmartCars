import logging

import neopixel
from flask import current_app as app

import hardware.utils as utils

log = logging.getLogger('led_stripe')


class LedStripe:

    def __init__(self) -> None:
        """Init the led stripe module with the values specified in the config
        """
        self.pixels = neopixel.NeoPixel(app.config['LED_STRIPE_PIN'],
                                        app.config['LED_STRIPE_SIZE'],
                                        brightness=1,
                                        auto_write=False,
                                        pixel_order=app.config['LED_STRIPE_ORDER'])
        self.led_stripe_mode = app.config['LED_STRIPE_MODE']
        self.led_stripe_size = app.config['LED_STRIPE_SIZE']
        self.led_stripe_center_right = app.config['LED_STRIPE_CENTER_LED_RIGHT']
        self.max_pollution = app.config['MAX_POLLUTION']
        self.min_pollution = app.config['MIN_POLLUTION']

    def set_led_stripe(self, current_pollution_grade) -> None:
        """
        Set the color of the led stripe depending ont he pollution grade.
        The led display style depends on the selected style specified int he config
        :param current_pollution_grade: the current absolute pollution grade
        :return: None
        """
        if self.led_stripe_mode == 0:
            self.__fade_lights(current_pollution_grade)
        elif self.led_stripe_mode == 1:
            self.__mixed_lights(current_pollution_grade)
        # TODO Add other led stripe modes
        else:
            self.__fade_lights(current_pollution_grade)

    def __fade_lights(self, current_pollution_grade) -> None:
        """
        Fade the lights depending on the current pollution grade.
        Depending on the pollution the led stripe will loose the green value and get more red value
        :param current_pollution_grade: the current absolute pollution grade
        :return None
        """
        relative_pollution = utils.calculate_pollution_grade(current_pollution_grade,
                                                             255,
                                                             self.max_pollution,
                                                             self.min_pollution)
        # logging.info("Led Stripe Relative Pollution: {}".format(relative_pollution))
        self.pixels.fill((relative_pollution, 255 - relative_pollution, 0))
        self.pixels.show()

    def __mixed_lights(self, current_pollution_grade) -> None:
        """
        Mixed mode for the led stripe. Corresponding to the relative pollution the leds will turn red.
        The leds that will not turn red will fade to red according to the relative pollution (This is because green is
        mich more dominant and will not drastically.
        :param current_pollution_grade: the current pollution
        :return: None
        """
        # Relative pollution with half the amount of led's that will turn red
        relative_pollution_switch = utils.calculate_pollution_grade(current_pollution_grade,
                                                                    self.led_stripe_size / 2,
                                                                    self.max_pollution,
                                                                    self.min_pollution)

        # Relative pollution to fade the remaining led's
        relative_pollution_fade = utils.calculate_pollution_grade(current_pollution_grade,
                                                                  255,
                                                                  self.max_pollution,
                                                                  self.min_pollution)

        for i in range(30):
            if relative_pollution_switch <= i:
                # Fade Led between red and green
                color = (relative_pollution_switch, 255 - relative_pollution_fade, 0)
            else:
                # Set led to red
                color = (255, 0, 0)

            # Set always two led on the left and right side
            self.pixels[(self.led_stripe_center_right + i) % 60] = color
            self.pixels[(self.led_stripe_center_right - 1 - i) % 60] = color
            self.pixels.show()
