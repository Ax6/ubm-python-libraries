import numpy as np
from Acquisition.Filter import Filter


class Speed:
    FRONT_LEFT = "SpeedFLKmh"
    FRONT_RIGHT = "SpeedFRKmh"
    REAR_LEFT = "SpeedRLKmh"
    REAR_RIGHT = "SpeedRRKmh"

    def __init__(self, dataset):
        self.dataset = dataset
        self.phonic_wheels = {
            self.FRONT_LEFT: PhonicWheel(self.dataset, self.FRONT_LEFT),
            self.FRONT_RIGHT: PhonicWheel(self.dataset, self.FRONT_RIGHT),
            self.REAR_LEFT: PhonicWheel(self.dataset, self.REAR_LEFT),
            self.REAR_RIGHT: PhonicWheel(self.dataset, self.REAR_RIGHT),
        }

    def get(self):
        to_average = [self.get_sensor(self.FRONT_LEFT).get(), self.get_sensor(self.FRONT_RIGHT).get()]
        return np.mean(np.transpose(to_average), 1)

    def get_sensor(self, position):
        return self.phonic_wheels[position]


class Dampers:
    FRONT_LEFT = "DamperFLmm"
    FRONT_RIGHT = "DamperFRmm"
    REAR_LEFT = "DamperRLmm"
    REAR_RIGHT = "DamperRRmm"

    def __init__(self, dataset):
        self.dataset = dataset

    def get_front_left(self):
        return self.dataset.get_data()[self.FRONT_LEFT]

    def get_front_right(self):
        return self.dataset.get_data()[self.FRONT_RIGHT]

    def get_rear_left(self):
        return self.dataset.get_data()[self.REAR_LEFT]

    def get_rear_right(self):
        return self.dataset.get_data()[self.REAR_RIGHT]


class RideHeight:
    FRONT_LEFT = "FLHeightmm"
    FRONT_RIGHT = "FRHeightmm"
    REAR_LEFT = "RLHeightmm"
    REAR_RIGHT = "RRHeightmm"

    def __init__(self, dataset):
        self.dataset = dataset

    def get_front_left(self):
        return self.dataset.get_data()[self.FRONT_LEFT]

    def get_front_right(self):
        return self.dataset.get_data()[self.FRONT_RIGHT]

    def get_rear_left(self):
        return self.dataset.get_data()[self.REAR_LEFT]

    def get_rear_right(self):
        return self.dataset.get_data()[self.REAR_RIGHT]


class PhonicWheel:
    def __init__(self, dataset, position):
        self.dataset = dataset
        self.position = position
        self.filtered = None
        self.filter = Filter()
        self.filter.set_type(Filter.TYPE_MEDIAN)

    def get(self):
        if self.filtered is None:
            self.filtered = self._get_filtered()
        return self.filtered

    def get_raw(self):
        return self.dataset.get_data()[self.position]

    def get_opposite_sensor(self):
        opposite_position = Speed.FRONT_LEFT
        if self.position == Speed.FRONT_LEFT:
            opposite_position = Speed.FRONT_RIGHT
        if self.position == Speed.REAR_LEFT:
            opposite_position = Speed.REAR_RIGHT
        if self.position == Speed.REAR_RIGHT:
            opposite_position = Speed.REAR_LEFT
        return self.dataset.speed.get_sensor(opposite_position)

    def _get_filtered(self):
        self.filter.set_data(self.get_raw())
        no_outliers = self.filter.remove_outliers(4, 48)
        self.filter.set_data(no_outliers)
        working_intervals = self.filter.detect_stuck(48)
        calc_from_opposite = self._calc_on_wheel()
        no_outliers[working_intervals == 0] = calc_from_opposite[working_intervals == 0]
        self.filter.set_data(no_outliers)
        self.filter.set_param(Filter.PARAM_WINDOW_LENGTH, 13)
        return self.filter.get()

    def _calc_on_wheel(self):
        opposite_sensor = self.get_opposite_sensor()
        gyro_yaw = self.dataset.get_gyroscope().get_yaw() / 10
        if self.position == Speed.FRONT_RIGHT or self.position == Speed.REAR_RIGHT:
            gyro_yaw = -gyro_yaw
        self.filter.set_data(opposite_sensor.get_raw())
        return self.filter.remove_outliers() + gyro_yaw
