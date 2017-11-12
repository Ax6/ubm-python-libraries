from numpy import *


class SteeringAngle:
    """
    Gyroscope and Speed needed for calibration
    """

    STEERING_ANGLE = "SteeringAngle"
    CL_ZEROING = 0.1
    CL_MOVING_SPEED = 10

    def __init__(self, dataset):
        self.dataset = dataset
        self.ANGLE_OFFSET = 0
        self._calibrate()

    def get(self):
        return self.dataset.get_data()[self.STEERING_ANGLE] - self.ANGLE_OFFSET

    def _calibrate(self):
        gyro_yaw = self.dataset.get_gyroscope().get_yaw()
        is_moving = (self.dataset.get_speed() > self.CL_MOVING_SPEED)
        is_not_turning = (gyro_yaw < self.CL_ZEROING) & (gyro_yaw > self.CL_ZEROING)
        self.ANGLE_OFFSET = median(self.get()[is_moving & is_not_turning])


class Throttle:
    THROTTLE = "Throttle"

    def __init__(self, dataset):
        self.dataset = dataset

    def get(self):
        return self.dataset.get_data()[self.THROTTLE]


class Brakes:
    FRONT_PRESSURE = "PbrakeFrontBar"
    REAR_PRESSURE = "PbrakeRearBar"

    def __init__(self, dataset):
        self.dataset = dataset

    def get_front_pressure(self):
        return self.dataset.get_data()[self.FRONT_PRESSURE]

    def get_rear_pressure(self):
        return self.dataset.get_data()[self.REAR_PRESSURE]

    def get_balance(self):
        total_mean = mean(concatenate((self.get_front_pressure(), self.get_rear_pressure())))
        return round((mean(self.get_front_pressure()) / total_mean) * 50, 1)
