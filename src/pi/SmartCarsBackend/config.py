import board
import neopixel

from model.vehicle import Vehicle


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "it worked"
    AVAILABLE_VEHICLES = [
        Vehicle(id_=1, name='Car', radius_wheel=2.0, amount_magnets=1, pollution_per_cm=5),
        Vehicle(id_=2, name='Bus', radius_wheel=2.0, amount_magnets=1, pollution_per_cm=3)
    ]

    POLLUTION_LOG_DELAY = 10

    # Pollution Min Max Values
    MIN_POLLUTION = 100
    MAX_POLLUTION = 1000

    # Hardware
    HARDWARE_LOOP_SLEEP = 0.1
    LED_STRIPE_PIN = board.D18
    LED_STRIPE_ORDER = neopixel.GRB
    LED_STRIPE_SIZE = 60
    LED_STRIPE_MODE = 0
    SERVO_MOTOR_PINS = [26, 19, 13, 6]


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
