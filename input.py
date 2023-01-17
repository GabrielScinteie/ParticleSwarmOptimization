# Parametrii algoritm

w = 0.4 # Inertia
c1 = 2  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
noParticles = 30  # Numarul particule
noIterations = 50  # Numarul maxim de iteratii

r = 100  # Raza vecinatatii geografie
noFriends = noParticles // 10  # Numarul de prieteni pt vecinatati sociale

repulsivePoints = [(-50, -50, 1), (-50, 50, 1), (50, 50, 1), (50, -50, 1), (0, 50, 1), (50, 0, 1), (-50, 0, 1), (0, -50, 1),
                   (-10, -10, 1), (-10, 10, 1), (10, 10, 1), (10, -10, 1)]
attractivePoints = [(-75, -75, 2), (-75, 75, 2), (75, 75, 2), (75, -75, 2), (0, 0, 5)]

inputDimension = 2  # Numarul de parametrii de intrare ai functiei obiectiv
inputLowerLimits = [-100] * inputDimension  # Limita superioara a domeniului de cautare
inputUpperLimits = [100] * inputDimension  # Limita inferioara a domeniului de cautare
alfa = 0.1  # Coeficient viteza maxima


# Parametrii animatie si afisare
animation = 0
deltaT = 0.02  # Timpul dintre frame-urile animatiilor
numberDecimals = 2  # Numarul de zecimale ale rezultatelor





