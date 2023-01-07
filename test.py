from main import particleSwarmOptimization


# Functie obiectiv
def f(x):
    sum = 0
    for elem in x:
        sum += elem * elem
    return sum


# Parametrii default

w = 0.4  # Inertia
c1 = 1  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
noParticles = 30  # Numarul particule
iterationMax = 100  # Numarul maxim de iteratii
precision = 1e-5


print(particleSwarmOptimization(f, iterationMax, noParticles, w, c1, c2))