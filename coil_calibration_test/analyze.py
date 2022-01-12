import numpy as np
import matplotlib.pyplot as plt

data_name = '22_11-01-2022_21-53-32'

data = np.load('data/' + data_name + '.npy')

data = np.average(data, axis=1)

current = data[:,0]

coil_on = data[:,1]

coil_off = data[:,2]

coef = np.polyfit(current,coil_on - coil_off,1)
poly1d_fn = np.poly1d(coef) 
#plt.plot(current, coil_on, label='Coil on Measurement')
#plt.plot(current, coil_off, label='Coil off Measurement')
plt.plot(current, coil_on - coil_off, 'x',label='Difference')
plt.plot(current, poly1d_fn(current), '--k')

plt.plot([], [], ' ', label='Gain = ' + str(round(coef[0],3)) + '\nOffset = ' + str(round(coef[1],3)))
plt.legend()
plt.xlabel('Current Measured [A]')
plt.ylabel('Field [uT]')
plt.title(data_name)
plt.show()
