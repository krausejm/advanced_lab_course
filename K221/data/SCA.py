import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.special import erf
from numpy import genfromtxt
import argparse

data = genfromtxt("spectrum.csv", delimiter=",")

sca1_bin_low = data[1:,0]
sca1_bin_up = data[1:,1]
sca1 = data[1:,2]


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

plt.hist(sca1_bin_low, weights=sca1, bins=len(sca1),edgecolor='black',label="Count rates N")
#plt.vlines(x=600, ymin=-100, ymax=10000,linestyles="dashed")
#plt.vlines(x=1000, ymin=-100, ymax=10000,linestyles="dashed")
plt.ylim(0,6200)
plt.fill_between([1300,2000], [10000,10000], color='orange',label="Selected SCA window")
plt.xlim(0, np.max(sca1_bin_up))
plt.xlabel("SCA Window / Ch.", fontsize=20,fontname='DejaVu Serif')
plt.ylabel("Counts N", fontsize=20,fontname='DejaVu Serif')
plt.legend()
plt.text(1635,1720,"14.4 keV",ha="center")
plt.text(730,3130,"EC-cascade\n$\\approx$ 6keV",ha="center")
plt.text(2300,460,"Simultaneous\nEC and 14.4 keV\n measurement",ha="center")
plt.text(230,5000,"Noise")
plt.xlim(100, 3200)
plt.savefig("../TeX/figs/SCA.pdf", bbox_inches='tight')

plt.show()

