#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
def lorenz(x,x0,a,b,gamma):
    return gamma**2/4*a/((x-x0)**2+(gamma/2)**2)+b


data = genfromtxt("FPI_1.csv", delimiter=",",skip_header=14)
y=np.array(data[:,0])
print(y)
x=np.array(np.arange(0,25000*8e-8,8e-8))*1e3
n=len(x)
m=len(y)

if n==m:
    c=r.TCanvas()
    c.SetGrid()
    gr=r.TGraph(n,x,y)
    gr.SetTitle("")
    gr.GetXaxis().SetTitle("rel. time / ms")
    gr.GetYaxis().SetTitle("Voltage / arb. units")
    gr.SetMarkerStyle(2)
    gr.Draw("AP")
    gr.GetXaxis().SetRangeUser(0,2*0.25)
    funcs=[]
    llimfit=[0.018*2,0.0685*2,0.12*2,0.17*2,0.22*2]
    ulimfit=[0.05*2,0.1*2,0.15*2,0.2*2,0.25*2]
    posfit=[0.02*2,0.08*2,0.13*2,0.17*2,0.23*2]
    fwhm=[]
    fwhm_err=[]
    pos=[]
    pos_err=[]

    for i in range(5):
        f=r.TF1(f"f{i}","[0]*[1]^2/4/((x-[2])^2+[1]^2/4)+[3]")
        f.SetParNames("amplitude","FWHM","pos.","offset")
        f.SetParameters(70,0.03,posfit[i],-30)
        funcs.append(f)
    
    for i in range(5):
        gr.Fit(f"f{i}","N","",llimfit[i],ulimfit[i])
        funcs[i].SetRange(llimfit[i],ulimfit[i])
        funcs[i].Draw("Same")
        dummyf=funcs[i].Clone()
        dummyf.SetRange(dummyf.GetParameter(2)-(ulimfit[i]-dummyf.GetParameter(2)),llimfit[i])
        dummyf.SetLineStyle(2)
        dummyf.DrawClone("Same")

        fwhm.append(funcs[i].GetParameter(1))
        fwhm_err.append(funcs[i].GetParError(1))
        pos.append(funcs[i].GetParameter(2))
        pos_err.append(funcs[i].GetParError(2))

leg = r.TLegend(0.1,0.83,0.48,1.)
leg.SetFillColor(0)
leg.AddEntry(funcs[0],"Fit range","l")
leg.AddEntry(dummyf,"extrapolated","l")
leg.DrawClone("Same")