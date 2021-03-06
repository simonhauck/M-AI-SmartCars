import logging
import time
from typing import Optional

from flask import current_app

from model.pollution_log import PollutionLog, PollutionEntry
from model.vehicle import Vehicle

log = logging.getLogger('car_service')


class VehicleService:

    def __init__(self) -> None:
        pollution_log_delay = current_app.config['POLLUTION_LOG_DELAY']
        self.pollution_log = PollutionLog(pollution_log_delay)

        # self.available_vehicles = vehicle_list
        self.available_vehicles = current_app.config['AVAILABLE_VEHICLES']

    def add_vehicle_tick(self, vehicle_id: int, amount_ticks: int = 1):
        log.info("Add vehicle tick for id {}".format(vehicle_id))
        log.debug("Search for vehicle...")

        vehicle = self.get_vehicle_by_id(vehicle_id)

        # If vehicle is not existing,
        if vehicle is None:
            log.debug("Vehicle not found for id: {}".format(vehicle_id))
            return

        log.debug("Vehicle found: {}".format(vehicle))

        timestamp = time.time()
        pollution = vehicle.calculate_pollution(amount_ticks)
        log.debug("Calculated pollution: {}, TimeStamp: {}".format(pollution, timestamp))

        pollution_entry = PollutionEntry(pollution=pollution, timestamp=timestamp)
        self.pollution_log.add_entry(pollution_entry)
        log.debug("Pollution log contains {} element(s)".format(self.pollution_log.get_size()))

    def get_vehicle_by_id(self, id_: int) -> Optional[Vehicle]:
        """
        Get a vehicle by its id from the available vehicles list.
        :param id_: the id of the vehicle
        :return: the vehicle or None if not found
        """
        for vehicle in self.available_vehicles:
            if vehicle.id_ == id_:
                return vehicle
        return None

    def clean_log(self) -> None:
        """Clean the pollution log"""
        self.pollution_log.clean_list()

    def sum_pollution(self) -> float:
        """
        Calculate the sum of the pollution
        :return: the sum of the pollution
        """
        return self.pollution_log.sum_pollution()

    def total_amount_entries_log(self) -> int:
        """
        :return: the total amount of entries in the pollution log
        """
        return self.pollution_log.total_amount
