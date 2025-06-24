import numpy as np
from sympy import symbols, diff, simplify, lambdify, cos, sqrt
from scipy.optimize import root_scalar

from Coeff_approx import coefficientSail as coeff

def optimzeSailAngle(appWindAngle):
    '''appWindAngle - pi/2 = angle(dc/dalpha,appWindVec) <=> ... '''
    alpha = symbols('alpha',real=True)
    cL,cD = coeff(alpha)
    tangVec = diff(cL,alpha),diff(cD,alpha) # (cL'(alpha),cD'(alpha))
    expr = (tangVec[0])/sqrt(tangVec[0]**2+tangVec[1]**2)-cos(appWindAngle)
    simpl = simplify(expr)
    lam_f = lambdify(alpha, simpl)
    sol = root_scalar(lam_f,bracket=[0,np.pi],method='brentq')
    return sol.root

def findRudderAngle():
    return 0