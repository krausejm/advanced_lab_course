#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from numpy import genfromtxt
import argparse
import datetime
import pandas as pd
import matplotlib.dates as mdates


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

time = 200
df = pd.read_csv('measurement.csv')
angles = [180,90,270,225,135,120,105,150,165,195,210,240,255]
angles_important = [180,90,270,225,135]
x = np.array([np.mean(df[df["angle"]==angles]["angle"]) for angles in angles])
x_err = [1 for i in range(len(x))]
y = np.array([np.mean(df[df["angle"]==angles]["coincidence"]) for angles in angles])/time
y_err = np.array([np.sqrt(np.sum((df[df["angle"]==angles]["coincidence"])))/(len(df[df["angle"]==angles])*time) for angles in angles])

######
# Random coincidences
######

nr=2.75
nr_err=0.05

######
# Time dependent counting rate
######
plt.figure(figsize=(16,9))
clock = df["clock"] = pd.to_datetime(df["clock"]) 
plt.errorbar(x=clock,y=df["n1"],yerr=np.sqrt(df["n1"]),fmt=".")
plt.xticks(rotation = 25)
plt.grid(color='black',linestyle=':')
plt.xlabel("time / HH:MM")
plt.ylabel("Counts $N_1$ / $10^2$")
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)

plt.savefig("../../TeX/figs/main/time_dependence_n1.pdf", bbox_inches='tight')
plt.show()
plt.figure(figsize=(16,9))
for angles_important in angles_important:
    clock = pd.to_datetime(df[df["angle"]==angles_important]["clock"],format='%H:%M:%S',exact=True)
    plt.errorbar(x=clock,y=df[df["angle"]==angles_important]["n2"],yerr=np.sqrt(df[df["angle"]==angles_important]["n2"]),fmt=".",label=("$\\theta$=(%d$\pm$%d)$^\circ$"%(angles_important,1)))
plt.xticks(rotation = 35)
plt.grid(color='black',linestyle=':')
plt.legend()
plt.xlabel("time / HH:MM")
plt.ylabel("Counts $N_2$ / $10^2$")
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
plt.savefig("../../TeX/figs/main/time_dependence_n2.pdf", bbox_inches='tight')
plt.show()

######
# Apply correction
######

count1=np.array([np.mean(df[df["angle"]==angles]["n1"]) for angles in angles])
count1_err = np.array([np.sqrt(np.sum((df[df["angle"]==angles]["n1"])))/(len(df[df["angle"]==angles])*time) for angles in angles])
count2=np.array([np.mean(df[df["angle"]==angles]["n2"]) for angles in angles])
count2_err = np.array([np.sqrt(np.sum((df[df["angle"]==angles]["n2"])))/(len(df[df["angle"]==angles])*time) for angles in angles])
plt.errorbar(x=x,y=count1,yerr=count1_err,fmt=".")
plt.grid(color='black',linestyle=':')
plt.xlabel("$\\theta$ / degree")
plt.ylabel("Counts $N_1$ / $10^2$")
plt.savefig("../../TeX/figs/main/count1.pdf", bbox_inches='tight')
plt.show()
plt.figure(figsize=(16,9))
plt.errorbar(x=x,y=count2,yerr=count2_err,fmt=".")
plt.grid(color='black',linestyle=':')
plt.xlabel("$\\theta$ / degree")
plt.ylabel("Counts $N_2$ / $10^2$")
plt.savefig("../../TeX/figs/main/count2.pdf", bbox_inches='tight')
plt.show()

coincidence = (y-nr)*count2[0]/count2
coincidence_err = np.sqrt((count2[0]/count2*y_err)**2+(count2[0]/count2*nr_err)**2+((y-nr)*count2[0]/count2**2*count2_err)**2+((y-nr)/count2*count2_err[0])**2)


y = coincidence
y_err = coincidence_err

######
# Measurement with applied corrections
######
plt.figure(figsize=(16,9))

def func(x, a,b,c):
    return a*(1+b*(np.cos(x*np.pi/180)**2)+c*(np.cos(x*np.pi/180)**4))

#fit
popt, pcov= optimize.curve_fit(func,x,y,[1000.,0.1,0.1],y_err)
#params
fit_a=popt[0]
fit_b=popt[1]
fit_c=popt[2]
#param errors
a_err=np.sqrt(pcov[0][0])
b_err=np.sqrt(pcov[1][1])
c_err=np.sqrt(pcov[2][2])
#print fit results
print("a={:e} +/- {:e}".format(fit_a,a_err))
print("b={:e} +/- {:e}".format(fit_b,b_err))
print("c={:e} +/- {:e}".format(fit_c,c_err))



#plot fit results
xx=np.linspace(min(x)-1,max(x)+1,10000)
yy=func(xx,fit_a,fit_b,fit_c)
#calculate chi2
ychi=func(x,fit_a,fit_b,fit_c)
chisq=0
for i in range(len(x)):
    chisq+=((y[i]-ychi[i])/y_err[i])**2
print("chi2={:.4f}".format(chisq))

plt.plot(xx,yy,color="red",label="Fitted function")
plt.text(160,42,"$\chi^2=$ {:.4f}".format(chisq))
plt.errorbar(x=x,y=y,xerr=x_err,yerr=y_err,fmt=".",color="black",label="data points")
plt.xlabel("$\\theta$ / degree",fontsize=22,fontname='DejaVu Serif')
#plt.ylabel("$W(\\theta)$",fontsize=22,fontname='DejaVu Serif')
plt.ylabel("coincident count rate $n_C$ / $10^2$s$^{-1}$",fontsize=22,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')
plt.legend()
plt.savefig("../../TeX/figs/main/measurement.pdf", bbox_inches='tight')
plt.show()
