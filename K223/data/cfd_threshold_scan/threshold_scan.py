#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse



my_data = genfromtxt("threshold_scan.txt", delimiter="\t")

# data with source
x1_source= np.array(my_data[1:16, 0])
y1_source=np.array(my_data[1:16, 1])

x1_source_error = np.sqrt(x1_source)
y1_source_error = np.sqrt(y1_source)

x2_source= np.array(my_data[1:16, 3])
y2_source=np.array(my_data[1:16, 4])

x2_source_error = np.sqrt(x2_source)
y2_source_error = np.sqrt(y2_source)

#data without source
x1_no_source= np.array(my_data[17:, 0])
y1_no_source=np.array(my_data[17:, 1])

x1_no_source_error = np.sqrt(x1_no_source)
y1_no_source_error = np.sqrt(y1_no_source)

x2_no_source= np.array(my_data[17:, 3])
y2_no_source=np.array(my_data[17:, 4])

x2_no_source_error = np.sqrt(x2_no_source)
y2_no_source_error = np.sqrt(y2_no_source)

xerr=[0.3 for i in range(len(x1_no_source))]

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




plt.errorbar(x1_source,y1_source,xerr=xerr,yerr=y1_source_error,fmt=".", label="CFD 1 counts with source")
plt.errorbar(x1_no_source,y1_no_source,xerr=xerr,yerr=y1_no_source_error,fmt=".", label="CFD 1 counts without source")

plt.yscale("log")
plt.xlabel('CFD Setting', fontsize=20)
plt.ylabel('Counts N', fontsize=20)
plt.vlines(x=20,ymin=0,ymax=np.max(y2_source)*10, linestyles="dashed", colors="gray", label="set value 20")
plt.ylim(0,np.max(y2_source)*3)
plt.legend(bbox_to_anchor=(1,-0.2))
plt.savefig("../../TeX/figs/CFD/CFD1.pdf", bbox_inches='tight')
plt.show()

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

plt.errorbar(x2_source,y2_source,xerr=xerr,yerr=y2_source_error,fmt=".", label="CFD 2 counts with source")
plt.errorbar(x2_no_source,y2_no_source,xerr=xerr,yerr=y2_no_source_error,fmt=".", label="CFD 2 counts without source")

plt.yscale("log")
plt.xlabel('CFD Setting', fontsize=20)
plt.ylabel('Counts N', fontsize=20)
plt.vlines(x=20,ymin=0,ymax=np.max(y2_source)*10, linestyles="dashed", colors="gray", label="set value 20")
plt.ylim(0,np.max(y2_source)*3)
plt.legend(bbox_to_anchor=(1,-0.2))
plt.savefig("../../TeX/figs/CFD/CFD2.pdf", bbox_inches='tight')
plt.show()
