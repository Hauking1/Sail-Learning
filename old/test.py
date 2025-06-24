import numpy as np
from Coeff_approx import coefficientSail as coeff
from sympy import symbols, diff, simplify, lambdify, nsolve, cos, sqrt
from scipy.optimize import root_scalar, fsolve
import Sailor as s
from matplotlib import pyplot as plt

# appWindAngle = 100*np.pi/180
# alpha = symbols('alpha',real=True)
# cL,cD = coeff(alpha)
# tangVec = diff(cL,alpha),diff(cD,alpha) # (cL'(alpha),cD'(alpha))
# expr = tangVec[0]/sqrt(tangVec[0]**2+tangVec[1]**2)-cos(appWindAngle)
# simpl = simplify(expr)
# lam_f = lambdify(alpha, simpl)
# sol = root_scalar(lam_f,bracket=[-np.pi,np.pi],method='bisect')
# print(sol.root*180/np.pi)

appWindAngle = np.linspace(np.pi/2,np.pi,180)
delta = []
for e in appWindAngle:
    temp = s.optimzeSailAngle(e)
    print(temp)
    delta.append(temp)
delta = np.array(delta)
