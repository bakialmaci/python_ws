import sklearn
from sklearn import datasets
import numpy as np
from sklearn import preprocessing


house = sklearn.datasets.fetch_california_housing(data_home=None, download_if_missing=True, return_X_y=False)


x = np.insert(house.data,0,1,axis=1)
y = house.target
m = x.shape[0]
n = x.shape[1]
theta = np.ones(n)
iteration = 30000
alfa = 10e-3
x = preprocessing.normalize(x)

(m,n) = house.data.shape
x = (house.data - np.resize(np.average(house.data,axis=0),(m,n)))/np.resize(np.std(house.data,axis=0),(m,n))
x = np.insert(x,0,1,axis=1)


def hypotesis(x, theta):
    return np.matmul(np.transpose(theta),x)


def cost(theta,x,y):
        sum = np.matmul(np.transpose(np.matmul(x,theta)-y),np.matmul(x,theta)-y)
        return sum/(2*len(x))


def gradient_Derivative(theta,alfa,m,y,x):
    for i in range(iteration):
        theta = theta - (alfa/m)*np.matmul(np.transpose(x),np.matmul(x,theta)-y)
        print(cost(theta,x,y))


gradient_Derivative(theta,alfa,m,y,x)
