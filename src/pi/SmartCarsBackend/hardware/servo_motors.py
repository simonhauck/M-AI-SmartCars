import logging

import RPi.GPIO as GPIO
from flask import current_app as app

import hardware.utils as utils

log = logging.getLogger('servo_motors')


class ServoMotors:

    def __init__(self) -> None:
        """Initialize the servo motor pins with the specified values from the config"""
        self.servo_motor_pins = app.config['SERVO_MOTOR_PINS']
        self.max_pollution = app.config['MAX_POLLUTION']
        self.min_pollution = app.config['MIN_POLLUTION']
        self.initialized_pwm_pins = []

        GPIO.setmode(GPIO.BCM)

        for pin in self.servo_motor_pins:
            GPIO.setup(pin, GPIO.OUT)

            new_initialized_pin = GPIO.PWM(pin, 50)  # 50hz frequency
            new_initialized_pin.start(2.5)
            self.initialized_pwm_pins.append(new_initialized_pin)

        self.last_duty_cycle = 2.5

    def set_servo_motors(self, current_pollution_grade) -> None:
        """
        Set the servo motor positions according to the current pollution grade
        :param current_pollution_grade: the current absolute pollution grade
        :return: None
        """
        relative_pollution = utils.calculate_pollution_grade(current_pollution_grade,
                                                             180,  # the value in degrees
                                                             self.max_pollution,
                                                             self.min_pollution)

        duty_cycle = relative_pollution / 18 + 2.5
        if not duty_cycle == self.last_duty_cycle:
            self.last_duty_cycle = duty_cycle

            for pin in self.initialized_pwm_pins:
                pin.ChangeDutyCycle(duty_cycle)

            logging.debug("Duty cycle: {}".format(duty_cycle))
