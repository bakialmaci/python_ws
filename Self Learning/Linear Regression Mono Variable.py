import numpy as np
import matplotlib.pyplot as plt

rng = np.random.RandomState(1)
X = list(map(lambda x: 5*x, rng.rand(50)))
y = list(map(lambda x: (x*0.4+float(rng.rand(1))), X))

a = 1
b = 1


def h_func(a, b, x):
    return a*x + b


def j_func(a, b):
    sum = 0
    for i in range(len(X)):
        sum += (h_func(a, b, X[i])-y[i])**2
    return sum/(2*len(X))


def derivative(a, b):
    der_a = 0
    der_b = 0

    for i in range(len(X)):
        der_a += (h_func(a, b, X[i]) - y[i])*X[i]

    for j in range(len(y)):
        der_b += (h_func(a, b, X[j]) - y[j])

    return der_a,der_b


def gradientDescent(a, b):
    for i in range(10000):
        der_a, der_b = derivative(a, b)
        a = a - 0.001*(der_a/len(X))
        b = b - 0.001*(der_b/len(y))
        print(j_func(a,b))
    return a,b


def plot(a, b):
    plt.scatter(X, y)
    Y_pred = a*np.array(X) + b
    plt.plot([min(X), max(X)], [min(Y_pred), max(Y_pred)], color='red')
    plt.show()


a, b = gradientDescent(a, b)
plot(a, b)
