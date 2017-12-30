clear all;
close all;
pkg load signal;
load('This_Side_Up_intervalo');
nz=400; % Zeros iniciais
x=[x(1).*ones(nz,1);x;x(length(x)).*ones(nz,1)] -mean(x);
y=[y(1).*ones(nz,1);y;y(length(y)).*ones(nz,1)] -mean(y);

n=3; % ordem do filtro/2

f=100/7 ;% Sample rate
%Band Pass all
f1=1/7; %F start
f2=3;   %F Stop
%Low pass
[A,B] = butter(n,[f2]/(f/2));
X=filter(A,B,x);
Y=filter(A,B,y);
%High pass
[C,D] = butter(n,[f1]/(f/2),'high');
X1=filter(C,D,X);
Y1=filter(C,D,Y);

%%===================BATIMENTO====================
%Band Pass Batimento 
f_1=0.8;
f_2=2;
%Low pass
[A,B] = butter(n,[f_2]/(f/2));
X_b=filter(A,B,x);
Y_b=filter(A,B,y);
%High pass
[C,D] = butter(n,[f_1]/(f/2),'high');
X1_b=filter(C,D,X_b);
Y1_b=filter(C,D,Y_b);

%%=================RESPIRACAO=====================
%Band Pass Respiracao
f_1=0.1;
f_2=0.8;
%Low pass
[A,B] = butter(n,[f_2]/(f/2));
X_r=filter(A,B,x);
Y_r=filter(A,B,y);
%High pass
[C,D] = butter(n,[f_1]/(f/2),'high');
X1_r=filter(C,D,X_r);
Y1_r=filter(C,D,Y_r);

%=====================SHOW========================
%show respiracao
%subplot(2,1,1);plot([X]);
%subplot(2,1,2);plot([X1_r.^3]);


%show batimento
X1_b(400:425)=0;
subplot(2,1,1);plot([cumsum(X1_b) X]);
subplot(2,1,2);plot([cumsum(X1_b).^3]);
