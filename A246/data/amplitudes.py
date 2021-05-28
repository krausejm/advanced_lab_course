#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
data = genfromtxt("amplitudes.txt", delimiter=",")
x=np.array(data[:,0])
ex=np.zeros(len(x))
y=np.array(data[:,1])
ey=np.array(data[:,2])


n=len(x)
print(n)
c=r.TCanvas()
c.SetGrid()

gr = r.TGraphErrors( n, x, y, ex,ey )
f=r.TF1("f1","[1]*x/[0]/TMath::Sqrt(1+x/[0])")
f.SetParNames("psat","offset")
f.SetParameters(100.,10.,10.)
  
leg = r.TLegend()
leg.SetFillColor(0)

gr.SetMarkerStyle(21)
gr.SetMarkerSize(2)
gr.SetLineStyle(0)
gr.Fit("f1")
leg.AddEntry(gr,"data points","pe")
gr.SetTitle("")
gr.GetXaxis().SetTitle("Power / #mu W")
gr.GetYaxis().SetTitle("A=1-T / arb. units")
gr.Draw("APE")
t=r.TLatex()
text="{:.2f}".format(f.GetChisquare()/f.GetNDF())
t.DrawLatex(1000,3,"#chi^{2}/ndf = "+text)   

#leg.SetTextSize(0.04)
leg.AddEntry(f,"fit","l")
leg.DrawClone("Same")
