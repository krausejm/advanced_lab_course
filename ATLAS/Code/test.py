#!/usr/bin/env python3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import odr
from scipy import optimize
import sys
from numpy import genfromtxt

def func_lin(x, a,b):
    return a*x+b



plt.figure(dpi=300,figsize=(10.3,6))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=22,fontname='DejaVu Serif')
plt.yticks(fontsize=22,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')

file = sys.argv[1]
print(sys.argv[1])
data = genfromtxt(file, delimiter=',')
#print(data)
#print(sim_wmass,half_max,half_max_error,half_max_atlas,half_max_atlas_error)
#plt.errorbar(x=sim_wmass, y=half_max, yerr=half_max_error, fmt='.', zorder=2, label = "Simulated datapoints")
#curve fit berechnet kleinere cov als odr... klappt auf jeden fall
x=data[1:1]
y=data[1:2]
print("xXXXXXXXXXXX\n",x)
#print(x)

#p,pcov = optimize.curve_fit(func_lin,x, y,[0,0])



#a, b = p
#a_err, b_err = [np.sqrt(pcov[0][0]),np.sqrt(pcov[1][1])]

#x_new = np.linspace(x[0]-1,x[-1]+1,1000)
#y_new = func_lin(x, a,b)
#chisq=0
#for i in range(len(half_max)):
#    chisq+=((half_max[i]-ychi[i])/half_max_error[i])**2
plt.plot(x,y)
plt.show()
