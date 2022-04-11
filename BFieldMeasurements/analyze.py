import numpy as np
import matplotlib.pyplot as plt

trolley_to_radius = 22.7 / 30000.0
rotate_to_phi = np.pi / 8000.0
vertical_to_z = 15.2 / 50000.0

trolley_0 = 3400.0
rotate_0 = 4050
vertical_0 = -34500.0

data = np.loadtxt("data/4-03-2022_15-30/output.txt")

trolley = data[:, 0]
rotate = data[:, 1]
vertical = data[:, 2]

power = data[:, 9]

monitor = data[:, 10]

time = data[:, 12]


r = trolley_to_radius * (trolley - trolley_0)
phi = rotate_to_phi * (rotate - rotate_0)
z = vertical_to_z * (vertical - vertical_0)

x = r * np.cos(phi)
y = r * np.sin(phi)

b_x_f = data[:, 3]
b_y_f = data[:, 5]
b_z_f = data[:, 7]

b_x = b_z_f * np.cos(phi) + b_x_f * np.sin(phi)
b_y = b_z_f * np.sin(phi) - b_x_f * np.cos(phi)
b_z = - b_y_f

fig, ax = plt.subplots()
ax.plot(x, b_x, '.')

ax.set(xlabel='x', ylabel='B_x [mG]')
ax.grid()


plt.show()