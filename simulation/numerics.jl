using Plots
import Pkg; Pkg.add("StaticArrays")
using StaticArrays

function verlet_step(x::AbstractVector,v::AbstractVector,a::AbstractVector,dt::Float64,acceleration::Function)
    @. x_new = x + v * dt + 0.5 * a * dt^2
    a_new = acceleration(x_new)
    @. v_new = v + 0.5 * (a + a_new) * dt
    return x_new, v_new, a_new
end

function integrate(acceleration::Function,x0::AbstractVector,v0::AbstractVector,dt::Float64,N_steps::Int)
    dim = length(x0)
    t = 0:dt:dt*N_steps
    X = Vector{SVector{dim, Float64}}(undef, N_steps+1)
    V = similar(X)
    A = similar(X)
    # X = zeros(Float64, dim, N_steps + 1)
    # V = similar(X)
    # A = similar(X)
    X[1] = @SVector x0
    V[1] = @SVector v0
    A[1] = acceleration(x0)
    for i in 1:N_steps
        x_new, v_new, a_new = verlet_step(X[i], V[i], A[i], dt, acceleration)
        # push!(X,x_new)
        # push!(V,v_new)
        # push!(A,a_new)
        X[i+1] = @SVector x_new
        V[i+1] = @SVector v_new
        A[i+1] = a_new
    end
    return t, X, V, A
end

function accel(x::AbstractVector)
    return .-x    
end

t,X,V,A = integrate(accel,[0.0,0.0,1.0],[1.0,0.0,0.0],0.05,100)
plot(t,X)