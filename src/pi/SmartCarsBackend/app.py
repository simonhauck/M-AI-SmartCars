import logging
import threading
import json
from time import sleep

from flask import Flask, request

from car_service.vehicle_service import VehicleService

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    car_service = VehicleService()


def loop() -> None:
    """Specifies the functionality that should be run in a loop"""

    # Clean the log with a thread lock
    thread_lock = threading.Lock()

    thread_lock.acquire()
    car_service.clean_log()
    thread_lock.release()

    current_pollution = car_service.sum_pollution()
    total_amount_entries = car_service.total_amount_entries_log()
    # app.logger.debug("Total Amount Entries: {}, Current Pollution: {}".format(total_amount_entries, current_pollution))

    # TODO Add hardware and clean log
    # app.logger.info("Add here hardware functionality")


@app.before_first_request
def activate_job():
    """Start a thread to run the loop function every x seconds. The delay can be specified with the config file"""
    sleep_time = app.config['HARDWARE_LOOP_SLEEP']
    app.logger.info("Hardware loop sleep time is {} second(s)".format(sleep_time))

    def run_job():
        while True:
            loop()
            sleep(0.1)

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def hello_world():
    app.logger.info("Hello world called")
    return 'Hello World!'


@app.route('/vehicle', methods=['POST'])
def vehicle_tick():
    json_body = request.json
    vehicle_id = json_body.get('id', 1)
    amount_ticks = json_body.get('th', 1)
    app.logger.debug("Vehicle Tick Body: id={}, ticks={}".format(vehicle_id, amount_ticks))
    car_service.add_vehicle_tick(vehicle_id=vehicle_id, amount_ticks=amount_ticks)
    return "", 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    app.logger.info("App finished")
