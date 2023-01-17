# from main import euclidianDistancePoints
from math import sqrt
# Parametrii

w = 0.4  # Inertia
c1 = 1  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
noParticles = 30  # Numarul particule
noIterations = 100  # Numarul maxim de iteratii

inputDimension = 2  # Numarul de parametrii de intrare ai functiei obiectiv
inputLowerLimits = [-100] * inputDimension  # Limita superioara a domeniului de cautare
inputUpperLimits = [100] * inputDimension  # Limita inferioara a domeniului de cautare
alfa = 0.1  # Coeficient viteza maxima

attractivePoints = [(-20, 0, 2), (40, 0, 2), (0, 20, 2)]
repulsivePoints = [(0, 0, 2), (-20, 20, 2), (60, 0, 4), (-25, -5, 2)]


def euclidianDistancePoints(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def f(point):
    value = 0
    for index in range(len(attractivePoints)):
        attractivePoint = (attractivePoints[index][0], attractivePoints[index][1])
        value += 1 / (euclidianDistancePoints(point, attractivePoint) + 1) * attractivePoints[index][2]
        # o solutie este cu atat mai buna cu atat distanta dintre punctul candidat si punctele atractive este mai mica

    for index in range(len(repulsivePoints)):
        repulsivePoint = (repulsivePoints[index][0], repulsivePoints[index][1])
        value -= 1 / (euclidianDistancePoints(point, repulsivePoint) + 1) * repulsivePoints[index][2]

    return -value
