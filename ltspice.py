import ltspice
import matplotlib.pyplot as plt
import numpy as np
import os

l = ltspice.Ltspice('21.raw')
# Make sure that the .raw file is located in the correct path
l.parse() 

time = l.get_time()
V_source = l.get_data('V(source)')
V_cap = l.get_data('V(cap)')

plt.plot(time, V_source)
plt.plot(time, V_cap)
plt.show()