import logging

from flask import current_app

from model.pollution_log import PollutionLog
from model.vehicle import Vehicle

log = logging.getLogger('car_service')


class CarService:

    def __init__(self) -> None:
        self.pollution_log = PollutionLog()

        # self.available_vehicles = vehicle_list
        self.available_vehicles = current_app.config['AVAILABLE_VEHICLES']

    def add_vehicle_tick(self, vehicle_id: int):
        log.info("Add vehicle tick for id {}".format(vehicle_id))
        log.debug("Search for vehicle...")

        vehicle = self.get_vehicle_by_id(vehicle_id)
        log.debug("Found: {}".format(vehicle))

    # TODO not working properly
    def get_vehicle_by_id(self, id_: int) -> Vehicle:
        selected_vehicle = filter(lambda vehicle: vehicle.id_ == id_, self.available_vehicles)
        return selected_vehicle
