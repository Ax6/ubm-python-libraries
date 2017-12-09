from numpy import *
from Acquisition.Dataset import IMU
from Acquisition.Dataset import Vehicle
from Acquisition.Dataset import Driver
from Acquisition.Dataset import Internal


class Dataset:
    F_SAMPLING = 100

    def __init__(self, data):
        self.original_data = data
        NameCompatibility().fix(self)
        self.start_time = 0
        self.end_time = self._get_duration()
        """
        The order is IMU -> Vehicle -> Driver -> Internal
        Important as they have dependencies
        """
        self.accelerometer = IMU.Accelerometer(self)
        self.gyroscope = IMU.Gyroscope(self)
        self.speed = Vehicle.Speed(self)
        self.dampers = Vehicle.Dampers(self)
        self.ride_height = Vehicle.RideHeight(self)
        self.steering_angle = Driver.SteeringAngle(self)
        self.brakes = Driver.Brakes(self)
        self.throttle = Driver.Throttle(self)
        self.temperatures = Internal.Temperatures(self)

    def init(self):
        self.gyroscope.calibrate()
        self.steering_angle.calibrate()

    def get_original_data(self):
        return self.original_data

    def get_data(self):
        data_interval = self._get_data_interval()
        return self.original_data[:][data_interval[0]:data_interval[1]]

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time

    def get_time_axis(self):
        time_interval = self._get_time_interval()
        return arange(time_interval[0], time_interval[1] - time_interval[0] - 1 / self.F_SAMPLING, 1 / self.F_SAMPLING)

    def get_accelerometer(self):
        return self.accelerometer

    def get_gyroscope(self):
        return self.gyroscope

    def get_speed(self):
        return self.speed.get()

    def get_dampers(self):
        return self.dampers

    def get_ride_height(self):
        return self.ride_height

    def get_steering_angle(self):
        return self.steering_angle.get()

    def get_brakes(self):
        return self.brakes

    def get_throttle(self):
        return self.throttle.get()

    def get_temperatures(self):
        return self.temperatures

    def _get_data_interval(self):
        return [int(i * self.F_SAMPLING + 1) for i in self._get_time_interval()]

    def _get_time_interval(self):
        return [self.start_time, self.end_time]

    def _get_duration(self):
        return len(self.original_data) / self.F_SAMPLING


class NameCompatibility:
    """
    Another Luke pearl
    """

    # Right: Wrong
    COMPATIBILITY_DICTIONARY = [
        ('DamperFLmm', 'DamperFL'),
        ('DamperFRmm', 'DamperFR'),
        ('DamperRLmm', 'DamperRL'),
        ('DamperRRmm', 'DamperRR')
    ]

    def __init__(self):
        return

    def fix(self, dataset):
        for right, wrong in self.COMPATIBILITY_DICTIONARY:
            if wrong in dataset.get_original_data().columns:
                dataset.original_data[right] = dataset.original_data[wrong]
                dataset.original_data[wrong] = None
