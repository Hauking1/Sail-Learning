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
const_hydr = ρ_wat*A_hydr/2

# fit parameters for sail polars
# lift fourier model
plift = [1.103317488667890274e+02,9.164163828360953890e-01,-5.376682433806420081e-01,-5.771673858251248623e-02,-2.630117507551118713e-02,6.885615654282364329e-01,2.013045091066880954e-01,6.027036569627169937e-02]
# drag sin^2 model
pdrag = [-8.963222371772262420e+01,6.112799534644035582e-01,-1.808207230408802324e-02,4.918361664352755534e-04,-2.333848848242065242e-06]