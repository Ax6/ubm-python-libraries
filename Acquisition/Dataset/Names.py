class Names:
    """
    Another Luke pearl
    """

    # (Right, Wrong)
    COMPATIBILITY_DICTIONARY = [
        ('DamperFLmm', 'DamperFL'),
        ('DamperFRmm', 'DamperFR'),
        ('DamperRLmm', 'DamperRL'),
        ('DamperRRmm', 'DamperRR'),
    ]

    Driver = {
        "SteeringAngle": 'SteeringAngle',
        "Throttle": 'Throttle',
        "Brakes": ('PbrakeFrontBar', 'PbrakeRearBar')
    }

    Engine = {

    }

    IMU = {
        "Accelerometer": ('AccXg', 'AccYg', 'AccZg'),
        "Gyroscope": ('GyroXrad', 'GyroYrad', 'GyroZrad')
    }

    Internal = {

    }

    Vehicle = {
        "PhonicWheels": ('SpeedFLKmh', 'SpeedFRKmh', 'SpeedRLKmh', 'SpeedRRKmh'),
        "Dampers": ('DamperFLmm', 'DamperFRmm', 'DamperRLmm', 'DamperRRmm'),
        "RideHeight": ('FLHeightmm', 'FRHeightmm', 'RLHeightmm', 'RRHeightmm')
    }

    def __init__(self):
        return

    def fix(self, dataset):
        for right, wrong in self.COMPATIBILITY_DICTIONARY:
            if wrong in dataset.get_original_data().columns:
                dataset.original_data[right] = dataset.original_data[wrong]
                dataset.original_data[wrong] = None
