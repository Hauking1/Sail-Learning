using DifferentialEquations

include("forces.jl")

function rhs(X,p,t)
    # ̈x = a(x,̇x,t) => ̇x = v, ̇v = a(x,v,t)
    truewind,boatdir = p
    x1dot = X[1]
    x2dot = X[2]
    x3dot = X[3]
    v1dot, v2dot, v3dot = acceleration(t,[x1dot,x2dot,x3dot],truewind,boatdir)
    return [x1dot, x2dot, x3dot, v1dot, v2dot, v3dot]
end

u0 = [0.0,0.0,0.0,0.0,0.0,0.0]
tspan = [0.0,10.0]
dt = 0.05
prob = ODEProblem(rhs, u0, tspan, p=[[0.0,-10.0],0.0])
sol  = solve(prob, ImplicitMidpoint(); dt = dt, saveat = dt)

plot(sol[1,:],sol[2,:])