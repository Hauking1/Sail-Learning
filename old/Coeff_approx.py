"""These are approximated coefficient for sail boats."""

import numpy as np
from numpy import pi


def coefficientAirDrag(angleOfAttack: float) -> float:
    """Calculate the wind resistance coefficient based on the angle of attack."""
    return 0.41 * pow(angleOfAttack, 2) + 0.13 * abs(angleOfAttack) + 0.3


def coefficientAirLift(angleOfAttack: float) -> float:
    """Calculate the wind lift coefficient based on the angle of attack."""
    return -3.5 * 16 / pow(pi, 2) * pow((abs(angleOfAttack) - pi / 4), 2) + 3.5


def coefficientWaterDrag(angleOfAttack: float) -> float:
    """Calculate the water drag coefficient based on the angle of attack."""
    return coefficientAirDrag(angleOfAttack)


def coefficientWaterLift(angleOfAttack: float) -> float:
    """Calculate the water lift coefficient based on the angle of attack."""
    return coefficientAirLift(angleOfAttack)

'''------------------ von vorne -----------------'''

def coefficientSail(angleOfAttack):
    c_SL = -3.5 * 16 / pow(pi, 2) * pow((abs(angleOfAttack) - pi / 4), 2) + 3.5
    c_SD = 0.41 * pow(angleOfAttack, 2) + 0.13 * abs(angleOfAttack) + 0.3
    return np.array([c_SL,c_SD])

def coefficientThinSym(angleOfAttack):
    c_L = -3.5 * 16 / pow(pi, 2) * pow((abs(angleOfAttack) - pi / 4), 2) + 3.5
    c_D = 0.41 * pow(angleOfAttack, 2) + 0.13 * abs(angleOfAttack) + 0.3
    return np.array([c_L,c_D])

def cofficientHull(angleOfAttack,flowSpeed):
    c_L = 0.13*angleOfAttack # low angle of attack dependency
    c_D = flowSpeed**6 # appr poly O(v^6)
    return np.array([c_L,c_D])