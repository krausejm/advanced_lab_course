#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
def lorenz(x,x0,a,b,gamma):
    return gamma**2/4*a/((x-x0)**2+(gamma/2)**2)+b


data = genfromtxt("nonlinear.csv", delimiter=",",skip_header=14)
#data1 =genfromtxt("linear.csv",delimiter=",",skip_header=14)


y=np.array(data[:,0])
#y1=np.array(data1[:,0])
#y=y1-y
print(y)
x=np.array(np.arange(0,25000*8e-07,8e-07))*1e3
n=len(x)
m=len(y)

if n==m:
    c=r.TCanvas()
    c.SetGrid()
    gr=r.TGraph(n,x,y)
    gr.SetTitle("")
    gr.GetXaxis().SetTitle("rel. time / ms")
    gr.GetXaxis().SetRangeUser(7,13)
    gr.GetYaxis().SetTitle("Voltage / arb. units")
    gr.SetMarkerStyle(2)
    gr.Draw("AP")
    funcs=[]
  


    llimfit=[7.5,8.05,9.4,9.65,11.41,11.62,12.05,12.59]
    ulimfit=[7.65,8.25,9.55,9.78,11.49,11.75,12.2,12.71]
    posfit=[7.55,8.15,9.45,9.69,11.4,11.7,12.2,12.5]
    amp_fit=[10,5,20,10,10,30,10,20]
    offset_fit=[0,15,-20,-10,-40,-60,-5,-20]
    fwhm=[]
    fwhm_err=[]
    pos=[]
    pos_err=[]
    amp=[]
    amp_err=[]
    for i in range(8):

        if i==3:
            f=r.TF1(f"f{i}","[0]*([1]/2)^2/((x-[2])^2+([1]/2)^2)+[3]*x+[4]")
            f.SetParNames("amplitude","fwhm","pos","slope","offset")
            f.SetParameters(amp_fit[i],2*0.2,posfit[i],1.,offset_fit[i])
            funcs.append(f)
        else:    
            f=r.TF1(f"f{i}","[0]*([1]/2)^2/((x-[2])^2+([1]/2)^2)+[3]")
            f.SetParNames("amplitude","fwhm","pos","offset")
            f.SetParameters(amp_fit[i],2*0.2,posfit[i],offset_fit[i])
            funcs.append(f)
        
        
        

    for i in range(8):
  
        gr.Fit(f"f{i}","N","Q",llimfit[i],ulimfit[i])
        funcs[i].SetRange(llimfit[i],ulimfit[i])
        funcs[i].Draw("Same")
        dummyf=funcs[i].Clone()
        dummy_pos=dummyf.GetParameter(2)
        dummy_fwhm=dummyf.GetParameter(1)
        dummyf.SetRange(dummy_pos-2*dummy_fwhm,dummy_pos+2*dummy_fwhm)
        dummyf.SetLineStyle(2)
        dummyf.DrawClone("Same")

        amp.append(funcs[i].GetParameter(0))
        amp_err.append(funcs[i].GetParError(0))
        fwhm.append(funcs[i].GetParameter(1))
        fwhm_err.append(funcs[i].GetParError(1))
        pos.append(funcs[i].GetParameter(2))
        pos_err.append(funcs[i].GetParError(2))

leg = r.TLegend(0.1,0.83,0.48,1.)
leg.SetFillColor(0)
leg.AddEntry(funcs[0],"Fit range","l")
leg.AddEntry(dummyf,"extrapolated ","l")
leg.DrawClone("Same")
t1=r.TLatex()
t1.SetTextAlign(21)
t1.SetTextAngle(270)
t1.DrawLatex(7.1,-20,"#scale[1]{ ^{87}Rb 1 #rightarrow 2}")
t1.DrawLatex(8.1,0,"#scale[1]{ ^{87}Rb 1 #rightarrow 1}")
t1.DrawLatex(2*4.3+0.5,-70,"#scale[1]{ ^{85}Rb 2 #rightarrow 2}")
t1.DrawLatex(2*4.3+0.5,-70,"#scale[1]{crossover}")
t1.DrawLatex(2*4.3+0.5,-70,"#scale[1]{^{85}Rb 2 #rightarrow 3}")
t1.DrawLatex(2*5.4,-100,"#scale[1]{  ^{85}Rb 3 #rightarrow 2}}")
t1.DrawLatex(2*5.4+0.5,-100,"#scale[1]{crossover}")
t1.DrawLatex(2*5.4+0.5,-100,"#scale[1]{  ^{85}Rb 3 #rightarrow 3}")
t1.DrawLatex(2*5.75,-30,"#scale[1]{ ^{87}Rb 2 #rightarrow 2}")
t1.DrawLatex(2*6.1,-30,"#scale[1]{ ^{87}Rb 2 #rightarrow 1}")

def constant(i,j,k,l,m):
    c=2.9393e3
    c_err=0.0086e3
    diff=(pos[i]-pos[j]+pos[k]-pos[l])/2
    diff_err=np.sqrt(pos_err[i]**2+pos_err[j]**2+pos_err[k]**2+pos_err[j]**2)/2
    a=c*diff
    a_err=np.sqrt((diff*c_err)**2+(c*diff_err)**2)
    return a/m, a_err/m
print(constant(6,0,7,1,4))
print(constant(1,0,7,6,4))