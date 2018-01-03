from LogsManager import Manager
from matplotlib import pyplot as plt
from Acquisition.Dataset.Vehicle import Speed
from Acquisition.Dataset.Dataset import Instant
import numpy as np
from scipy import signal

logs = Manager('../../../../Data/log_files/*/')
acq = logs.get_acquisition('301017_Imola_null_null_run3')
print(acq.get_name())
dataset = acq.get_dataset()
lim = [0, dataset.get_time_axis()[-1]]
dataset.set_start_time(lim[0])
dataset.set_end_time(lim[1])

t = dataset.get_time_axis()

raw = dataset.speed.get_sensor(Speed.FRONT_LEFT).get_raw()
plt.plot(t, raw,  linewidth=0.4, label='left_raw')
plt.plot(t, dataset.speed.get_sensor(Speed.FRONT_LEFT).get(), linewidth=2, label='left_get')

plt.legend(loc='upper left')
plt.xlim(lim)
plt.show()
