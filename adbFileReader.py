import re
import pickle

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import pandas as pd

voltages = []
currents = []
times = []

prev_line = ""
with open("test_logcat.txt") as logC:
    current_found = 0
    for line in logC:
        if ("OnResponseReceived" and "AUX_CURRENT") in line:
            #output_line = line.decode("utf-8").strip()
            hex_current = line[-4:]
            current_mA = (65535 - int(hex_current, 16)) # SPAR uses 0xFFFF as 0 amps for some reason, so (0xFFFF - 0x????) gives mA 
            current_A = current_mA * 0.00001
            currents.append(round(current_A, 4))
            current_found = 1

            match = re.search(r'\d{2}:\d{2}:\d{2}.\d{3}', prev_line)
            times.append(str(match.group()))

        if ("AUX_VOLTAGE" in line) and (current_found == 1):
            #output_line = line.decode("utf-8").strip()
            hex_volt = line[-4:]
            volt_mV = int(hex_volt, 16)
            volt_V = volt_mV * 0.01
            voltages.append(round(volt_V, 6))
            current_found = 0
        
        prev_line = line

'''
with open("volts.txt", "w") as v:
    v.write(str(voltages))

with open("currents.txt", "w") as c:
    c.write(str(currents))

with open("times.txt", "w") as t:
    t.write(str(times))

'''

#x = np.linspace(0, 1000, len(voltages), endpoint=True)
dates = pd.to_datetime(times, format='%H:%M:%S.%f')
lstDateTime = dates.to_list()

with open("timesDatetime.txt", "w") as t:
    t.write(str(lstDateTime))

fig, ax = plt.subplots(2)
ax[0].plot(lstDateTime, voltages)
ax[1].plot(lstDateTime, currents)

myFmt = mdates.DateFormatter('%H:%M:%S')
ax[0].xaxis.set_major_formatter(myFmt)
ax[1].xaxis.set_major_formatter(myFmt)

ax[0].set_xlabel('Time')
ax[0].set_ylabel('Volts (V)')

ax[1].set_xlabel('Time')
ax[1].set_ylabel('Current (A)')


plt.show()