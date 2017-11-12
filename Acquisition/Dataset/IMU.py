from Acquisition.Filter import Filter
from numpy import *


class Accelerometer:
    PITCH = "AccXg"
    ROLL = "AccZg"
    YAW = "AccYg"

    def __init__(self, dataset):
        self.dataset = dataset
        self.filter = Filter()
        self.filter.set_type(Filter.MEDIAN)

    def get_pitch(self):
        return self.filter.set_data(self.dataset.get_data()[self.PITCH]).get()

    def get_roll(self):
        return self.filter.set_data(self.dataset.get_data()[self.ROLL]).get()

    def get_yaw(self):
        return self.filter.set_data(self.dataset.get_data()[self.YAW]).get()

    def get_filter(self):
        return self.filter


class Gyroscope:
    """
    Accelerometer needed for calibration
    """

    PITCH = "GyroXrad"
    ROLL = "GyroZrad"
    YAW = "GyroYrad"
    CL_ZEROING = 0.05

    def __init__(self, dataset):
        self.dataset = dataset
        self.filter = Filter()
        self.filter.set_type(Filter.MEDIAN)
        self.PITCH_OFFSET = 0
        self.ROLL_OFFSET = 0
        self.YAW_OFFSET = 0
        self._calibrate()

    def get_pitch(self):
        return self.filter.set_data(self.dataset.get_data()[self.PITCH]).get() - self.PITCH_OFFSET

    def get_roll(self):
        return self.filter.set_data(self.dataset.get_data()[self.ROLL]).get() - self.ROLL_OFFSET

    def get_yaw(self):
        return self.filter.set_data(self.dataset.get_data()[self.YAW]).get() - self.YAW_OFFSET

    def get_filter(self):
        return self.filter

    def _calibrate(self):
        acc_pitch = self.dataset.get_accelerometer().get_pitch()
        self.PITCH_OFFSET = median(self.get_pitch()[(acc_pitch < self.CL_ZEROING) & (acc_pitch > -self.CL_ZEROING)])

        acc_roll = self.dataset.get_accelerometer().get_roll()
        self.ROLL_OFFSET = median(self.get_roll()[(acc_roll < self.CL_ZEROING) & (acc_roll > -self.CL_ZEROING)])

        acc_yaw = self.dataset.get_accelerometer().get_yaw()
        self.YAW_OFFSET = median(self.get_yaw()[(acc_yaw < self.CL_ZEROING) & (acc_yaw > -self.CL_ZEROING)])
