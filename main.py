import random
import time
from IPython.display import display, clear_output
from copy import copy, deepcopy
from math import sqrt
from enum import Enum
import matplotlib.pyplot as plt


def readInput():
    file = open("parametrii.txt", "r")
    parametrii_vector = file.read()
    parametrii_vector = parametrii_vector.split("\n")

    w = float(parametrii_vector[0])  # Inertia
    c1 = float(parametrii_vector[1])  # Coeficient incredere in sine
    c2 = float(parametrii_vector[2])  # Coeficient incredere in vecini
    noParticles = int(parametrii_vector[3])  # Numarul de particule
    noIterations = int(parametrii_vector[4])  # Numar de iteratii
    r = float(parametrii_vector[5])  # Raza vecinatatii geografice
    noFriends = int(parametrii_vector[6])  # Numarul de prieteni pt vecinatati sociale

    return w, c1, c2, noParticles, noIterations, r, noFriends


# Constantele problemei


repulsivePoints = [(-50, -50, 1), (-50, 50, 1), (50, 50, 1), (50, -50, 1), (0, 50, 1), (50, 0, 1), (-50, 0, 1), (0, -50, 1)]
                  # (-10, -10, 1), (-10, 10, 1), (10, 10, 1), (10, -10, 1)]
attractivePoints = [(-75, -75, 2), (-75, 75, 2), (75, 75, 2), (75, -75, 2), (0, 0, 3)]

inputDimension = 2  # Numarul de parametrii de intrare ai functiei obiectiv
inputLowerLimits = [-100] * inputDimension  # Limita superioara a domeniului de cautare
inputUpperLimits = [100] * inputDimension  # Limita inferioara a domeniului de cautare
alfa = 0.1  # Coeficient viteza maxima

# Parametrii animatie si afisare
animation = 1
deltaT = 0.1  # Timpul dintre frame-urile animatiilor
numberDecimals = 2  # Numarul de zecimale ale rezultatelor

# Variabile globale

attractiveArray_x = list(map(lambda x: x[0], attractivePoints))
attractiveArray_y = list(map(lambda x: x[1], attractivePoints))

repulsiveArray_x = list(map(lambda x: x[0], repulsivePoints))
repulsiveArray_y = list(map(lambda x: x[1], repulsivePoints))


class Particle:
    def __init__(self):
        self.position = [random.uniform(inputLowerLimits[i], inputUpperLimits[i]) for i in
            range(inputDimension)]  # Setam pozitia initiala a particulei
        self.cost = f(copy(self.position))  # Setam valoarea functiei pentru particula
        self.speed = [0 for _ in range(inputDimension)]
        self.maxSpeeds = [alfa * (inputUpperLimits[i] - inputLowerLimits[i]) for i in
            range(inputDimension)]  # Setam viteza maxima pe fiecare dimensiune
        self.personalOptim = copy(self.position)


class Type(Enum):
    GeographicalBest = 0
    SocialBest = 1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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


def euclidianDistancePoints(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def f(point):
    value = 0
    for index in range(len(attractivePoints)):
        attractivePoint = (attractivePoints[index][0], attractivePoints[index][1])
        value -= 1 / (euclidianDistancePoints(point, attractivePoint) ** 2 + 1) * attractivePoints[index][2]
        # daca distanta tinde la 0, atunci se va scadea 1 / (0 + 1) * pondere = pondere
        # daca distanta este 1, atunci se va scadea 1 / 2 * pondere
        # daca distanta tinde la infinit, atunci se va scadea 0
        # deci, daca distanta este mica se scad numere mai mari, deci minimizarea functiei ne va aduce mai aproape de punctele de atractie

    for index in range(len(repulsivePoints)):
        repulsivePoint = (repulsivePoints[index][0], repulsivePoints[index][1])
        value += 1 / (euclidianDistancePoints(point, repulsivePoint) ** 2 + 1) * repulsivePoints[index][2]

    return value


def getOptimalOfGeographicalNeighbours(particle, swarm, r):
    optimal = copy(particle)
    for index in range(len(swarm)):
        if euclidianDistance(particle, swarm[index]) < r:
            if swarm[index].cost < optimal.cost:
                optimal = copy(swarm[index])

    return optimal


def getOptimalOfSocialNeighbours(particleIndex, swarm, noFriends):
    startingIndex = max(0, particleIndex - noFriends)
    endingIndex = min(len(swarm) - 1, particleIndex + noFriends)

    optimal = copy(swarm[startingIndex])
    for index in range(startingIndex, endingIndex + 1):
        if swarm[index].cost < optimal.cost:
            optimal = copy(swarm[index])

    return optimal

def particleSwarmOptimizationGlobalBest(f, swarm, noIterations, noParticles, w, c1, c2):
    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)

    for iteration in range(noIterations):
        print(iteration)
        if animation == 1:
            x_positions = list(map(lambda x: x.position[0], swarm))
            y_positions = list(map(lambda x: x.position[1], swarm))

            ax.clear()
            ax.scatter(x_positions, y_positions)
            ax.scatter(attractiveArray_x, attractiveArray_y, c="green")
            ax.scatter(repulsiveArray_x, repulsiveArray_y, c="red")
            ax.set_xlim(inputLowerLimits[0], inputUpperLimits[0])
            ax.set_ylim(inputLowerLimits[1], inputUpperLimits[1])

            display(fig)
            clear_output(wait=True)
            plt.pause(deltaT)

            time.sleep(deltaT)

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


