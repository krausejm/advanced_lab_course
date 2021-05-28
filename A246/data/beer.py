#/bin/usr/env python3
import numpy as np
from numpy import genfromtxt
import ROOT as r
data = genfromtxt("amplitudes.csv", delimiter="\t")
x=np.array(data[0,:])
ex=np.zeros(len(x))
y=np.array(data[1,:])
ey=np.array(data[2,:])


n=len(x)

c=r.TCanvas()
c.SetGrid()

gr = r.TGraphErrors( n, x, y, ex,ey )
#f=r.TF1(f"f{i}","pol1")
#f.SetParameters(1,1)
  
leg = r.TLegend(0.1,0.73,0.58,1.)
leg.SetFillColor(0)

gr.SetMarkerStyle(21)
gr.SetMarkerSize(2)
gr.SetLineStyle(0)
gr.Fit("f1")
leg.AddEntry(gr,"data points","pe")

gr.GetXaxis().SetTitle("Power / #mu W")
gr.GetYaxis().SetTitle("A=1-T / arb. units")
gr.Draw("APE")
   

leg.SetTextSize(0.04)
#leg.AddEntry(funcs[0],"Law of Lambert-Beer","l")
leg.DrawClone("Same")





    


