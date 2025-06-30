# approximations for lift and drag coefficientes of sails, underwater foils and hull

function fourier(x::Float64,params::SVector{8, Float64})::Float64
    p,a0,a1,a2,a3,b1,b2,b3 = params
    arg = 2*π/p
    return a0 + a1*cos(arg*x) + b1*sin(arg*x) + a2*cos(2*arg*x) + b2*sin(2*arg*x) + a3*cos(3*arg*x) + b3*sin(3*arg*x) # + a4*cos(4*arg*x) + b4*sin(4*arg*x)
end


function drag_model(x::Float64,params::SVector{5, Float64})::Float64
    x0,p0,p1,p2,p3 = params
    return sin(π/360*(x-x0))^2 * (p0 + p1*x + p2*x^2 + p3*x^3)
end


function coefficient_centerboard(β::Float64)::SVector{2,Float64}
    # drag/lift coefficient at the centerboard as a function of the leeway angle
    c_d = 1.5*sin(β)^2 + 0.1 # dominated by projection effect (sin)
    c_l = -2*π*β*(1+0.18)*(β-π)*(β+π) * 0.1*exp(-(0.5*β^2)) # zero points are known exactly due to symmetry, exp(...) for more realistic shape (guess)
    return [c_d,c_l]
end


function coefficient_hull(β::Float64, boatvelocity_sq::Float64)::SVector{2,Float64}
    c_d = 0.5*boatvelocity_sq^3 # wave drag ( ∝v^6*sin(...)) + friction drag (∝v^2)
    c_l = 0 # maybe some low dependency in β or 0
    return [c_d,c_l]
end


function coefficient_sail(α::Float64)::SVector{2,Float64}
    # drag/lift coefficient at the sail as a function of the angle of attack
    c_d = drag_model(α,pdrag) # from measured data (Facharbeit)
    c_l = fourier(α,plift) # from measured data (Facharbeit)
    return [c_d,c_l]
end