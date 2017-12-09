from numpy import *


class Speed:
    FRONT_LEFT = "SpeedFLKmh"
    FRONT_RIGHT = "SpeedFRKmh"
    REAR_LEFT = "SpeedRLKmh"
    REAR_RIGHT = "SpeedRRKmh"

    def __init__(self, dataset):
        self.dataset = dataset

    def get(self):
        return mean(transpose([self.get_front_left(), self.get_front_right()]), 1)

    def get_front_left(self):
        return self.dataset.get_data()[self.FRONT_LEFT]

    def get_front_right(self):
        return self.dataset.get_data()[self.FRONT_RIGHT]


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
