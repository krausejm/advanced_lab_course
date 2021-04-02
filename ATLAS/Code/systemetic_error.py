#!/usr/bin/env python3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import odr
from scipy import optimize
import sys
from numpy import genfromtxt


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


file = "results.txt"
data = genfromtxt(file, delimiter=';')
m_W_stat = data[1,1]
m_W_stat_error = data[1:,2]
m_W_var = data[2:,1]
m_W_var_error = data[2:,2]
data_set_names = data[2:,0]

diff = []

neg_spread = 0
pos_spread = 0

for i in range(len(data_set_names)):
    diff.append(m_W_var[i]-m_W_stat)

for i in range(len(diff)):
    if diff[i]<0:
        neg_spread += diff[i]
    else:
        pos_spread += diff[i]

print(pos_spread)
print(neg_spread)

for i in range(0, len(data_set_names)):
    print(data[i+2], diff[i])
