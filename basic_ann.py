import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import random as rnd
from math import*
import time

def sig(x,derivative = False):
    f=[]
    for item in x:
        f.append( 1./(1.+exp(-item)))
    return f

rnd.seed()

data = pd.read_excel('your excel_file directory')
data = np.matrix(data)
# if data is not normalized
M = []
for i in range(0,3):
  M.append(np.max(data[:,i] , axis =0))

Max = np.array(M)
print("MAX:" , Max)

m = []
for i in range(0,3):
  m.append(np.min(data[:,i] , axis =0))

Min = np.array(m)
print("MIN:" , Min)
# normalization
new_data = np.zeros((data.shape[0] , data.shape[1]))
for i in range(0,data.shape[0]):
  for j in range(0,data.shape[1]):
    new_data[i,j] = (data[i,j]-Min[j])/(Max[j]-Min[j])
new_data = np.matrix(new_data)
# this process tends to implement MLP network manually without any neural network libraries
row = np.shape(data)[0]

col = np.shape(data)[1]

n1=col -1

n2 = 8
n3 = 5
n4 = 1

a=-1
b=1

w1=np.random.uniform(a,b,(n2,n1))
net1= np.zeros((n2,1))
o1 = np.zeros((n2,1))

w2=np.random.uniform(a,b,(n3,n2))
net2= np.zeros((n3,1))
o2 = np.zeros((n3,1))

w3=np.random.uniform(a,b,(n4,n3))

net3= np.zeros((n4,1))
net3 = net3.reshape(1,n4)
o3 = net3

num_train =int( .75*row)

num_test =int(row-.75*row)

data_train = new_data[0:num_train,0:col]
data_test = new_data[num_train:,0:col]
output_train = np.zeros((num_train,1))
output_test = np.zeros((num_test ,1))

Max_epoch = 100
eta=.01

error_train= np.zeros((num_train,1))
error_test= np.zeros((num_test,1))
mse_train= np.zeros((Max_epoch,1))
mse_test= np.zeros((Max_epoch,1))

data_test.shape , o3.shape , col-1 , data_train

# training process
for i in range(0,Max_epoch):

    
    
    for j in range (0,num_train):
        
        I = data_train[j,0:n1]
        target = data_train[j,col-1]
        
        net1= np.matmul(w1,I.T)
        o1 = sig(net1)
        
        net2 =np.matmul(w2,o1)
        o2 = sig(net2)
        
        net3 =np.matmul( w3,o2)
        o3 = net3
        error_train[j] = target- o3

        B = np.diag(np.multiply(o2,(np.ones(len(o2))-o2)))
        A = np.diag(np.multiply(o1,(np.ones(len(o1))-o1)))
        x= (w3.dot(B)).dot(w2.dot(A))
        y= w3.dot(B)
        w1 = w1 + eta*error_train[j]*x.T*I
        w2 = w2+eta*error_train[j]*y.T*o1
        w3 =w3 + eta*error_train[j]*o2
        
        
    for j in range (0,num_train):
        
        
        I = data_train[j,0:n1]
        target = data_train[j,col-1]
        
        net1= np.matmul(w1,I.T)
        o1 = sig(net1)
        
        net2 =np.matmul(w2,o1)
        o2 = sig(net2)
        
        net3 =np.matmul( w3,o2)
        o3 = net3
        output_train[j]=o3
        error_train[j]= target - o3
        
    mse_train[i] = (error_train[j]**2)
    
    # test process
    for j in range(0,num_test):
      

      I = data_test[j,0:n1]
      target=data_test[j,col-1]
      net1= np.matmul(w1,I.T)
      o1 = sig(net1)
        
      net2 =np.matmul(w2,o1)
      o2 = sig(net2)
        
      net3 =np.matmul( w3,o2)
      o3 = net3
      output_test[j]=o3
      error_test[j]= target - o3 

# visualization 
plt.figure(1)   
plt.plot(data_train,lw=.7,color ='r')
plt.hold=True
plt.plot(output_train,lw=.8,color='b')
plt.hold=False

plt.figure(2) 
        
    
plt.plot(data_test[:,0],lw = .9 , color ='r')
plt.hold=True
plt.plot(output_test ,lw =.9, color='b')
plt.hold=False
