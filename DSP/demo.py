#
#	Headers and Libs
#
import csv							#CSV manipulators
import numpy as np					#numerical functions
from sklearn.svm import SVR			#ANN and satatistical models
import matplotlib.pyplot as plt		#plot lib
from time import gmtime, strftime	#date and times functions

#
#	Constants and global Vars
#Vars
Times = []
XData = []
YData = []
ZData = []
#Constants
N=6		#n points of memory
k=100	#n points data test
a=.5 	#sin timestep
testeModelo=0	#simulatio model flag
displayMsg=1
stDevTol= 1		#standart deviation tolerance

NpWindow=30 	#Data window size
SampleRate=20	#Sample rate of sensor
#
#	Define functions and routines
#
def get_data(filename):				# read CSV database file
	with open(filename, 'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			Times.append(float(row[0]))
			XData.append(float(row[1]))
			YData.append(float(row[2]))
			ZData.append(float(row[3]))
	return
def get_csv_data(filename):				# read CSV database file
	with open(filename, 'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			Times.append(float(row[0]))
			XData.append(float(row[1]))
			YData.append(float(row[2]))
			ZData.append(float(row[3]))
	return
def Construct_model(Data, x): 		# build estimator model with ann rbf
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models, using radial basis funcion
	data_in=Data[0:len(Data)-x]
	for u in range(1,x):
		data_in=np.column_stack((data_in,Data[u:len(Data)-x+u]))
	svr_rbf.fit(data_in,Data[x:len(Data)]) # fitting the data points in the models
	return svr_rbf	#return model
def G_detect(triAxisData): 			# detect G force
	med=[np.mean(i) for i in triAxisData]
	print med
	res=np.sqrt(np.sum(np.square(med)))
	if(res>9.6 and res<10):
		if(displayMsg):
			print "Forca G detectada"
		return True
	else:
		if(displayMsg):
			print "Forca G nao detectada"
		return False
def high_pass(triAxisData):			# delete DC and very low frequency
	mean=np.asarray([len(triAxisData[0])*[np.mean(x[0:NpWindow])] for x in triAxisData])
	for j in range(0,len(triAxisData)):
		for i in range(NpWindow,len(triAxisData[0])):
			mean[j][i]=((NpWindow-1)*mean[j][i-1] + triAxisData[j][i])/NpWindow
	return np.array(triAxisData)-mean
def plot_3(Time,triAxisData,title):	# plot 3 data on same scale
	plt.plot(Time, triAxisData[0], color= 'blue', label= 'X Data')
	plt.plot(Time, triAxisData[1], color= 'red', label= 'Y Data')
	plt.plot(Time, triAxisData[2], color= 'green', label= 'Z Data')
	plt.xlabel('Time')
	plt.ylabel('Value')
	plt.title(title)
	plt.legend()
	plt.show()
def plot_1(data,title):
    plt.plot(range(1,len(data)+1), data, color= 'blue', label= 'X Data')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(title)
    plt.legend()
    plt.show()
def to_periodic_sampled(Time, triAxisData): # convert time series data to periodic sampled data (TODO using linear interpolation)
	tmp=3*[[0]]#[np.zeros(len(Time)/2)];
	tmp[0][0]=triAxisData[0][0];
	tmp[1][0]=triAxisData[1][0];
	tmp[2][0]=triAxisData[2][0];
	i=1
	j=0
	time=0
	while (i<len(Time)):
		if(Time[i-1]<Time[i]):
			j+=1
			tmp[0].append(triAxisData[0][i])
			tmp[1].append(triAxisData[1][i])
			tmp[2].append(triAxisData[2][i])


			'''time=(Time[0]+j/SampleRate) -Time[i-1]
			tmp[0][i]=(triAxisData[0][i]-triAxisData[0][i-1])*SampleRate*time+ triAxisData[0][i-1]
			tmp[1][i]=(triAxisData[1][i]-triAxisData[1][i-1])*SampleRate*time+ triAxisData[1][i-1]
			tmp[2][i]=(triAxisData[2][i]-triAxisData[2][i-1])*SampleRate*time+ triAxisData[2][i-1]'''
		i+=1
	if(displayMsg):
		print str(j+1)+" Amostras de "+str(len(Time))+" processadas"
	return tmp
def detect_deviation(triAxisData):	# detec if standart deviation is under tolerance
		return all([np.std(x)<stDevTol for x in triAxisData])

#
#	Run Script
#
print strftime("%Y-%m-%d %H:%M:%S", gmtime())+"-Inicio do porcessamento do modelo"
get_data('sin.csv') # Load sensor database

#initial analysis
#G detect
i=-1;
flag=False
while(i<(len(Times)/NpWindow) or flag): #Search for the minimum conditions for analysis
	i+=1
	#detect G force and standart deviation
	tmp=[XData[i*NpWindow:NpWindow*(1+i)],YData[i*NpWindow:NpWindow*(1+i)],ZData[i*NpWindow:NpWindow*(1+i)]]
	flag=G_detect(tmp) and detect_deviation(tmp)
if (flag): # Minimum conditions were found
	#high pass filter
	tmp=high_pass([XData[i*NpWindow:len(Times)],YData[i*NpWindow:len(Times)],ZData[i*NpWindow:len(Times)]])
	if(displayMsg):
		plot_3(Times,tmp)	#plot data filtered
	#fft
	fft=[np.fft.rfft(x) for x in tmp]
	if(displayMsg):
		plot_3(range(0,len(fft[0])),fft)	#plot fft of data
else:
	print "nao encontrado o eixo G ou desvio padrao eh maior que a tolerancia, nao eh possivel a analise"

#
# 	Model test
#
if(testeModelo):#test of ann aproximation model
	plot_3(Times,[XData,YData,ZData],'data test1')
	plot_3(Times,[XData,YData,ZData],'data test2')
	model=Construct_model(XData, N)
	print strftime("%Y-%m-%d %H:%M:%S", gmtime())+"-Termino do modelo"
	print "Inicio dos testes"
	x=np.sin(np.array(range(0,N))*a)+1
	y=[]
	t=np.asarray([u * a for u in range(0,k)])
	yt=np.sin(1.6+np.array(range(0,k))*a)+1
	for i in range(0,k):	#test loop
		tmp=model.predict(x.reshape(1,-1))[0]
		#print tmp
		y.append(tmp)
		x=np.roll(x,-1)
		x[N-1]=tmp*1.2
	plt.scatter(t, yt, color= 'black', label= 'Data')
	plt.plot(t, yt, color= 'black', label= 'Data')
	plt.plot(t,y, color= 'red', label= 'RBF model')
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('aproximacao continuada')
	plt.legend()
	plt.show()
#end model test
print strftime("%Y-%m-%d %H:%M:%S", gmtime())+"-Fim dos testes"
