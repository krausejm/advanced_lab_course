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


plt.figure(dpi=300,figsize=(10.3,7.3))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=22,fontname='DejaVu Serif')
plt.yticks(fontsize=22,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')

file = ["./kick_data/kick_x_C0.csv","./kick_data/kick_z_C0.csv","./kick_data/kick_x_C1.csv","./kick_data/kick_z_C1.csv"]
labels = ["data C0 $x$","data C0 $z$","data C1 $x$","data C1 $z$"]
#file = sys.argv[1]
counter=0
for file in file:
    data = genfromtxt(file, delimiter=',')
    x = data[1:,1]
    y = data[1:,2]
    y_error = data[1:,4]
    chisq=0

    plt.errorbar(x=x, y=y, yerr=y_error, fmt='.', zorder=2, label = labels[counter])

    p,pcov = optimize.curve_fit(func_lin,x, y,[0,0],y_error)

    a, b = p
    a_err, b_err = [np.sqrt(pcov[0][0]),np.sqrt(pcov[1][1])]

    print("alpha="+str(-b/a))
    if min(x)<0:
        x_new = np.linspace(np.min(x)+0.02*np.min(x),np.max(x)-0.02*np.max(x),1000)
    else:
        x_new = np.linspace(np.min(x)-0.02*np.min(x),np.max(x)+0.02*np.max(x),1000)

    y_new = func_lin(x_new, a,b)
    ychi=func_lin(x,a,b)

    for i in range(len(y)):
        chisq+=((y[i]-ychi[i]))**2

    cov_err=pcov[0][1]

    print("chi2=",chisq)
    if "_x" in file:
        plt.plot(x_new,y_new, label="$x(I)=(%.4f\pm%.4f)\\frac{mm}{A}\cdot I + (%.4f\pm%.4f)$mm\n$\\chi^2=%.4f$"%(a,a_err,b,b_err, chisq))
    else:
        plt.plot(x_new,y_new, label="$z(I)=(%.4f\pm%.4f)\\frac{mm}{A}\cdot I  + (%.4f\pm%.4f)$mm\n$\\chi^2=%.4f$"%(a,a_err,b,b_err, chisq))
    #plt.text(0,-47,"$\chi^2$={:.4f}".format(chisq))
    counter += 1
plt.legend(bbox_to_anchor=(1,1))
plt.xlabel("I / A", fontsize=20)
plt.ylabel("$x, z$ / mm", fontsize=20)
plt.savefig("../../TeX/figs/calibration/"+"current_verification.pdf", bbox_inches='tight')
#plt.show()
