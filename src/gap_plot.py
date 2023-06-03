"""
   file: gap_plot.py
   author: http://stackoverflow.com/questions/15652503/put-a-gap-break-in-a-line-plot
   author: bksteele, bksvcs@rit.edu

   Masked arrays work well for skipping gaps in missing data.
   You need to mask the first of the points you don't want to connect.
   See the documentation links below and the warning at the end.
"""

# numpy is a set of important python numeric tools modules
import numpy as np

# http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html
import numpy.ma as ma

import matplotlib.pyplot as plt

t1 = np.arange(0, 8, 0.25)
mask_start = len(t1)
t2 = np.arange(10, 14, 0.25)
t = np.concatenate([t1, t2])
c = np.cos(t) # generate cos(t) over values in the array t

# create a masked array from the data
mc = ma.array(c)

""" from maskedarray pydocs:
   recommended way to mark one or several specific entries of a masked array
   as invalid is to assign the special value masked to them:
"""
mc[mask_start] = ma.masked
# the data between where t1 ended and t2 starts again is now masked.
# masked data will be skipped by plotting, leaving a 'gap/break'.

plt.figure()
plt.plot(t, mc, '*', linestyle="-")
plt.title('Using masked arrays')

#################################################
"""
warning: plt.show() has termination issues and platform differences.
The 'normal' behavior is for the show() function to block until
the user has closed the plotting window (x-ing out).
That is known as interactive python behavior.

On several platforms of python3, x-ing out may hang the process, 
which means that whatever comes after in the code execution will not
execute. 

When your program gets hung up, the control-C key combination may
not work, and neither does control-D (which may log you out!).
Instead, you have to control-Z to put the program to sleep. Then
use your OS tools to kill the program. On OSX and *NIX, the command
sequence to kill the program is this: kill %1; fg %1
(The fg command is needed because the python program is waiting to
output its dying message.)

The primary, preferred solution to this problem is to call 
matplotlib.use( <backend-str> ) to have set the background drawing
mechanisms up to be able to continue after the show() blocks.

To set up the backend, see backendlisting.py for more information
and links on how to make interactive plotting work more smoothly.
--bks
"""
#################################################

print( "showing now. close the window to quit..." )
plt.show()


