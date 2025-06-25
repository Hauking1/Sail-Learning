import pandas as pd
import numpy as np
from scipy.interpolate import splrep, BSpline
from scipy import optimize as opt
from matplotlib import pyplot as plt

# path = ['F_A; alpha laufend; Profil1.txt','F_W; alpha laufend 0-360°; Profil1.txt']
paths = ['coeff_data\measurements_facharbeit\F_A; alpha laufend; Profil1.txt',
         'coeff_data\measurements_facharbeit\F_W; alpha laufend 0-360°; Profil1.txt']

pressure = 1.204/2*0.01*3**2 * 1e3 # rho/2 * A * u^2 * 1e3 # due to mN
df = pd.read_csv(paths[0],sep='\t',skiprows=5,names=['time','lift'],decimal=',')/pressure
df['drag'] = (pd.read_csv(paths[1],sep='\t',skiprows=5,names=['time','drag'],decimal=',')/pressure).drag
df['angle'] = np.linspace(0,90,len(df.time))

def poly(x,p0,p1,p2,p3,p4): # ,p4,p5,p6):
    '''model for drag'''
    return p0 + p1*x + p2*x**2 + p3*x**3 + p4*x**4 # + p5*x**5 + p6*x**6

def fourier(x,p,a0,a1,a2,a3,b1,b2,b3):
    arg = 2*np.pi/p
    return a0 + a1*np.cos(arg*x) + b1*np.sin(arg*x) + a2*np.cos(2*arg*x) + b2*np.sin(2*arg*x) + a3*np.cos(3*arg*x) + b3*np.sin(3*arg*x) # + a4*np.cos(4*arg*x) + b4*np.sin(4*arg*x)
    

def model(x,x0,p0,p1,p2,p3): # ,p4,p5,p6):
    '''model for drag'''
    return np.sin(np.pi/360*(x-x0))**2 * (p0 + p1*x + p2*x**2 + p3*x**3)

p0 = [93,58.89354242,-30.87180848,-7.87084064,-3.63829307,21.08891605,7.77232228,2.30317846] # p0[1:] from fit with fixed p=93 then reuse as starting values for fit with variable p
plift,_ = opt.curve_fit(fourier,df.angle,df.lift,p0=p0)
pdrag,_ = opt.curve_fit(model,df.angle,df.drag)
print(plift)
print(pdrag)

np.savetxt('coeff_data/plift', plift, newline=',')
np.savetxt('coeff_data/pdrag', pdrag, newline=',')

df['lift_m'] = fourier(df.angle,*plift) # lift/drag model
df['drag_m'] = model(df.angle,*pdrag)

fig,ax = plt.subplots()

ax.plot(df.angle,df.lift,marker='.',linewidth=0.05,markersize=0.4,alpha=0.6)
ax.plot(df.angle,df.drag,marker='.',linewidth=0.05,markersize=0.4,alpha=0.6)

ax.plot(df.angle,df.lift_m)
ax.plot(df.angle,df.drag_m)
# ax.plot(df.angle,2*np.pi*df.angle*(1+0.1)+df.lift_m[0]) # approximation for small alpha
plt.show()