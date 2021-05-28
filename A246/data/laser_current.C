{

/*void rescaleaxis(TGraphErrors *g,double scale, double n){
    //"""This function rescales the x-axis on a TGraph."""
    int N = g->GetN();
    double* x = g->GetX();
    for(int i = 1; i< N+1; i++){
        x[i] = scale*x[i]+n;
    }
}
void rescaleyaxis(TGraphErrors *g,double scale, double n){
    //"""This function rescales the y-axis on a TGraph."""
    int N = g->GetN();
    double* y = g->GetY();
    for(int i = 1; i< N+1; i++){
        y[i] = scale*y[i]+n;
    }
}



void fit(){*/
auto c=new TCanvas();c->SetGrid();

TGraph *graph0 = new TGraphErrors("./laser_current.txt","%lg %lg %lg");
graph0->SetMarkerStyle(kFullSquare);
graph0->Draw("AP");
graph0->SetTitle("");
graph0->GetYaxis()->SetTitle("Power /#mu W");
graph0->GetXaxis()->SetTitle("Laser Current / mA");
TF1* f1=new TF1("f1","pol1",0,220);
graph0->Fit("f1","N","",60,200);
f1->Draw("Same");

TLatex* text = new TLatex();
double chisqndf=f1->GetChisquare()/f1->GetNDF();
text->DrawLatex(20,300,Form("#chi^{2} / ndf =%.2f",chisqndf));
TLegend* leg = new TLegend();
leg->SetFillColor(0);
leg->AddEntry(graph0,"measured values","pe");
leg->AddEntry(f1,"linear fit","l");
leg->Draw("Same");

//}
}
