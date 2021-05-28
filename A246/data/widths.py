#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
import pandas as pd
txt=["fourth.csv","third.csv","sixth.csv","seventh.csv","fifth.csv","second.csv","first.csv"]
y=[]
graphs=[]
#c=r.TCanvas()
#c.SetGrid()
#c.Divide(2,3)
x=np.arange(0,25000*8e-08,8e-08)*1e3
n=len(x)
ampdata = genfromtxt("sort_amps.txt", delimiter="\t")
power=np.array(ampdata[:,0])
funcs=[]
  


llimfit=[1.03,1.099,1.16,0.9,1.13,1.05]
ulimfit=[1.1,1.15,1.21,1.,1.23,1.175]
posfit=[1.05,1.125,1.121,0.925,1.125,1.1]
amp_fit=[0.,10.,10.,15.,40.,50.]
offset_fit=[-50.,-70.,-70.,-50,-70,-50]
fwhm=[]
fwhm_err=[]


for t in txt:
    data=genfromtxt(t, delimiter=",",skip_header=14)
    tmpy=np.array(data[:,0])
    y.append(tmpy)

    
for i in range(len(y)):
    if i!=4:
        gr=r.TGraph( n, x, np.array(y[i]))
        gr.GetXaxis().SetTitle("rel. time / ms")
        gr.GetYaxis().SetTitle("voltage / arb. units")
        gr.SetTitle("P={:.2f} W".format(power[i]))
        graphs.append(gr)
for i in range(6):
    f=r.TF1(f"f{i}","[0]*([1]/2)^2/((x-[2])^2+([1]/2)^2)+[3]")
    f.SetParNames("amplitude","fwhm","pos","offset")
    f.SetParameters(amp_fit[i],2*0.2,posfit[i],offset_fit[i])
    funcs.append(f)

for i in range(6):
    #c.cd(i+1)
    #r.gPad.SetGrid()
    #graphs[i].Draw("AP")
    if i ==3:
        graphs[3].GetXaxis().SetRangeUser(0.8,1.2)
    else:
        graphs[i].GetXaxis().SetRangeUser(1,1.4)
    graphs[i].Fit(f"f{i}","N","",llimfit[i],ulimfit[i])
    funcs[i].SetRange(llimfit[i],ulimfit[i])
    funcs[i].Draw("Same")
    dummyf=funcs[i].Clone()
    dummy_pos=dummyf.GetParameter(2)
    dummy_fwhm=dummyf.GetParameter(1)
    dummyf.SetRange(dummy_pos-2*dummy_fwhm,dummy_pos+2*dummy_fwhm)
    dummyf.SetLineStyle(2)
    #dummyf.DrawClone("Same")
    fwhm.append(funcs[i].GetParameter(1))
    fwhm_err.append(funcs[i].GetParError(1))
c=r.TCanvas()
c.SetGrid()
power=np.delete(power,4)
d={'power / micro W':power,'FWHM / MHz': fwhm, 'err / MHz':fwhm_err}
df=pd.DataFrame(data=d)
df.to_csv('widths.txt')

err=np.array(fwhm_err)*np.array(fwhm)*2
graph=r.TGraphErrors(len(power),power,np.array(fwhm)**2,np.zeros(len(power)),err)
graph.SetMarkerStyle(21)
graph.GetXaxis().SetTitle("Power / #mu W")
graph.GetYaxis().SetTitle("(#Delta #nu)^{2} / MHz^{2}")
func=r.TF1("f1","pol1")
graph.Fit("f1")
graph.Draw("AP")
t=r.TLatex()
text="{:.2f}".format(func.GetChisquare()/func.GetNDF())
t.DrawLatex(1000,0.002,"#chi^{2}/ndf = "+text)   

#leg.SetTextSize(0.04)
leg = r.TLegend()
leg.SetFillColor(0)
leg.AddEntry(graph,"data points","pe")
leg.AddEntry(func,"fit","l")
leg.DrawClone("Same")






"""
t=r.TLatex()
text="{:.2f}".format(f.GetChisquare()/f.GetNDF())
t.DrawLatex(1000,3,"#chi^{2}/ndf = "+text)   

#leg.SetTextSize(0.04)
leg.AddEntry(f,"fit","l")
leg.DrawClone("Same")"""