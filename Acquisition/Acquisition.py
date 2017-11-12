from Acquisition.Dataset.Dataset import Dataset
from numpy import genfromtxt


class Acquisition:

    START_WITH_CAR_OFFSET = 10

    def __init__(self, name):
        self.name = name
        self.dataset = Dataset(self._load_data())

    def get_name(self):
        return self.name

    def get_dataset(self):
        return self.dataset

    def _load_data(self):
        return genfromtxt(self.name + '.csv', delimiter=',', names=True, dtype='double')