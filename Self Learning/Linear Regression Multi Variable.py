import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

n = 15
k = 500
rng = np.random.RandomState(1)
X = np.array(list(map(lambda x: 5*x, rng.rand(n*k))))
X = X.reshape((k, n))
ones = np.ones((500, 1), dtype=float)
y = np.array(list(map(lambda x: (x[0]*0.4 + rng.rand(1))[0], X)))
X = np.c_[X, np.ones(500)]


theta_as_python_list = []
for i in range(len(X[0])):
    theta_as_python_list.append(1.0)
theta = np.array(theta_as_python_list)
print(theta)


def hypotesis(x, theta):
    return theta.dot(x)


def cost(theta):
    sum = 0
    for i in range(len(X)):
        sum += (hypotesis(X[i], theta)-y[i])**2
    return sum/(2*len(X))


def gradient_Derivative(theta):
    der_list = np.zeros(16)
    for i in range(len(X)):
        for j in range(16):
            der_list[j] += (hypotesis(X[i], theta) - y[i])*X[i][j]

    for i in range(len(theta)):
        theta[i] = theta[i] - 0.01*(der_list[i]/len(X))


def plot(theta):
    x = np.linspace(1, 10*np.pi, 100)
    y = np.sin(x)

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x, y)

    for i in range(7000):
        line1.set_ydata(cost(theta))
        fig.canvas.draw()
        gradient_Derivative(theta)
        print(cost(theta))


plot(theta)
