import logging
from flask import current_app
import board
import neopixel

log = logging.getLogger('led_stripe')


class LedStripe:

    def __init__(self, led_stripe_pin: board.pin, led_stripe_size: int, pixel_order: neopixel) -> None:
        self.pixels = neopixel.NeoPixel(led_stripe_pin, led_stripe_size, brightness=1, auto_write=False,
                                        pixel_order=pixel_order)
