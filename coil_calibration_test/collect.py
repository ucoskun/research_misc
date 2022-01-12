#Fluxgate calibration test using a 3D printed solenoid 1/11/2022

import pyvisa
import serial
import numpy as np
import time
from datetime import datetime

now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

probe_number = 22

# Initialize serial communication with Arduino
mcon = serial.Serial('COM3', 9600, timeout = 3)
print('Probe Switcher : ATMega bootloader is loading')
time.sleep(4)
print('Done.')

mcon.write((str(probe_number).zfill(2)).encode('ascii'))

#Load VISA resource manager
rm = pyvisa.ResourceManager()

#Initialize Coil power supply and multimeter
coil = rm.open_resource('ASRL6::INSTR')
dmm = rm.open_resource('USB0::0x0957::0x0A07::MY48003317::0::INSTR')
print(coil.query('*IDN?'))
print(dmm.query('*IDN?'))

def measureCurr():
    curr_str = coil.query('MEAS:CURR?')
    return float(curr_str[:-2])

def setCurr(val):
    coil.write('CURR ' + str(val))

def outp(val):
    coil.write('OUTP ' + str(val))

#Setting voltage limit first and turn off output
outp(0)
coil.write('VOLT 10')

time.sleep(0.1)

# Reset DMM and configure
dmm.write('*RST')                   # Reset the settings
dmm.write('SENS:VOLT:DC:NPLC 10')   # NPLC = 10 (Can change later)
dmm.write('VOLT:RANG 1')          # Voltage full scale range
dmm.write('VOLT:DC:IMP:AUTO 1')     # 10G Input Impedance
dmm.write('TRIG:SOUR IMM')          # Trigger immediately

time.sleep(1)

def measureB():
    res = dmm.query('READ?')
    return float(res) * 100.0 #micro Tesla units

#Currents to test (units Amperes)
curr_list = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007]

#Number of repeats per current
n_repeat = 10

#Data taking starts here
data = np.empty([len(curr_list), n_repeat, 3])

datasize = data.shape[0] * data.shape[1]
progress_count = 0
for id_appCurr, appCurr in enumerate(curr_list):
    setCurr(appCurr)
    for id_repeat in range(n_repeat):
        outp(1)
        time.sleep(0.6)
        curr = measureCurr()
        coil_on_B = measureB()
        outp(0)
        time.sleep(0.6)
        coil_off_B = measureB()

        data[id_appCurr, id_repeat, 0] = curr
        data[id_appCurr, id_repeat, 1] = coil_on_B
        data[id_appCurr, id_repeat, 2] = coil_off_B
        progress_count += 1

        print('Progress = ', round(100 * progress_count/datasize),'%',' Current Measured : ', round(curr,4), ' Coil_On_B : ', round(coil_on_B,3), ' Coil_Off_B : ', round(coil_off_B,3), ' Difference : ',round(coil_on_B-coil_off_B,3))
    
#Save data into a file
np.save('data/'+str(probe_number) + '_' + str(now), data)