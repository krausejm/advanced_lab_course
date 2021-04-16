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


def anpassung_yerr(function, x, y, y_error, presets, plot):
    model = odr.Model(function)
    data = odr.RealData(x, y, sy=y_error)
    out = odr.ODR(data, model, beta0=presets).run()
    popt = out.beta
    perr = out.sd_beta
    pcov = out.cov_beta
    if plot == True:
        x_fit = np.linspace(min(x), max(x), 10000)
        y_fit = function(popt, x_fit)
        plt.plot(x_fit, y_fit)

    return popt,perr, pcov

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
data = genfromtxt(file, delimiter='\t')
x = data[1:,0]
y = data[1:,3]
y_error = [0.1 for i in range(len(y))] 


plt.errorbar(x=x, y=y, yerr=[0.01 for i in range(len(y))], fmt='.', zorder=2, label = "data")
#plt.plot(x,y, '.', label="data")

p,pcov = optimize.curve_fit(func_lin,x, y,[0,0],y_error)

a, b = p
a_err, b_err = [np.sqrt(pcov[0][0]),np.sqrt(pcov[1][1])]

print("alpha="+str(-b/a))
if min(x)<0:
    x_new = np.linspace(np.min(x)+0.02*np.min(x),np.max(x)-0.02*np.max(x),1000)
else:
    x_new = np.linspace(np.min(x)-0.02*np.min(x),np.max(x)+0.02*np.max(x),1000)
#x_new = np.linspace(np.min(x),np.min(x),1000)

y_new = func_lin(x_new, a,b)
ychi=func_lin(x,a,b)
chisq=0
for i in range(len(y)):
    chisq+=((y[i]-ychi[i])/y_error[i])**2

cov_err=pcov[0][1]
alpha_value=-b/a
alpha_error=np.sqrt(2*(-b)/a**3*cov_err+(1/a*b_err)**2+((-b)/a**2*a_err)**2)
if alpha_error<0.1:
    alpha_error=0.1
print(alpha_value, alpha_error)

print("chi2=",chisq)
plt.plot(x_new,y_new, label="$\Delta x(\\alpha)=(%.3f\pm%.3f) \\frac{mm}{mrad}\cdot \\alpha + (%.3f\pm%.3f)mm$\n$\\chi^2=%.3f$\n"%(a,a_err,b,b_err, chisq))
#plt.text(0,-47,"$\chi^2$={:.4f}".format(chisq))
plt.errorbar(y=0, x=alpha_value,fmt='.', yerr=alpha_error, color="black", label="$\\alpha_{ideal}=(%.1f\pm%.1f)$ mrad"%(alpha_value, round(alpha_error,1)))
plt.vlines(x=-b/a,ymin=np.min(y_new), ymax=np.max(y_new),linestyles="--", color="gray")
plt.legend(bbox_to_anchor=(1,-0.2))
plt.xlabel("$\\alpha$ / mrad", fontsize=20)
if "_x" in file:
    plt.ylabel("$\Delta x$ / mm", fontsize=20)
else:
    plt.ylabel("$\Delta z$ / mm", fontsize=20)
plt.axis([max(x_new),min(x_new),max(y_new),min(y_new)])
print(sys.argv[1][:-4])
plt.savefig("../../TeX/figs/calibration/"+sys.argv[1][13:-4]+".pdf", bbox_inches='tight')
#plt.show()
