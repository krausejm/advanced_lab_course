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
data = genfromtxt(file, delimiter=',')
sim_wmass = data[1:-1,1]
half_max = data[1:-1,2]
half_max_error = data[1:-1,3]
half_max_atlas = data[-1,2]
half_max_atlas_error = data[-1,3]
print(half_max_atlas_error)
#print(sim_wmass,half_max,half_max_error,half_max_atlas,half_max_atlas_error)
plt.errorbar(x=sim_wmass, y=half_max, yerr=half_max_error, fmt='.', zorder=2, label = "Simulated datapoints")

p,pcov = optimize.curve_fit(func_lin,sim_wmass, half_max,[0,0],half_max_error)

a, b = p
a_err, b_err = [np.sqrt(pcov[0][0]),np.sqrt(pcov[1][1])]


x = np.linspace(sim_wmass[0]-1,sim_wmass[-1]+1,1000)
y = func_lin(x, a,b)
ychi=func_lin(sim_wmass,a,b)
chisq=0
for i in range(len(half_max)):
    chisq+=((half_max[i]-ychi[i])/half_max_error[i])**2

cov_err=pcov[0][1]
if(sys.argv[1][11:-4]=="Zee"):
    sim_wmass[-1]=93
    x = np.linspace(sim_wmass[0]-1,sim_wmass[-1]+1,1000)
    y = func_lin(x, a,b)

m_w=(half_max_atlas-b)/a
m_w_error=np.sqrt(2*(half_max_atlas-b)/a**3*cov_err+(1/a*half_max_atlas_error)**2+(1/a*b_err)**2+((half_max_atlas-b)/a**2*a_err)**2)
#m_w_error=np.sqrt((1/a*half_max_atlas_error)**2+(1/a*b_err)**2+((half_max_atlas-b)/a**2*a_err)**2) # Wie wir es normaler weise berechnen würden
print(m_w,"+-",m_w_error)
print("chi2=",chisq)
plt.plot(x,y, label="$x_{HM}(m)=(%.3f\pm%.3f)\cdot m + (%.3f\pm%.3f)$GeV"%(a,a_err,b,b_err))
plt.text(81,42,"$\chi^2$={:.4f}".format(chisq))
if(sys.argv[1][11:-4]!="Zee"):
     plt.errorbar(x=m_w, y=half_max_atlas, xerr=m_w_error, yerr=half_max_atlas_error, fmt='', color="black",label = "$m_{W}$=(%.3f$\pm$%.3f) GeV"%(m_w, m_w_error))
else:
     plt.errorbar(x=m_w, y=half_max_atlas, xerr=m_w_error, yerr=half_max_atlas_error, fmt='', color="black",label = "$m_{Z}$=(%.3f$\pm$%.3f) GeV"%(m_w, m_w_error))

plt.legend(bbox_to_anchor=(1,-0.2))
plt.ylabel("Half Maximum $x_{HM}$/ GeV")
plt.xlabel("$m_{W}$ / GeV")
plt.savefig("../TeX/P1_pics/gauge_results/"+sys.argv[1][11:-4]+".pdf", bbox_inches='tight')
#plt.show()
results = open('results.txt', 'a')
results.write(str(sys.argv[1][11:-4])+";"+str(m_w)+";"+str(m_w_error)+"\n")
results.close()