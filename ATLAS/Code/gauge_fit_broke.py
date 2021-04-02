import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
import scipy
from scipy import stats
from uncertainties import unumpy
import uncertainties.unumpy as unp
from uncertainties import ufloat
import scipy.odr as sodr

def lin_func(p, x):
     m, c = p
     return m * x + c

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

model = sodr.Model(lin_func)
fit_data = sodr.RealData(half_max[0:], sim_wmass[0:], sx=half_max_error[0:])
odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
out = odr.run()
a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]
x_plot= np.linspace(half_max[0],half_max[-1],1000)
y_fit = a * x_plot + b


plt.errorbar(x=half_max, y=sim_wmass, xerr=half_max_error, fmt='x', zorder=2, label = "Simulated datapoints")
plt.plot(x_plot, y_fit, label="$m(x_{HM})=(%.3f\pm%.3f)\cdot x_{HM} + (%.3f\pm%.3f)$GeV"%(unumpy.nominal_values(a),unumpy.std_devs(a),unumpy.nominal_values(b),unumpy.std_devs(b)))

a = ufloat(a, err_a)
b = ufloat(b, err_b)
half_max_atlas = ufloat(half_max_atlas, half_max_atlas_error)

m_w = a*half_max_atlas+b
if(sys.argv[1][11:-4]!="Zee"):
     plt.errorbar(x=unumpy.nominal_values(half_max_atlas), y=unumpy.nominal_values(m_w), xerr=unumpy.std_devs(half_max_atlas), yerr=unumpy.std_devs(m_w), fmt='', color="black", label = "$m_{W}$=(%.3f$\pm$%.3f) GeV"%(unumpy.nominal_values(m_w),unumpy.std_devs(m_w)))
else:
     plt.errorbar(x=unumpy.nominal_values(half_max_atlas), y=unumpy.nominal_values(m_w), xerr=unumpy.std_devs(half_max_atlas), yerr=unumpy.std_devs(m_w), fmt='', color="black", label = "$m_{Z}$=(%.3f$\pm$%.3f) GeV"%(unumpy.nominal_values(m_w),unumpy.std_devs(m_w)))
plt.legend(bbox_to_anchor=(1,-0.2))
plt.xlabel("Half Maximum / GeV")
plt.ylabel("$m_{W}$ / GeV")
plt.savefig("../TeX/P1_pics/gauge_results/"+sys.argv[1][11:-4]+".pdf", bbox_inches='tight')
plt.show()
