#include "math.h"
#include "TMath.h"

double ElecCalib(double e_raw, double pt, double eta, 
		 double phi, double etiso, double eoverp, double mindrjet)
{
  double dummy=pt*eta*phi*etiso*eoverp*mindrjet;
  double z_mass = 91.1876;
  double energy = e_raw;
  if ((eta)<-2.4) energy = energy * z_mass/86.27;
  else if (eta<-2.3 && eta>=-2.4) energy = energy * z_mass/87.11;
  else if (eta<-2.2 && eta>=-2.3) energy = energy * z_mass/87.64;
  else if (eta<-2.1 && eta>=-2.2) energy = energy * z_mass/88.42;
  else if (eta<-2.0 && eta>=-2.1) energy = energy * z_mass/89.30;
  else if (eta<-1.9 && eta>=-2.0) energy = energy * z_mass/89.44;
  else if (eta<-1.8 && eta>=-1.9) energy = energy * z_mass/89.55;
  else if (eta<-1.7 && eta>=-1.8) energy = energy * z_mass/90.25;
  else if (eta<-1.6 && eta>=-1.7) energy = energy * z_mass/88.73;
  else if (eta<-1.5 && eta>=-1.6) energy = energy * z_mass/89.42;
  else if (eta<-1.4 && eta>=-1.5) energy = energy * z_mass/87.31;
  else if (eta<-1.3 && eta>=-1.4) energy = energy * z_mass/89.53;
  else if (eta<-1.2 && eta>=-1.3) energy = energy * z_mass/89.44;
  else if (eta<-1.1 && eta>=-1.2) energy = energy * z_mass/89.26;
  else if (eta<-1.0 && eta>=-1.1) energy = energy * z_mass/89.58;
  else if (eta<-0.9 && eta>=-1.0) energy = energy * z_mass/89.08;
  else if (eta<-0.8 && eta>=-0.9) energy = energy * z_mass/89.56;
  else if (eta<-0.7 && eta>=-0.8) energy = energy * z_mass/89.54;
  else if (eta<-0.6 && eta>=-0.7) energy = energy * z_mass/89.82;
  else if (eta<-0.5 && eta>=-0.6) energy = energy * z_mass/89.82;
  else if (eta<-0.4 && eta>=-0.5) energy = energy * z_mass/90.20;
  else if (eta<-0.3 && eta>=-0.4) energy = energy * z_mass/89.88;
  else if (eta<-0.2 && eta>=-0.3) energy = energy * z_mass/90.06;
  else if (eta<-0.1 && eta>=-0.2) energy = energy * z_mass/89.82;
  else if (eta<-0.0 && eta>=-0.1) energy = energy * z_mass/89.98;
  else if (eta>=0.0 && eta<0.1) energy = energy * z_mass/89.78;
  else if (eta>=0.1 && eta<0.2) energy = energy * z_mass/89.99;
  else if (eta>=0.2 && eta<0.3) energy = energy * z_mass/89.92;
  else if (eta>=0.3 && eta<0.4) energy = energy * z_mass/89.83;
  else if (eta>=0.4 && eta<0.5) energy = energy * z_mass/89.96;
  else if (eta>=0.5 && eta<0.6) energy = energy * z_mass/89.9;
  else if (eta>=0.6 && eta<0.7) energy = energy * z_mass/89.72;
  else if (eta>=0.7 && eta<0.8) energy = energy * z_mass/89.59;
  else if (eta>=0.8 && eta<0.9) energy = energy * z_mass/89.33;
  else if (eta>=0.9 && eta<1.0) energy = energy * z_mass/89.39;
  else if (eta>=1.0 && eta<1.1) energy = energy * z_mass/89.30;
  else if (eta>=1.1 && eta<1.2) energy = energy * z_mass/89.49;
  else if (eta>=1.2 && eta<1.3) energy = energy * z_mass/89.04;
  else if (eta>=1.3 && eta<1.4) energy = energy * z_mass/89.81;
  else if (eta>=1.4 && eta<1.5) energy = energy * z_mass/89.06;
  else if (eta>=1.5 && eta<1.6) energy = energy * z_mass/89.1;
  else if (eta>=1.6 && eta<1.7) energy = energy * z_mass/88.7;
  else if (eta>=1.7 && eta<1.8) energy = energy * z_mass/90.12;
  else if (eta>=1.8 && eta<1.9) energy = energy * z_mass/90.1;
  else if (eta>=1.9 && eta<2.0) energy = energy * z_mass/89.6;
  else if (eta>=2.0 && eta<2.1) energy = energy * z_mass/88.96;
  else if (eta>=2.1 && eta<2.2) energy = energy * z_mass/88.5;
  else if (eta>=2.2 && eta<2.3) energy = energy * z_mass/87.5;
  else if (eta>=2.3 && eta<2.4) energy = energy * z_mass/87.36;
  else if (eta>=2.4 && eta<2.5) energy = energy * z_mass/88.0;



  if((phi)<-3.14*11/12) energy = energy * z_mass/90.85;
  else if (phi>=-3.14*11/12 && phi<-3.14*10/12) energy = energy * z_mass/91.4;
  else if (phi>=-3.14*10/12 && phi<-3.14*9/12) energy = energy * z_mass/91.22;
  else if (phi>=-3.14*9/12 && phi<-3.14*8/12) energy = energy * z_mass/91.1;
  else if (phi>=-3.14*8/12 && phi<-3.14*7/12) energy = energy * z_mass/91.08;
  else if (phi>=-3.14*7/12 && phi<-3.14*6/12) energy = energy * z_mass/91.08;
  else if (phi>=-3.14*6/12 && phi<-3.14*5/12) energy = energy * z_mass/91.29;
  else if (phi>=-3.14*5/12 && phi<-3.14*4/12) energy = energy * z_mass/91.33;
  else if (phi>=-3.14*4/12 && phi<-3.14*3/12) energy = energy * z_mass/90.91;
  else if (phi>=-3.14*3/12 && phi<-3.14*2/12) energy = energy * z_mass/91.19;
  else if (phi>=-3.14*2/12 && phi<-3.14*1/12) energy = energy * z_mass/91.4;
  else if (phi>=-3.14*1/12 && phi<-3.14*0/12) energy = energy * z_mass/90.92;
  else if (phi>=-3.14*0/12 && phi<+3.14*1/12) energy = energy * z_mass/90.84;
  else if (phi>=3.14*1/12 && phi<+3.14*2/12) energy = energy * z_mass/91.19;
  else if (phi>=3.14*2/12 && phi<+3.14*3/12) energy = energy * z_mass/91.4;
  else if (phi>=3.14*3/12 && phi<+3.14*4/12) energy = energy * z_mass/91.11;
  else if (phi>=3.14*4/12 && phi<+3.14*5/12) energy = energy * z_mass/91.32;
  else if (phi>=3.14*5/12 && phi<+3.14*6/12) energy = energy * z_mass/91.13;
  else if (phi>=3.14*6/12 && phi<+3.14*7/12) energy = energy * z_mass/91.17;
  else if (phi>=3.14*7/12 && phi<+3.14*8/12) energy = energy * z_mass/91.18;
  else if (phi>=3.14*8/12 && phi<+3.14*9/12) energy = energy * z_mass/91.09;
  else if (phi>=3.14*9/12 && phi<+3.14*10/12) energy = energy * z_mass/91.16;
  else if (phi>=3.14*10/12 && phi<+3.14*11/12) energy = energy * z_mass/91.43;
  else if (phi>=3.14*11/12) energy = energy * z_mass/90.81;

  if(pt<15) energy = energy * z_mass/88.63;
  else if (pt>=3*5 && pt < 4*5) energy = energy * z_mass/90.19;
  else if (pt>=4*5 && pt < 5*5) energy = energy * z_mass/90.47;
  else if (pt>=5*5 && pt < 6*5) energy = energy * z_mass/90.09;
  else if (pt>=6*5 && pt < 7*5) energy = energy * z_mass/90.62;
  else if (pt>=7*5 && pt < 8*5) energy = energy * z_mass/90.75;
  else if (pt>=8*5 && pt < 9*5) energy = energy * z_mass/91.32;
  else if (pt>=9*5 && pt < 10*5) energy = energy * z_mass/92.26;
  else if (pt>=10*5 && pt < 11*5) energy = energy * z_mass/92.14;
  else if (pt>=11*5 && pt < 12*5) energy = energy * z_mass/92.09;
  else if (pt>=12*5 && pt < 13*5) energy = energy * z_mass/91.96;
  else if (pt>=13*5 && pt < 14*5) energy = energy * z_mass/91.81;
  else if (pt>=14*5 && pt < 16*5) energy = energy * z_mass/91.85;
  else if (pt>=16*5) energy = energy * z_mass/91.92;

  return energy;
} 
