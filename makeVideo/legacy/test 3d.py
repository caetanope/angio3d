import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.

o = np.arange(0, 2*np.pi, 0.25)
p = np.arange(0, np.pi, 0.125)
r = 1

X = r * np.sin(o) * np.cos(p)
Y = r * np.cos(o) * np.sin(p)
Z = r * np.cos(o)

# Plot the surface.
surf = ax.plot_wireframe(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()