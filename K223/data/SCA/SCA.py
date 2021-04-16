import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.special import erf
from numpy import genfromtxt
import argparse

data = genfromtxt("SCA.csv", delimiter=",")

sca1_bin_low = data[1:,0]
sca1_bin_up = data[1:,1]
sca1 = data[1:,2]

sca2_bin_low = data[1:,3]
sca2_bin_up = data[1:,4]
sca2 = data[1:,5]

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
plt.vlines(x=600, ymin=-100, ymax=10000,linestyles="dashed")
plt.vlines(x=1000, ymin=-100, ymax=10000,linestyles="dashed")
plt.ylim(0,6200)
plt.fill_between([600,1000], [10000,10000], color='orange',label="Selected SCA1 window")
plt.xlim(0, np.max(sca1_bin_up))
plt.xlabel("SCA1 Voltage window", fontsize=20)
plt.ylabel("Counts N", fontsize=20)
plt.legend()
plt.savefig("../../TeX/figs/SCA/SCA1.pdf", bbox_inches='tight')
plt.show()


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



plt.hist(sca2_bin_low, weights=sca2, bins=len(sca2),edgecolor='black',label="Count rates N")
plt.vlines(x=600, ymin=-100, ymax=10000,linestyles="dashed")
plt.vlines(x=1000, ymin=-100, ymax=10000,linestyles="dashed")
plt.fill_between([600,1000], [10000,10000], color='orange',label="Selected SCA2 window")
plt.ylim(0,6200)
plt.xlim(0, np.max(sca2_bin_up))
plt.xlabel("")
plt.xlabel("SCA2 Voltage window", fontsize=20)
plt.ylabel("Counts N", fontsize=20)
plt.savefig("../../TeX/figs/SCA/SCA2.pdf", bbox_inches='tight')
plt.legend()
plt.show()