"""
   backendlisting.py lists the python backend choices for your platform.
   Run this to determine what to pass 
   as the backend-str to matplotlib.use( 'backend-str')

   Also see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend
   to learn about backends for interactive python graphics.

   author: http://stackoverflow.com/questions/5091993/list-of-all-available-matplotlib-backends

   converted from python 2
   author: bksteele, bksvcs@rit.edu
"""

from pylab import *
import time

import matplotlib.backends
import matplotlib.pyplot as p
import os.path


def is_backend_module(fname):
    """Identifies if a filename is a matplotlib backend module"""
    return fname.startswith('backend_') and fname.endswith('.py')

def backend_fname_formatter(fname): 
    """Removes the extension of the given filename, then takes away the leading 'backend_'."""
    return os.path.splitext(fname)[0][8:]

# get the directory where the backends live
backends_dir = os.path.dirname(matplotlib.backends.__file__)

# filter all files in that directory to identify all files which provide a backend
backend_fnames = filter(is_backend_module, os.listdir(backends_dir))

backends = [backend_fname_formatter(fname) for fname in backend_fnames]

print( "supported backends: \t" + str(backends))

# validate backends
backends_valid = []
for b in backends:
    try:
        p.switch_backend(b)
        backends_valid += [b]
    except:
        continue

print( "valid backends: \t" + str(backends_valid))

