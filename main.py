import random
import time
from IPython.display import display, clear_output
from input import *
from copy import copy
from math import sqrt
from enum import Enum
import matplotlib.pyplot as plt

# !!! La asignarea listelor si a obiectelor se va folosi copy


class Particle:
    def __init__(self):
        self.position = [random.uniform(inputLowerLimits[i], inputUpperLimits[i]) for i in
            range(inputDimension)]  # Setam pozitia initiala a particulei
        self.cost = f(copy(self.position))  # Setam valoarea functiei pentru particula
        self.speed = [0 for _ in range(inputDimension)]
        self.maxSpeeds = [alfa * (inputUpperLimits[i] - inputLowerLimits[i]) for i in
            range(inputDimension)]  # Setam viteza maxima pe fiecare dimensiune
        self.personalOptim = copy(self.position)


class Square:
    def __init__(self, x1, y1, x2, y2):
        self.length = x2 - x1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def isPointInside(self, x, y):
        if self.x1 < x and self.x2 > x:
            if self.y1 < y and self.y2 > y:
                return True
        return False





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


def checkAllPointsInCamera(swarm, rectangle):
    for particle in swarm:
        x = particle.position[0]
        y = particle.position[1]
        if not rectangle.isPointInside(x, y):
            return False

    return True


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


camera = Square(inputLowerLimits[0], inputLowerLimits[1], inputUpperLimits[0], inputUpperLimits[1])


def particleSwarmOptimizationGlobalBest(f, noIterations, noParticles, w, c1, c2):
    global camera

    swarm = initializeSwarm(noParticles)
    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)

    attractiveArray_x = list(map(lambda x: x[0], attractivePoints))
    attractiveArray_y = list(map(lambda x: x[1], attractivePoints))

    repulsiveArray_x = list(map(lambda x: x[0], repulsivePoints))
    repulsiveArray_y = list(map(lambda x: x[1], repulsivePoints))

    for iteration in range(noIterations):
        # newCamera = Square(camera.x1 / 10, camera.y1 / 10, camera.x2 / 10, camera.y2 / 10)
        # if checkAllPointsInCamera(swarm, newCamera) == True:
        #     camera = copy(newCamera)
        print(iteration)
        x_positions = list(map(lambda x: x.position[0], swarm))
        y_positions = list(map(lambda x: x.position[1], swarm))

        ax.clear()
        ax.scatter(x_positions, y_positions)
        ax.scatter(attractiveArray_x, attractiveArray_y, c="green")
        ax.scatter(repulsiveArray_x, repulsiveArray_y, c="red")
        ax.set_xlim(camera.x1, camera.x2)
        ax.set_ylim(camera.y1, camera.y2)

        display(fig)
        clear_output(wait=True)
        plt.pause(0.05)

        time.sleep(0.05)
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


def particleSwarmOptimizationLocalBest(f, noIterations, noParticles, w, c1, c2, type, parameter):
    # Daca type este GeographicalBest, atunci parameter are semnificatia urmatoare:
    #   ne spune cat de mare este raza vecinatatii unei particule
    # Daca type este SocialBest, atunci parameter are semnificatia urmatoare:
    #   ne spune care este vecinatatea unei particule cu indexul i: [index - parameter, index + noFriends]

    swarm = initializeSwarm(noParticles)

    for iteration in range(noIterations):
        print(iteration)

        x_positions = list(map(lambda x: x.position[0], swarm))
        y_positions = list(map(lambda x: x.position[1], swarm))

        ax.clear()
        ax.scatter(x_positions, y_positions)
        ax.set_xlim(inputLowerLimits[0], inputUpperLimits[0])

        ax.set_ylim(inputLowerLimits[1], inputUpperLimits[1])
        display(fig)
        clear_output(wait=True)
        plt.pause(0.1)

        time.sleep(0.2)
        # screen.fill((255, 255, 255))
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

            if f(particle.position) > f(particle.personalOptim):
                particle.personalOptim = copy(particle.position)

    socialOptim = min(list(map(lambda x: x.personalOptim, swarm)), key=f)
    return socialOptim, f(socialOptim)


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(inputLowerLimits[0], inputUpperLimits[0])
    ax.set_ylim(inputLowerLimits[1], inputUpperLimits[1])
    print(particleSwarmOptimizationGlobalBest(f, noIterations, noParticles, w, c1, c2))
    r = (inputUpperLimits[0] - inputLowerLimits[0]) * sqrt(inputDimension) / 4 # jumatate lungimea diagonalei hipercubului
    noFriends = noParticles // 2 # jumatate din numarul de particule
    # print(particleSwarmOptimizationLocalBest(f, noIterations, noParticles, w, c1, c2, Type.GeographicalBest, r))
    # print(particleSwarmOptimizationLocalBest(f, noIterations, noParticles, w, c1, c2, Type.SocialBest, noFriends))





