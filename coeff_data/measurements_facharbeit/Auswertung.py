import numpy as np
import pandas as pd
from scipy.interpolate import splrep, BSpline
from scipy import optimize as opt
from matplotlib import pyplot as plt

# path = ['F_A; alpha laufend; Profil1.txt','F_W; alpha laufend 0-360°; Profil1.txt']
paths = ['coeff_data\measurements_facharbeit\F_A; alpha laufend; Profil1.txt',
         'coeff_data\measurements_facharbeit\F_W; alpha laufend 0-360°; Profil1.txt']

df = pd.read_csv(paths[0],sep='\t',skiprows=5,names=['time','lift'],decimal=',')
df['drag'] = (pd.read_csv(paths[1],sep='\t',skiprows=5,names=['time','drag'],decimal=',')).drag
df['angle'] = np.linspace(0,90,len(df.time))

tck_l = splrep(df.angle,df.lift,s=len(df.angle)*14.625)
df['lift_s'] = BSpline(*tck_l)(df.angle)
tck_d = splrep(df.angle,df.drag,s=len(df.angle)*4.4)
df['drag_s'] = BSpline(*tck_d)(df.angle)

def poly(x,p0,p1,p2,p3,p4): # ,p4,p5,p6):
    '''model for drag'''
    return p0 + p1*x + p2*x**2 + p3*x**3 + p4*x**4 # + p5*x**5 + p6*x**6

def model(x,x0,p0,p1,p2,p3,p4): # ,p4,p5,p6):
    '''model for lift'''
    return np.sin(np.pi/360*(x-x0))*poly(x,p0,p1,p2,p3,p4) # ,p4,p5,p6)

plift,_ = opt.curve_fit(model,df.angle,df.lift)
pdrag,_ = opt.curve_fit(poly,df.angle,df.drag)
# print(plift)
# print(pdrag)

df['lift_m'] = model(df.angle,*plift) # lift/drag model
df['drag_m'] = poly(df.angle,*pdrag)

df['force_angle'] = np.arctan2(df.lift_m,df.drag_m)*180/np.pi # in °
df['force_mag'] = np.sqrt(df.lift_m**2+df.drag_m**2)

df['dlift_s'] = np.gradient(df.lift_s,df.angle)
df['ddrag_s'] = np.gradient(df.drag_s,df.angle)
df['dlift_m'] = np.gradient(df.lift_m,df.angle)
df['ddrag_m'] = np.gradient(df.drag_m,df.angle)
df['d_angle'] = np.arctan2(df.ddrag_m,df.dlift_m)*180/np.pi # angle of deriv'vec with app. wind in °
df['d_mag'] = np.sqrt(df.ddrag_m**2+df.dlift_m**2)

fig,ax = plt.subplots(1,3)
ax[0].plot(df.angle,df.lift,marker='.',linewidth=0.05,markersize=0.4,alpha=0.6)
ax[0].plot(df.angle,df.lift_s)
ax[0].plot(df.angle,model(df.angle,*plift))

ax[0].plot(df.angle,df.drag,marker='.',linewidth=0.05,markersize=0.4,alpha=0.6)
ax[0].plot(df.angle,df.drag_s)
ax[0].plot(df.angle,poly(df.angle,*pdrag))


# ax[1].plot(df.drag,df.lift)
ax[1].plot(df.drag_s,df.lift_s)
ax[1].plot(df.drag_m,df.lift_m)
ax[1].plot(df.ddrag_m,df.dlift_m)
alphas = [10,15,20,30,45,60,80,90]
for alpha in alphas:
    X,Y = np.meshgrid([df.drag_m[df.angle==alpha]],[df.lift_m[df.angle==alpha]])
    ax[1].quiver(X,Y,df.ddrag_m[df.angle==alpha],df.dlift_m[df.angle==alpha])

# ax[2].plot(df.angle,df.force_angle)
# ax[2].plot(df.angle,df.force_mag)
# ax[2].plot(df.angle,df.d_angle)
ax[2].plot(df.angle,df.dlift_m/df.d_mag)

plt.show()