import math


class Vehicle(object):

    def __init__(self, id_: int, name: str, radius_wheel: float, amount_magnets: int, pollution_per_cm: float) -> None:
        """
        Create a vehicle with the given specifications
        :param id_: the unique identifier of the vehicle
        :param name the name of the vehicle
        :param radius_wheel: the radius of the wheels from vehicle
        :param amount_magnets: the amount of magnets. 2 magnets mean that only half of the size of the wheel has passed
        :param pollution_per_cm: the pollution values per centimeter
        """
        self.id_ = id_
        self.name = name
        self.radius_wheel = radius_wheel
        self.amount_magnets = amount_magnets
        self.pollution_per_cm = pollution_per_cm

    def calculate_pollution(self, ticks: int = 1) -> float:
        """
        Calculate the pollution for the given amount of ticks of the sensor
        :return: the calculated pollution value
        """
        wheel_circumference = math.pi * 2 * self.radius_wheel
        travelled_distance_per_tick = wheel_circumference / self.amount_magnets
        pollution = travelled_distance_per_tick * self.pollution_per_cm * ticks
        return pollution
