#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
def lorenz(x,x0,a,b,gamma):
    return gamma**2/4*a/((x-x0)**2+(gamma/2)**2)+b


data = genfromtxt("short.csv", delimiter=",",skip_header=14)
y=np.array(data[:,0])
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
    gr.GetXaxis().SetRangeUser(2*3,2*6.5)
    gr.GetYaxis().SetTitle("Voltage / arb. units")
    gr.SetMarkerStyle(2)
    gr.Draw("AP")
    funcs=[]
  


    llimfit=[2*3.4,2*4.25,2*5.35,11.8]
    ulimfit=[2*3.8,2*5.,2*5.8,12.6]
    posfit=[2*3.6,2*4.6,2*5.2,12.2]
    amp_fit=[-30,-75,-140,-10]
    offset_fit=[-10,30,50,60]
    sig=[]
    sig_err=[]
    pos=[]
    pos_err=[]
    amp=[]
    amp_err=[]
    for i in range(4):    
        f=r.TF1(f"f{i}","[0]*TMath::Exp(-((x-[1])/2/[2])^2)+[3]*x+[4]")
        f.SetParNames("amplitude","pos.","sigma","offset")
        f.SetParameters(amp_fit[i],posfit[i],2*0.2,0,offset_fit[i])
        funcs.append(f)
 
        

    for i in range(4):
  
        gr.Fit(f"f{i}","N","",llimfit[i],ulimfit[i])
        funcs[i].SetRange(llimfit[i],ulimfit[i])
        funcs[i].Draw("Same")
        dummyf=funcs[i].Clone()
        dummy_mu=dummyf.GetParameter(1)
        dummy_sig=dummyf.GetParameter(2)
        dummyf.SetRange(dummy_mu-5*dummy_sig,dummy_mu+5*dummy_sig)
        dummyf.SetLineStyle(2)
        dummyf.DrawClone("Same")

        amp.append(funcs[i].GetParameter(0))
        amp_err.append(funcs[i].GetParError(0))
        sig.append(funcs[i].GetParameter(2))
        sig_err.append(funcs[i].GetParError(2))
        pos.append(funcs[i].GetParameter(1))
        pos_err.append(funcs[i].GetParError(1))

leg = r.TLegend(0.1,0.83,0.48,1.)
leg.SetFillColor(0)
leg.AddEntry(f,"Fit range","l")
leg.AddEntry(dummyf,"extrapolated 5#sigma interval","l")
leg.DrawClone("Same")
t1=r.TLatex()
t1.SetTextAlign(21)
t1.SetTextAngle(270)
t1.DrawLatex(2*3.25,-60,"#scale[1]{ ^{87}Rb 1 #rightarrow 2}")
t1.DrawLatex(2*3.75,-30,"#scale[1]{ ^{87}Rb 1 #rightarrow 1}")
t1.DrawLatex(2*4.3,-70,"#scale[1]{ ^{85}Rb 2 #rightarrow 2,3}")
t1.DrawLatex(2*5.4,-100,"#scale[1]{ ^{85}Rb 3 #rightarrow 2,3}")
t1.DrawLatex(2*5.75,-30,"#scale[1]{ ^{87}Rb 2 #rightarrow 2}")
t1.DrawLatex(2*6.1,-30,"#scale[1]{ ^{87}Rb 2 #rightarrow 1}")