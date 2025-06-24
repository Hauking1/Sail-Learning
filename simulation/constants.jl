# natural parameters
# densities in kg/m^3
ρ_air = 1.204 
ρ_wat = 1e3

# boat charcteristics
# areas in m^2
A_aero = 10.0 # sail area
A_hydr = 1.0 # centerboard (+ rudder) area

# inertial parameters
mass = 100 # in kg
inertiaZ = 1200 # in kg*m^2

# force constants
const_aero = ρ_air*A_aero/2
const_hydr = ρ_war*A_hydr/2