import numpy as np
import scipy.optimize as opt
from matplotlib import pyplot as plt

data = np.loadtxt('coeff_data\eppler22.csv',skiprows=1,unpack=True)

# additional data points
angle = np.append(data[0],[40,50,60,70,80,90])
lift = np.append(data[1],[1,0.8,0.6,0.4,0.2,0])

def func(x,b,c,d,e):
    return b*x**3 + c*x + d/x + e/x**2

popt,pcov = opt.curve_fit(func,data[0],data[1])

plt.plot(angle,lift)
alpha = np.linspace(-5,20,100)
# plt.plot(alpha,func(alpha,*popt))
plt.show()