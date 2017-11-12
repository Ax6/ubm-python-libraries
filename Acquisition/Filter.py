import scipy.signal as signal


class Filter:
    SGOLAY = "sgolay"
    MEDIAN = "median"
    # MOVING_AVERAGE = "MovingAverage"
    # LMS = "LMS"
    # LOW_PASS = "LowPass"
    PARAMETERS = {
        SGOLAY: {
            "window_length": 31,
            "polynomial_order": 5
        },
        MEDIAN: {
            "window_length": 31
        }
    }

    def __init__(self):
        self.type = self.SGOLAY
        self.data = []

    def set_data(self, data):
        self.data = data
        return self

    def set_type(self, flt_type):
        if self._type_exist(flt_type):
            self.type = flt_type
        else:
            raise ValueError("Unrecognised filter of type: " + flt_type)

    def set_param(self, param, value):
        self.PARAMETERS[self.type][param] = value

    def get(self):
        return getattr(self, 'get_' + self.type)()

    def get_sgolay(self):
        params = self._get_params(self.SGOLAY)
        return signal.savgol_filter(self.data, params['window_length'], params['polynomial_order'])

    def get_median(self):
        params = self._get_params(self.MEDIAN)
        return signal.medfilt(self.data, [params['window_length']])

    def _get_params(self, flt_type):
        return self.PARAMETERS[flt_type]

    def _type_exist(self, flt_type):
        if flt_type in self.PARAMETERS:
            return True
        else:
            return False
