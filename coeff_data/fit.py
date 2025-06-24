import numpy as np
import scipy.optimize as opt
from matplotlib import pyplot as plt

data = np.loadtxt('coeff_data\eppler22.csv',skiprows=1,unpack=True)

def func(x,b,c,d,e):
    return b*x**3 + c*x + d/x + e/x**2

popt,pcov = opt.curve_fit(func,data[0],data[1])

plt.plot(data[0],data[1])
alpha = np.linspace(-90,90,100)
plt.plot(alpha,func(alpha,*popt))
plt.show()