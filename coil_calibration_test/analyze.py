import numpy as np
import matplotlib.pyplot as plt

data_name = '9_23-01-2022_21-19-19'

data = np.load('data/' + data_name + '.npy')
data_shape = data.shape
data = np.average(data, axis=1)

curr_on = data[:,0]
curr_off = data[:,1]
coil_on = data[:,2]
coil_off = data[:,3]

coef, res, _, _, _ = np.polyfit(curr_on - curr_off,coil_on - coil_off,1, full=True)
poly1d_fn = np.poly1d(coef) 
#plt.plot(current, coil_on, label='Coil on Measurement')
#plt.plot(current, coil_off, label='Coil off Measurement')
plt.plot(curr_on - curr_off, coil_on - coil_off, 'x',label='Difference')
plt.plot(curr_on - curr_off, poly1d_fn(curr_on - curr_off), '--r')

plt.plot([], [], ' ', label='Gain = ' + str(round(coef[0],3)) + '\nOffset = ' + str(round(coef[1],3))+ '\nResidual = ' + str(res[0])+'\nRepeat = ' + str(data_shape[1]))
plt.legend()
plt.xlabel('Current Measured [A]')
plt.ylabel('Field [uT]')
plt.title(data_name)

plt.savefig('plots/'+ data_name + '.png', format='png')

plt.show()
