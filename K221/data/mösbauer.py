import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.special import erf
from numpy import genfromtxt
import argparse
from scipy.interpolate import UnivariateSpline


def lorenz(x,x0,a,b,gamma):
    return gamma**2/4*a/((x-x0)**2+(gamma/2)**2)+b


data = genfromtxt("mösbauer.csv", delimiter=",")

poti = data[1:,0]
count_lr = data[1:,5]
delta_count_lr = data[1:,6]
time_lr=np.array(data[1:,2])/100

count_rl = data[1:,11]
delta_count_rl = data[1:,12]
time_rl=np.array(data[1:,8])/100

rounds = np.array(data[1:,1])

length = 25.1

v_lr=-length*rounds/time_lr
v_rl=length*rounds/time_rl

plt.figure(figsize=(21,9))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=30,fontname='DejaVu Serif')
plt.yticks(fontsize=30,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')


plt.errorbar(v_lr, count_lr,yerr=delta_count_lr, label="N LR", marker="x", ls="none")
plt.errorbar(v_rl, count_rl,yerr=delta_count_rl, label="N RL", marker="x", ls="none")


energy_conv = 1/(3*1e11)*14.4*1e3
#for i in range(len(v_lr)):
#    print(i, v_rl[i])
#x0,a,b,gamma

v_lr_pos = [[-5.244,500,620,-0.3],[-3.125,500,620,-0.25],[-0.940,500,620,-0.3]]
v_lr_data_frame = [[10,35], [39,61],[67, 79]]
v_lr_labels = ["|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-3/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$"]
v_lr_label_offset = [-30,-17,-27]
v_lr_max_pos = []
for i in range(len(v_lr_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]], count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]],v_lr_pos[i],delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]])
    perr = np.sqrt(np.diag(pcov))
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    x_fit = np.linspace(np.min(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),np.max(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(x_fit,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]

    x = v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y = count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y_err = delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    v_lr_max_pos.append(popt[0])
    plt.text(x_min, y_min+v_lr_label_offset[i], v_lr_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    print(str(v_lr_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3],perr[3],popt[0],perr[0],))
#print(v_lr_max_pos)


v_rl_pos = [[+5.231,520,620,1],[+3.144,500,620,0.9],[+0.940,500,620,0.4]]
v_rl_data_frame = [[10,30], [37,55],[66, 77]]
v_rl_labels = ["|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+3/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$"]
v_rl_label_y_offset=[-30,-18,-18]
v_rl_max_pos = []
for i in range(len(v_rl_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]], count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]],v_rl_pos[i],delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]])
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    perr = np.sqrt(np.diag(pcov))

    x_fit = np.linspace(np.min(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),np.max(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(x_fit,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]
    
    x = v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y = count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y_err = delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    #print(chisq)
    #print(x_min, y_min)

    #print(x_min, y_min)
    #plt.text(x_min-0.1,y_min-15, v_rl_labels[i])
    plt.text(x_min, y_min+v_rl_label_y_offset[i], v_rl_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    v_rl_max_pos.append(popt[0])
    print(str(v_rl_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3],perr[3],popt[0],perr[0],))
#print(v_rl_max_pos)
plt.legend()
plt.xlabel("$v$ / mm/s", fontsize=30,fontname='DejaVu Serif')
plt.ylabel("Counting Rate #/s", fontsize=30,fontname='DejaVu Serif')
plt.ylim(495,680)
plt.savefig("../TeX/figs/moesbauer.pdf", bbox_inches='tight')
plt.show()


#####
# In energy units
#####
print("---------------------in energy units neV---------------------")
plt.figure(figsize=(21,9))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=30,fontname='DejaVu Serif')
plt.yticks(fontsize=30,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')
plt.errorbar(v_lr*energy_conv*1e9, count_lr,yerr=delta_count_lr, label="N LR", marker="x", ls="none")
plt.errorbar(v_rl*energy_conv*1e9, count_rl,yerr=delta_count_rl, label="N RL", marker="x", ls="none")

v_lr_pos = [[-5.244,500,620,-0.3],[-3.125,500,620,-0.25],[-0.940,500,620,-0.3]]
v_lr_data_frame = [[10,35], [39,61],[67, 79]]
v_lr_labels = ["|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-3/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$"]
v_lr_label_offset = [-30,-17,-27]
v_lr_max_pos = []
v_lr_max_pos_err = []
for i in range(len(v_lr_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]], count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]],v_lr_pos[i],delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]])
    perr = np.sqrt(np.diag(pcov))
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    x_fit = np.linspace(np.min(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),np.max(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(x_fit*energy_conv*1e9,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]

    x = v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y = count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y_err = delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    v_lr_max_pos.append(popt[0])
    v_lr_max_pos_err.append(perr[0])
    plt.text(x_min*energy_conv*1e9, y_min+v_lr_label_offset[i], v_lr_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    print(str(v_lr_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3]*energy_conv*1e9,perr[3]*energy_conv*1e9,popt[0]*energy_conv*1e9,perr[0]*energy_conv*1e9))
#print(v_lr_max_pos)

v_rl_pos = [[+5.231,520,620,1],[+3.144,500,620,0.9],[+0.940,500,620,0.4]]
v_rl_data_frame = [[10,30], [37,55],[66, 77]]
v_rl_labels = ["|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+3/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$"]
v_rl_label_y_offset=[-30,-18,-18]
v_rl_max_pos = []
v_rl_max_pos_err = []
for i in range(len(v_rl_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]], count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]],v_rl_pos[i],delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]])
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    perr = np.sqrt(np.diag(pcov))

    x_fit = np.linspace(np.min(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),np.max(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(x_fit*energy_conv*1e9,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]
    
    x = v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y = count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y_err = delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    #print(chisq)
    #print(x_min, y_min)

    #print(x_min, y_min)
    #plt.text(x_min-0.1,y_min-15, v_rl_labels[i])
    plt.text(x_min*energy_conv*1e9, y_min+v_rl_label_y_offset[i], v_rl_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    v_rl_max_pos.append(popt[0])
    v_rl_max_pos_err.append(perr[0])

    print(str(v_rl_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3]*energy_conv*1e9,perr[3]*energy_conv*1e9,popt[0]*energy_conv*1e9,perr[0]*energy_conv*1e9))
#print(v_rl_max_pos)
plt.legend()
plt.xlabel("$E$ / neV", fontsize=30,fontname='DejaVu Serif')
plt.ylabel("Counting Rate #/s", fontsize=30,fontname='DejaVu Serif')
plt.ylim(495,680)
plt.savefig("../TeX/figs/moesbauer_energy.pdf", bbox_inches='tight')
plt.show()

#####
# Calculating the g-factor
#####

energy_diff = []
energy_diff_error = []
###
# g_1/2
###
energy_diff.append(-(v_rl_max_pos[2]-v_lr_max_pos[1]))
energy_diff_error.append(np.sqrt(v_rl_max_pos_err[2]**2+v_lr_max_pos_err[1]**2))

energy_diff.append(-(v_rl_max_pos[1]-v_lr_max_pos[2]))
energy_diff_error.append(np.sqrt(v_rl_max_pos_err[1]**2+v_lr_max_pos_err[2]**2))

###
# g_3/2
###
energy_diff.append(v_rl_max_pos[1]-v_rl_max_pos[2])
energy_diff_error.append(np.sqrt(v_rl_max_pos_err[1]**2+v_rl_max_pos_err[2]**2))

energy_diff.append(v_lr_max_pos[2]-v_lr_max_pos[1])
energy_diff_error.append(np.sqrt(v_lr_max_pos_err[2]**2+v_lr_max_pos_err[1]**2))

energy_diff = np.array(energy_diff)*energy_conv
energy_diff_error = np.array(energy_diff_error)*energy_conv
print("----------------------g-factor----------------------")
print("E_1/2=",np.average([energy_diff[0],energy_diff[1]])*1e9,"\pm",1/2*np.sqrt(energy_diff_error[0]**2+energy_diff_error[1]**2)*1e9)
print("E_3/2=",np.average([energy_diff[2],energy_diff[3]])*1e9,"\pm",1/2*np.sqrt(energy_diff_error[0]**2+energy_diff_error[1]**2)*1e9)

mu_N = 3.152451*1e-8
delta_m = 1
mu = 1
H=33.3 
H_err = 1
B = mu*H
B_err = mu*H_err
g=-energy_diff/(mu_N*delta_m*B)
g_error = []
for i in range(len(g)):
    g_error.append(np.sqrt((1/(mu_N*B)*energy_diff_error[i])**2+(energy_diff[i]/(mu_N*B**2)*B_err)**2))
print("g_1/2=",np.average([g[0],g[1]]),"\pm",1/2*np.sqrt(g_error[0]**2+g_error[1]**2))
print("g_3/2=",np.average([g[2],g[3]]),"\pm",1/2*np.sqrt(g_error[0]**2+g_error[1]**2))

print("ratio=",np.average([g[0],g[1]])/np.average([g[2],g[3]]),"\pm",np.sqrt((1/np.average([g[2],g[3]])*1/2*np.sqrt(g_error[0]**2+g_error[1]**2)**2+(np.average([g[0],g[1]])/np.average([g[2],g[3]])**2*1/2*np.sqrt(g_error[0]**2+g_error[1]**2))**2)))

#####
# Mirrored
#####
print("---------------------in energy units neV---------------------")
plt.figure(figsize=(10,9))
plt.minorticks_on()
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['mathtext.rm'] = 'serif'
font={'family' : 'serif','size'   : 22}
plt.rc("font",**font)
plt.xticks(fontsize=30,fontname='DejaVu Serif')
plt.yticks(fontsize=30,fontname='DejaVu Serif')
plt.grid(color='black',linestyle=':')
plt.errorbar(-v_lr*energy_conv*1e9, count_lr,yerr=delta_count_lr, label="N LR", marker="x", ls="none")
plt.errorbar(v_rl*energy_conv*1e9, count_rl,yerr=delta_count_rl, label="N RL", marker="x", ls="none")

v_lr_pos = [[-5.244,500,620,-0.3],[-3.125,500,620,-0.25],[-0.940,500,620,-0.3]]
v_lr_data_frame = [[10,35], [39,61],[67, 79]]
v_lr_labels = ["|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-3/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$","|1/2,-1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$"]
v_lr_label_offset = [-30,-17,-27]
v_lr_max_pos = []
v_lr_max_pos_err = []
for i in range(len(v_lr_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]], count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]],v_lr_pos[i],delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]])
    perr = np.sqrt(np.diag(pcov))
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    x_fit = np.linspace(np.min(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),np.max(v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(-x_fit*energy_conv*1e9,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]

    x = v_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y = count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    y_err = delta_count_lr[v_lr_data_frame[i][0]:v_lr_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    v_lr_max_pos.append(popt[0])
    v_lr_max_pos_err.append(perr[0])
    #plt.text(x_min*energy_conv*1e9, y_min+v_lr_label_offset[i], v_lr_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    #print(str(v_lr_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3]*energy_conv*1e9,perr[3]*energy_conv*1e9,popt[0]*energy_conv*1e9,perr[0]*energy_conv*1e9))
#print(v_lr_max_pos)

v_rl_pos = [[+5.231,520,620,1],[+3.144,500,620,0.9],[+0.940,500,620,0.4]]
v_rl_data_frame = [[10,30], [37,55],[66, 77]]
v_rl_labels = ["|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+3/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,+1/2$\\rangle$","|1/2,+1/2$\\rangle$ $\\rightarrow$ |3/2,-1/2$\\rangle$"]
v_rl_label_y_offset=[-30,-18,-18]
v_rl_max_pos = []
v_rl_max_pos_err = []
for i in range(len(v_rl_pos)):
    popt, pcov= optimize.curve_fit(lorenz,v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]], count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]],v_rl_pos[i],delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]])
    #print("FWHM: "+str(popt[3]*energy_conv/2))
    perr = np.sqrt(np.diag(pcov))

    x_fit = np.linspace(np.min(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),np.max(v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]),100)
    y_fit = lorenz(x_fit,popt[0],popt[1],popt[2],popt[3])
    plt.plot(x_fit*energy_conv*1e9,y_fit, color="black")
    y_min=np.min(y_fit)
    x_min=0
    for j in range(len(y_fit)):
        if y_min==y_fit[j]:
            x_min = x_fit[j]
    
    x = v_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y = count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    y_err = delta_count_rl[v_rl_data_frame[i][0]:v_rl_data_frame[i][1]]
    ychi=lorenz(x,popt[0],popt[1],popt[2],popt[3])
    chisq=0
    for z in range(len(x)):
        chisq+=((y[z]-ychi[z])/y_err[z])**2
    chisq=chisq/(len(x)-4)
    #print(chisq)
    #print(x_min, y_min)

    #print(x_min, y_min)
    #plt.text(x_min-0.1,y_min-15, v_rl_labels[i])
    #plt.text(x_min*energy_conv*1e9, y_min+v_rl_label_y_offset[i], v_rl_labels[i]+"\n$\\chi^2$/ndf=%.1f"%(chisq), fontsize=15, ha="center")#v_lr_labels[i])
    v_rl_max_pos.append(popt[0])
    v_rl_max_pos_err.append(perr[0])

    #print(str(v_rl_labels[i])+"& %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f"%(popt[1],perr[1],popt[2],perr[2],popt[3]*energy_conv*1e9,perr[3]*energy_conv*1e9,popt[0]*energy_conv*1e9,perr[0]*energy_conv*1e9))
#print(v_rl_max_pos)
plt.legend()
plt.xlabel("$E$ / neV", fontsize=30,fontname='DejaVu Serif')
plt.ylabel("Counting Rate #/s", fontsize=30,fontname='DejaVu Serif')
plt.ylim(495,680)
plt.savefig("../TeX/figs/moesbauer_mirrored.pdf", bbox_inches='tight')
plt.show()

isomeric_error = 1/2*np.sqrt(np.sum(np.array(list(v_rl_max_pos_err)+list(v_lr_max_pos_err))**2))
print("isomeric shift: ", np.average(list(v_rl_max_pos)+list(v_lr_max_pos))*energy_conv*1e9,isomeric_error*energy_conv*1e9)