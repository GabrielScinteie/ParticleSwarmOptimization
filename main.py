import random
from copy import copy
# La asignarea listelor si a obiectelor se va folosi copy

# Parametrii
from math import sqrt

w = 0.4  # Inertia
c1 = 1  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
noParticles = 30  # Numarul particule
noIterations = 100  # Numarul maxim de iteratii

# Constante

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



# Structuri de date
class Particle:
    def __init__(self):
        self.position = [random.uniform(inputLowerLimits[i], inputUpperLimits[i]) for i in
            range(inputDimension)]  # Setam pozitia initiala a particulei
        self.cost = f(copy(self.position))  # Setam valoarea functiei pentru particula
        self.speed = [0 for _ in range(inputDimension)]
        # self.speed = [round(0.05 * random.uniform(inputLowerLimits[i], inputUpperLimits[i]), 3) for i in
        #               range(inputDimension)]  # Setam viteza pe fiecare dimensiune
        self.maxSpeeds = [alfa * (inputUpperLimits[i] - inputLowerLimits[i]) for i in
            range(inputDimension)]  # Setam viteza maxima pe fiecare dimensiune
        self.personalOptim = copy(self.position)

# Functii utile


def limit(value, minim, maxim):
    return min(max(value, minim), maxim)


def initializeSwarm(noParticles):
    return [Particle() for _ in range(noParticles)]


def euclidianDistance(particle1, particle2):
    distance = 0
    for index in range(inputDimension):
        distance += (particle1.position[index] - particle2.position[index]) ** 2
    return sqrt(distance)


def getOptimalOfGeographicalNeighbours(particle, swarm, r):
    optimal = copy(particle)
    for index in range(len(swarm)):
        if euclidianDistance(particle, swarm[index]) < r:
            if swarm[index].cost < optimal.cost:
                optimal = copy(swarm[index])

    return optimal


def particleSwarmOptimizationGlobalBest(f, noIterations, noParticles, w, c1, c2):
    swarm = initializeSwarm(noParticles)
    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)

    for iteration in range(noIterations):
        for index in range(len(swarm)):
            r1 = random.random()
            r2 = random.random()

            # particle este o referinta catre swarm[index] deoarece in Python obiectele se transmit prin referinta
            particle = swarm[index]

            for i in range(inputDimension):
                particle.speed[i] = limit(
                    w * particle.speed[i] + \
                    c1 * r1 * (particle.personalOptim[i] - particle.position[i]) + \
                    c2 * r2 * (socialOptim[i] - particle.position[i]),
                    -particle.maxSpeeds[i], particle.maxSpeeds[i])

                particle.position[i] = limit(particle.position[i] + particle.speed[i], inputLowerLimits[i],
                                             inputUpperLimits[i])

            particle.cost = f(particle.position)

            if f(particle.position) < f(particle.personalOptim):
                particle.personalOptim = copy(particle.position)
                if particle.cost < f(socialOptim):
                    socialOptim = copy(particle.position)

    return socialOptim, f(socialOptim)


def particleSwarmOptimizationGeographicalBest(f, noIterations, noParticles, w, c1, c2, r):
    # r ne spune cat de mare este raza vecinatatii unei particule

    swarm = initializeSwarm(noParticles)
    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)

    for iteration in range(noIterations):
        for index in range(len(swarm)):
            r1 = random.random()
            r2 = random.random()

            # particle este o referinta catre swarm[index] deoarece in Python obiectele se transmit prin referinta
            particle = swarm[index]
            socialOptim = getOptimalOfGeographicalNeighbours(particle, swarm, r).position

            for i in range(inputDimension):
                particle.speed[i] = limit(
                    w * particle.speed[i] + \
                    c1 * r1 * (particle.personalOptim[i] - particle.position[i]) + \
                    c2 * r2 * (socialOptim[i] - particle.position[i]),
                    -particle.maxSpeeds[i], particle.maxSpeeds[i])

                particle.position[i] = limit(particle.position[i] + particle.speed[i], inputLowerLimits[i],
                                             inputUpperLimits[i])

            particle.cost = f(particle.position)

            if f(particle.position) < f(particle.personalOptim):
                particle.personalOptim = copy(particle.position)

    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)
    return socialOptim, f(socialOptim)


if __name__ == "__main__":
    print(particleSwarmOptimizationGlobalBest(f, noIterations, noParticles, w, c1, c2))
    r = (inputUpperLimits[0] - inputLowerLimits[0]) * sqrt(inputDimension) / 2 # jumatate lungimea diagonalei hipercubului
    print(particleSwarmOptimizationGeographicalBest(f, noIterations, noParticles, w, c1, c2, r))

