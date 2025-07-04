using Plots
# import Pkg; Pkg.add("StaticArrays")
using StaticArrays

function verlet_step(x::AbstractVector,v::AbstractVector,a::AbstractVector,dt::Float64,acceleration::Function,truewind::SVector{2,Float64},boatdir::Float64)
    x_new = @. x + v * dt + 0.5 * a * dt^2
    a_new = acceleration(0.0,x_new,v,truewind,boatdir)
    v_new = @. v + 0.5 * (a + a_new) * dt
    return x_new, v_new, a_new
end

function integrate(acceleration::Function,x0::SVector{3,Float64},v0::SVector{3,Float64},dt::Float64,N_steps::Int64,truewind::SVector{2,Float64},boatdir::Float64)
    dim = length(x0)
    t = 0:dt:dt*N_steps
    # X = Vector{SVector{dim, Float64}}(undef, N_steps+1)
    # V = similar(X)
    # A = similar(X)
    X = zeros(Float64, dim, N_steps+1)
    V = similar(X)
    A = similar(X)
    X[:,1] = x0
    V[:,1] = v0
    A[:,1] = acceleration(0.0,x0,v0,truewind,boatdir)
    for i in 1:N_steps
        x_new, v_new, a_new = verlet_step(SVector(X[:,i]...), SVector(V[:,i]...), SVector(A[:,i]...), dt, acceleration, truewind, boatdir)
        # push!(X,x_new)
        # push!(V,v_new)
        # push!(A,a_new)
        X[:,i+1] = x_new
        V[:,i+1] = v_new
        A[:,i+1] = a_new
    end
    return t, X, V, A
end

# function accel(x::AbstractVector,v::AbstractVector)
#     return .-x .- 0.5 .* v
# end

# t,X,V,A = integrate(accel,[0.0,0.0,1.0],[1.0,0.0,0.0],0.05,1000)
# plot(t,X[1,:])
# plot!(t,X[2,:])
# plot!(t,X[3,:])

# print(verlet_step([0.0,0.0,1.0],[1.0,1.0,0.0],accel([0.0,0.0,1.0]),0.05,accel))