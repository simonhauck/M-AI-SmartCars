import logging
import RPi.GPIO as GPIO

from flask import current_app as app

import hardware.utils as utils

log = logging.getLogger('servo_motors')


class ServoMotors:

    def __init__(self) -> None:
        self.servo_motor_pin = app.config['SERVO_MOTOR_PIN']
        self.max_pollution = app.config['MAX_POLLUTION']
        self.min_pollution = app.config['MIN_POLLUTION']

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_motor_pin, GPIO.OUT)

        self.pin = GPIO.PWM(self.servo_motor_pin, 50)  # 50hz frequency

        self.last_duty_cycle = 2.5
        self.pin.start(2.5)



    def set_servo_motors(self, current_pollution_grade):
        relative_pollution = utils.calculate_pollution_grade(current_pollution_grade,
                                                             180,
                                                             self.max_pollution,
                                                             self.min_pollution)

        duty_cycle = relative_pollution / 18 + 2.5
        if not duty_cycle == self.last_duty_cycle:
            self.last_duty_cycle = duty_cycle
            self.pin.ChangeDutyCycle(duty_cycle)
            logging.info("Duty cycle: {}".format(duty_cycle))
