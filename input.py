# Parametrii

w = 0.4  # Inertia
c1 = 1  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
noParticles = 30  # Numarul particule
noIterations = 100  # Numarul maxim de iteratii

inputDimension = 5  # Numarul de parametrii de intrare ai functiei obiectiv
inputLowerLimits = [-100] * inputDimension  # Limita superioara a domeniului de cautare
inputUpperLimits = [100] * inputDimension  # Limita inferioara a domeniului de cautare
alfa = 0.1  # Coeficient viteza maxima

# Functie obiectiv
def f(x):
    sum = 0
    for elem in x:
        sum += elem * elem
    return sum