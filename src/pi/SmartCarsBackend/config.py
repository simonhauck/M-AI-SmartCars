from model.vehicle import Vehicle


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "it worked"
    AVAILABLE_VEHICLES = [
        # {'id': 1, 'name': 'Car', 'radius_wheel': 2.0, 'amount_magnets': 1, 'pollution_per_cm': 5.0},
        # {'id': 1, 'name': 'Bus', 'radius_wheel': 2.0, 'amount_magnets': 1, 'pollution_per_cm': 5.0},
        Vehicle(id_=1, name='Car', radius_wheel=2.0, amount_magnets=1, pollution_per_cm=5),
        Vehicle(id_=2, name='Bus', radius_wheel=2.0, amount_magnets=1, pollution_per_cm=3)
    ]

    HARDWARE_LOOP_SLEEP = 0.1




class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
