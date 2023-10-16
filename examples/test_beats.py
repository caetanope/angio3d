import matplotlib.pyplot as plt
import numpy as np

resolution_multiplier = 1
resolution = 30 * resolution_multiplier
xpoints = range(0,resolution)
diastole = 13/20*resolution
systole = resolution - diastole
#ypoints = np.array([3, 10])
#-1+e^(-x)

ypoints = []
for x in xpoints:
    if x < diastole:
        y = (1-np.e**(-x/(resolution/10)))
    else:
        y = np.e**(-(x-diastole)/(resolution/15))

    y=y*0.8+0.5
    y=y**(1/3)
    ypoints.append(y)

plt.plot(xpoints, ypoints)
plt.show()