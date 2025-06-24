import numpy as np
from scipy.integrate import solve_ivp as solve
from matplotlib import pyplot as plt

import Coeff_approx as c
import Sailor as s

def force(CONST,flow,coeff,dirMatrix):
    '''general expression for aero/hydrodynamic force'''
    return -CONST*np.dot(flow,flow)*dirMatrix@coeff

def appWindAngle(trueWind,boatSpeedVec):
    '''wind triangle'''
    appWind = trueWind - boatSpeedVec
    boatSpeedVecSq = np.dot(boatSpeedVec,boatSpeedVec)
    if not boatSpeedVecSq == 0:
        a = np.dot(appWind,boatSpeedVec)
        b = np.sqrt((np.dot(appWind,appWind)*boatSpeedVecSq))
        return a/b
    else:
        return np.pi # appWindAngle0

def leewayAngle(boatDir,boatSpeedVec):
    '''calculates leewayAngle'''
    beta = appWindAngle(trueWind,boatSpeedVec) + np.pi/2 - boatDir
    if type(beta)==float:
        return beta
    else:
        return leewayAngle0
    
def angleOfAttack(appWindAngle):
    # return (appWindAngle - np.pi) / 2
    # return s.optimzeAngleOfAttack(appWindAngle)
    return 0.5*appWindAngle

def sailAngle(trueWind,boatDir,boatSpeedVec):
    '''delta = gamma - alpha - beta'''
    gamma = appWindAngle(trueWind,boatSpeedVec)
    return gamma - angleOfAttack(gamma) - leewayAngle(boatDir,boatSpeedVec)

def mirrorMatr(gamma):
    '''mirrors at symmetry axis'''
    # gamma = appWindAngle(angleOfAttack,sailAngle,leewayAngle)
    sin = np.sin(gamma)
    cos = np.cos(gamma)
    return np.array([[cos, sin],[sin, -cos]])

def fAero(trueWind,boatSpeedVec):
    '''aerodynamic forces'''
    RHO_AIR = 1.204 # kg/m^3
    A_AERO = 10 # m^2 # TODO
    CONST_AERO = A_AERO*RHO_AIR/2
    gamma = appWindAngle(trueWind,boatSpeedVec)
    alpha = angleOfAttack(gamma)
    coeffAero = c.coefficientSail(alpha)
    dirMatr = np.array([[1, 0],[1, 0]])
    return force(CONST_AERO,(trueWind-boatSpeedVec),coeffAero,dirMatr)

def fHydro(boatDir,boatSpeedVec,trueWind):
    '''hydrodynamic forces'''
    RHO_WATER = 1e3 # kg/m^3
    A_HYDRO = 1 # m^2 # TODO
    CONST_HYDRO = A_HYDRO*RHO_WATER/2
    beta = leewayAngle(boatDir,boatSpeedVec)
    rudderAngle = s.findRudderAngle()
    gamma = appWindAngle(trueWind,boatSpeedVec)
    coeffHydro = c.coefficientThinSym(beta) + c.coefficientThinSym(beta+rudderAngle) # + c.cofficientHull(beta,boatSpeedVec)
    mirror = mirrorMatr(gamma)
    return force(CONST_HYDRO,boatSpeedVec,coeffHydro,mirror)

def torque(angSpeed):
    '''calculates torques caused by rudderangle and angSpeed'''
    return 0

def acceleration(t,boatSpeedVec3d,trueWind,boatDir,MASS,INERTIA):
    '''return 3dim vector including all forces AND Torques; componentwise: F_x,F_y,T'''
    boatSpeedVec = boatSpeedVec3d[:2] # np.array([boatSpeedVec3d[0],boatSpeedVec3d[1]])
    # print(boatSpeedVec3d[0])
    # print(boatSpeedVec)
    # print(trueWind)
    angSpeed = boatSpeedVec3d[2:]
    forceX,forceY = fAero(trueWind,boatSpeedVec) + fHydro(boatDir,boatSpeedVec,trueWind)
    torqueZ = torque(angSpeed)
    return np.array([forceX/MASS,forceY/MASS,torqueZ/INERTIA])

# define wind
trueWindSpeed = -10 # m/s
trueWindDir = 90*np.pi/180 # in rad
trueWind = trueWindSpeed*np.array([np.cos(trueWindDir),np.sin(trueWindDir)])

# define boat
MASS = 100 # kg
INERTIA = 1200 # r^2 kg

# define situation
boatSpeedVec3d0 = np.array([1,0,0]) # speedX,speedY,angSpeed
boatDir0 = 45*np.pi/180 # in rad
''' v0_Boat = 0 is approximated boatSpeedVec(0+Delta_t) = trueWind(t=0))
    ==> pi = gamma = alpha + delta + gamma and
    ==> beta = windDir in boat's perspective'''
leewayAngle0 = trueWindDir-boatDir0 # (beta0)#
appWindAngle0 = np.pi # (gamma0)
angleOfAttack0 = angleOfAttack(appWindAngle0) # (delta0)
sailAngle0 = appWindAngle0 - leewayAngle0 - angleOfAttack0 # (alpha0)
# angSpeedVec0 = np.array([0,0,1])
rudderAngle0 = 0

# calculate initial values
initVals = acceleration(0,boatSpeedVec3d0,trueWind,boatDir0,MASS,INERTIA)
print('initVals:',initVals)


sol = solve(acceleration,t_span=(0,10),y0=initVals,args=(trueWind,boatDir0,MASS,INERTIA),t_eval=np.linspace(0,10,100))

print(sol.t)
print(sol.y)

plt.plot(sol.y[0],sol.y[1])
plt.show()