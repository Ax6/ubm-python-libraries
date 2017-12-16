import numpy as np
import math
from Acquisition.Dataset import IMU
from Acquisition.Dataset import Vehicle
from Acquisition.Dataset import Driver
from Acquisition.Dataset import Internal


class Dataset:
    F_SAMPLING = 100.0

    def __init__(self, data):
        self.original_data = data
        NameCompatibility().fix(self)
        self.start_instant = Instant(0)
        self.end_instant = Instant(self._get_total_duration(), Instant.TYPE_TIME)
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
        return self.original_data[:][self.start_instant.to_sample():self.end_instant.to_sample()]

    def set_start_time(self, time):
        self.start_instant = Instant(time, Instant.TYPE_TIME)

    def set_end_time(self, time):
        self.end_instant = Instant(time, Instant.TYPE_TIME)

    def get_time_axis(self):
        print(self.start_instant.to_sample())
        print(self.end_instant.to_sample())
        return self._get_interval().to_time()

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

    def _get_interval(self):
        return Interval(self.start_instant, self.end_instant)

    def _get_total_duration(self):
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


class Interval:
    F_SAMPLING = Dataset.F_SAMPLING

    def __init__(self, start, end):
        """
        :type start: Instant
        :type end: Instant
        """
        self.start = start
        self.end = end

    def to_sample(self):
        return np.r_[self.start.to_sample():self.end.to_sample()]

    def to_time(self):
        return self.to_sample() / self.F_SAMPLING


class Instant:
    F_SAMPLING = Dataset.F_SAMPLING
    TYPE_SAMPLE = 0
    TYPE_TIME = 1

    def __init__(self, instant, instant_type=TYPE_SAMPLE):
        self.type = instant_type
        self.instant = instant
        if self.type == self.TYPE_TIME:
            self.instant = math.floor(instant * self.F_SAMPLING)

    def to_sample(self):
        return self.instant

    def to_time(self):
        return self.instant * self.F_SAMPLING