def particleSwarmOptimizationLocalBest(f, swarm, noIterations, noParticles, w, c1, c2, type, parameter):
    # Daca type este GeographicalBest, atunci parameter are semnificatia urmatoare:
    #   ne spune cat de mare este raza vecinatatii unei particule
    # Daca type este SocialBest, atunci parameter are semnificatia urmatoare:
    #   ne spune care este vecinatatea unei particule cu indexul i: [index - parameter, index + noFriends]

    for iteration in range(noIterations):
        print(iteration)
        if animation == 1:
            x_positions = list(map(lambda x: x.position[0], swarm))
            y_positions = list(map(lambda x: x.position[1], swarm))

            ax.clear()

            ax.scatter(attractiveArray_x, attractiveArray_y, c="green")
            ax.scatter(repulsiveArray_x, repulsiveArray_y, c="red")
            ax.scatter(x_positions, y_positions)
            ax.set_xlim(inputLowerLimits[0], inputUpperLimits[0])
            ax.set_ylim(inputLowerLimits[1], inputUpperLimits[1])

            display(fig)
            clear_output(wait=True)
            plt.pause(deltaT)

            time.sleep(deltaT)

        for index in range(len(swarm)):
            r1 = random.random()
            r2 = random.random()

            particle = swarm[index]
            if type == Type.SocialBest:
                socialOptim = getOptimalOfSocialNeighbours(index, swarm, parameter).position
            else:
                socialOptim = getOptimalOfGeographicalNeighbours(particle, swarm, parameter).position

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

    socialOptim = min(list(map(lambda x: x.personalOptim, swarm)), key=f)
    return socialOptim, f(socialOptim)


if __name__  == "__main__":
    if animation == 1:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(inputLowerLimits[0], inputUpperLimits[0])
        ax.set_ylim(inputLowerLimits[1], inputUpperLimits[1])

    w, c1, c2, noParticles, noIterations, r, noFriends = readInput()
    swarm = initializeSwarm(noParticles)

    minim1 = particleSwarmOptimizationGlobalBest(f, deepcopy(swarm), noIterations, noParticles, w, c1, c2)
    minim2 = particleSwarmOptimizationLocalBest(f, deepcopy(swarm), noIterations, noParticles, w, c1, c2, Type.GeographicalBest, r)
    minim3 = particleSwarmOptimizationLocalBest(f, deepcopy(swarm), noIterations, noParticles, w, c1, c2, Type.SocialBest, noFriends)

    minim1_rounded = ([round(minim1[0][0], numberDecimals), round(minim1[0][1], numberDecimals)], round(minim1[1], numberDecimals))
    minim2_rounded = ([round(minim2[0][0], numberDecimals), round(minim2[0][1], numberDecimals)], round(minim1[1], numberDecimals))
    minim3_rounded = ([round(minim3[0][0], numberDecimals), round(minim3[0][1], numberDecimals)], round(minim3[1], numberDecimals))

    print(minim1_rounded)
    print(minim2_rounded)
    print(minim3_rounded)