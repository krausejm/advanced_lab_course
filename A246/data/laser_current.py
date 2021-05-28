#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse


def lin_func(p, x):

     m,c=p
     return m*x+c


my_data = genfromtxt(sys.argv[1], delimiter='\t')
x = my_data[1:, 0]
x_error = 0.1*x
y = my_data[1:, 1]
y_error = 0.1*y



lin_model = sodr.Model(lin_func)
#fit_data = sodr.RealData(x, y) #wenn x-error 0
fit_data = sodr.RealData(x, y, sx=x_error, sy=y_error)
odr = sodr.ODR(fit_data, lin_model, beta0=[0.,0.])
out = odr.run()


a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]


print("Fitergebnis:\n")
print("y = a * x + b mit\n")
print("a = {:.3f} +/- {:.3f}".format(a, err_a))
print("b = {:.3f} +/- {:.3f}".format(b, err_b))
y_fit = a * x +b


plt.figure()
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=22,fontname='DejaVu Serif')
plt.yticks(fontsize=22,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')
plt.plot(x,y,'.')

plt.errorbar(x, y, xerr=x_error,yerr=y_error,
                lw=2, fmt='.', label=r"measured data")
#plt.plot(x, y_fit, lw=2, label=r"linear fit ")
plt.xlabel('Laser current / mA')
plt.ylabel('Power / $\mu$W')
plt.legend()
plt.show()
