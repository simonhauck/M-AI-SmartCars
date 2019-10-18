import logging

from flask import Flask

from car_service.car_service import CarService

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    car_service = CarService()


@app.route('/')
def hello_world():
    app.logger.info("Hello world called")
    return 'Hello World!'


@app.route('/vehicle', methods=['POST'])
def vehicle_tick():
    car_service.add_vehicle_tick(1)
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
