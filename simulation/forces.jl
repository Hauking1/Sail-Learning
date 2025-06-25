using StaticArrays

include("coefficients.jl")
include("constants.jl")

function apparent_wind_angle(truewind::SVector{2, Float64}, boatvelocity::SVector{2, Float64})::Float
    appwind = truewind - boatvelocity
    return atan(appwind[2],appwind[1])
end


function force(constant::Float64, flowspeed::SVector{2, Float64}, coeff::SVector{2, Float64}, dirMatrix::SMatrix{2, 2, Float64})::SVector{2, Float64}
    -constant*dot(flowspeed,flowspeed) .* dirMatrix*coeff
end


function leeway_angle(boatdir::Float64, boatvelocity::SVector{2, Float64}, truewind::SVector{2, Float64})::Float64
    if dot(boatvelocity) == 0.0
        return 0.0 # TODO handle v=0
    else
        return apparent_wind_angle(truewind,boatvelocity) + π/2 - boatdir
    end
end


function angle_of_attack(γ::Float64)::Float64
    return 0.5*γ # TODO hard coded optimum angle of attack
end


function sail_angle(truewind::SVector{2,Float64}, boatdir::Float64, boatvelocity::SVector{2,Float64})::Float64
    # δ = γ - α + β
    γ = apparent_wind_angle(truewind,boatvelocity)
    return γ - angle_of_attack(γ) - leeway_angle(boatdir,boatvelocity,truewind)
end


function mirrorMatr(γ::Float64)::SMatrix(2,2,Float64)
    # mirror transformation at symmetry axis
    return [cos(γ) sin(γ); sin(γ) -cos(γ)]
end


function force_aero(truewind::SVector{2,Float64}, boatvelocity::SVector{2,Float64})::SVector{2,Float64}
    γ = apparent_wind_angle(truewind,boatvelocity)
    α = angle_of_attack(γ)
    coeff_aero = coefficient_sail(α)
    dirMatr = [1 0; 1 0] # TODO check signs!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return force(const_aero,(truewind .- boatvelocity),coeff_aero,dirMatr)
end


function force_hydr(boatdir::Float64, truewind::SVector{2,Float64}, boatvelocity::SVector{2,Float64})::SVector{2,Float64}
    β = leeway_angle(boatdir,boatvelocity,truewind)
    γ = apparent_wind_angle(truewind,boatvelocity)
    coeff_hydro = coefficient_centerboard(β) .+ coefficient_hull(β,dot(boatvelocity,boatvelocity))
    mirror = mirrorMatr(γ)
    return force(const_hydr,boatvelocity,coeff_hydro,mirror)
end


function acceleration(t::Float64,q_dot::SVector{3,Float64},truewind::SVector{2,Float64},boatdir::Float64)::SVector{3,Float64}
    # 3d right hand side
    boatvelocity = q_dot[1:2]
    angularvelocity = q_dot[3]
    forceX,forceY = force_aero(truewind,boatvelocity) .+ force_hydr(boatdir,truewind,boatvelocity)
    torqueZ = torque(angularvelocity)
    return [forceX/mass, forceY/mass, torqueZ/inertiaZ]
end