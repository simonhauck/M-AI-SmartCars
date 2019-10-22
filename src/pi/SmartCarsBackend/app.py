import logging
import threading
from time import sleep

from flask import Flask

from car_service.vehicle_service import VehicleService

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    car_service = VehicleService()


def loop() -> None:
    """Specifies the functionality that should be run in a loop"""
    # TODO Add hardware and clean log
    app.logger.info("Add here hardware functionality")


@app.before_first_request
def activate_job():
    """Start a thread to run the loop function every x seconds. The delay can be specified with the config file"""
    sleep_time = app.config['HARDWARE_LOOP_SLEEP']
    app.logger.info("Hardware loop sleep time is {} second(s)".format(sleep_time))

    def run_job():
        while True:
            app.logger.debug("Calling Hardware loop")
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
    car_service.add_vehicle_tick(1)
    return "", 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    app.logger.info("App finished")
