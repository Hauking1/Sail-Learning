# approximations for lift and drag coefficientes of sails, underwater foils and hull

function coefficient_centerboard(β::Float64)::SVector{2,Float64}
    # drag/lift coefficient at the centerboard as a function of the leeway angle
    c_d = 1.5*sin(β)^2 + 0.1 # dominated by projection effect (sin)
    c_l = -2*π*β*(1+0.18)*(β-π)*(β+π) * 0.1*exp(-(0.5*β^2)) # zero points are known exactly due to symmetry, exp(...) for more realistic shape (guess)
    return [c_d,c_l]
end


function coefficient_hull(β::Float64, boatvelocity_sq::Float64)::SVector{2,Float64}
    c_d = # wave drag ( ∝v^6*sin(...)) + friction drag (∝v^2)
    c_l = # maybe some low dependency in β or 0
    return [c_d,c_l]
end


function coefficient_sail(α::Float64)::SVector{2,Float64}
    # drag/lift coefficient at the sail as a function of the angle of attack
    c_d = # from measured data (Facharbeit)
    c_l = # from measured data (Facharbeit)
    return [c_d,c_l]
end