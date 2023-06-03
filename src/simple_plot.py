"""
file: simple_plot.py
description: demonstration program to validate matplotlib installation
author: CS @ RIT.EDU
"""

import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')

print( "close the window to terminate...")
plt.show()
