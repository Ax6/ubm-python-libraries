from Acquisition.Filter import Filter
from numpy import *


class InertialAxis:

    def __init__(self, device):
        self.device = device
        self.filter = device.filter
        self.dataset = device.dataset
        self.X_OFFSET = 0
        self.Y_OFFSET = 0
        self.Z_OFFSET = 0
        self.get_pitch = self.get_x
        self.get_roll = self.get_y
        self.get_yaw = self.get_z

    def get_x(self):
        return self.filter.set_data(self.get_raw_x()).get() + self.X_OFFSET

    def get_y(self):
        return self.filter.set_data(self.get_raw_y()).get() + self.Y_OFFSET

    def get_z(self):
        return self.filter.set_data(self.get_raw_z()).get() + self.Z_OFFSET

    def get_raw_x(self):
        # As strange as it might seem, it is right.
        # Thanks Team-Luke for the erroneous Axis
        return -self.dataset.get_data()[self.device.AXIS_X]

    def get_raw_y(self):
        # Same
        return self.dataset.get_data()[self.device.AXIS_Z]

    def get_raw_z(self):
        # Same
        return self.dataset.get_data()[self.device.AXIS_Y]


class Accelerometer(InertialAxis):
    AXIS_X = "AccXg"
    AXIS_Y = "AccYg"
    AXIS_Z = "AccZg"

    def __init__(self, dataset):
        self.dataset = dataset
        self.filter = Filter()
        self.filter.set_type(Filter.TYPE_MEDIAN)
        InertialAxis.__init__(self, self)

    def get_filter(self):
        return self.filter


class Gyroscope(InertialAxis):
    """
    Accelerometer needed for calibration
    """

    AXIS_X = "GyroXrad"
    AXIS_Y = "GyroYrad"
    AXIS_Z = "GyroZrad"
    CL_ZEROING = 0.05

    def __init__(self, dataset):
        self.dataset = dataset
        self.filter = Filter()
        self.filter.set_type(Filter.TYPE_MEDIAN)
        InertialAxis.__init__(self, self)

    def get_filter(self):
        return self.filter

    def calibrate(self):
        acc_x = self.dataset.get_accelerometer().get_x()
        self.X_OFFSET = median(self.get_pitch()[(acc_x < self.CL_ZEROING) & (acc_x > -self.CL_ZEROING)])

        acc_y = self.dataset.get_accelerometer().get_y()
        self.Y_OFFSET = median(self.get_roll()[(acc_y < self.CL_ZEROING) & (acc_y > -self.CL_ZEROING)])

        acc_z = self.dataset.get_accelerometer().get_z()
        self.Z_OFFSET = median(self.get_yaw()[(acc_z < self.CL_ZEROING) & (acc_z > -self.CL_ZEROING)])

