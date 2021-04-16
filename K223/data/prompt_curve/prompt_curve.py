#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.special import erf
from numpy import genfromtxt
import argparse


plt.figure(figsize=(16,9))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=22,fontname='DejaVu Serif')
plt.yticks(fontsize=22,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')

my_data = genfromtxt(sys.argv[1], delimiter="\t")
x_plot=my_data[1:,0]
y_plot=np.array(my_data[1:,1])
y_plot_err=np.sqrt(y_plot)

x=x_plot[8:]
y=y_plot[8:]
y_err=y_plot_err[8:]
def func(x, a0,a1,t0,t1,sigma):
    return a1/2*(1+erf((x-t0)/sigma)*erf((t1-x)/sigma))+a0

#fit
popt, pcov= optimize.curve_fit(func,x,y,[10.,1000.,20,60,8],y_err)
#params
fit_a0=popt[0]
fit_a1=popt[1]
fit_t0=popt[2]
fit_t1=popt[3]
fit_sigma=popt[4]

#param errors
a0_err=np.sqrt(pcov[0][0])
a1_err=np.sqrt(pcov[1][1])
t0_err=np.sqrt(pcov[2][2])
t1_err=np.sqrt(pcov[3][3])
sigma_err=np.sqrt(pcov[4][4])




#print fit results
print("a0={:e} +/- {:e}".format(fit_a0,a0_err))
print("a1={:e} +/- {:e}".format(fit_a1,a1_err))
print("t0={:e} +/- {:e}".format(fit_t0,t0_err))
print("t1={:e} +/- {:e}".format(fit_t1,t1_err))
print("sigma={:e} +/- {:e}".format(fit_sigma,sigma_err))




#plot fit results
xx=np.linspace(min(x)-1,max(x)+1,100)
yy=func(xx,fit_a0,fit_a1,fit_t0,fit_t1,fit_sigma)
#calculate chi2
ychi=func(x,fit_a0,fit_a1,fit_t0,fit_t1,fit_sigma)
chisq=0
for i in range(len(x)):
    chisq+=((y[i]-ychi[i])/y_err[i])**2
print("chi2={:.4f}".format(chisq))

plt.plot(xx,yy,color="red",label="$f(t)=\\frac{A_1}{2}\cdot(1+$erf$(\\frac{t-t_0}{\sigma})\cdot $erf$(\\frac{t_1-t}{\sigma}))+A_0$\n$A_0$=(%.1f$\pm$%.1f)s$^{-1}$\n$A_1$=(%.1f$\pm$%.1f)s$^{-1}$\n$t_0$=(%.1f$\pm$%.1f)ns\n$t_1$=(%.1f$\pm$%.1f)ns\n$\sigma$=(%.1f$\pm$%.1f)ns"%(fit_a0,a0_err, fit_a1,a1_err,fit_t0,t0_err,fit_t1,t1_err, fit_sigma, sigma_err))
plt.text(42.4,600,"$\chi^2=$ {:.4f}".format(chisq))
plt.errorbar(x_plot,y_plot,y_plot_err,fmt=".",color="black",label="data points")
plt.xlabel("Delay / ns",fontsize=22,fontname='DejaVu Serif')
plt.ylabel("Coincidence count rate / s$^{-1}$",fontsize=22,fontname='DejaVu Serif')
plt.vlines(x=42, ymin=0, ymax=2200, linestyles="dashed",label="set value 42 ns", color="gray")
plt.ylim(0,2100)
plt.xlim(-30,80)
plt.legend(loc="upper left")
plt.savefig("../../TeX/figs/prompt/prompt.pdf", bbox_inches='tight')
plt.show()
