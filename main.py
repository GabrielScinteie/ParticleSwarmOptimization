import random
from copy import copy

# La asignarea listelor si a obiectelor se va folosi copy

# Parametrii

w = 0.7  # Inertia
c1 = 2  # Coeficient incredere in sine
c2 = 2  # Coeficient incredere in vecini
alfa = 0.2  # Coeficient viteza maxima
noParticles = 30  # Numarul particule
inputDimension = 5  # Numarul de parametrii de intrare ai functiei obiectiv
inputLowerLimits = [-100] * inputDimension  # Limita superioara a domeniului de cautare
inputUpperLimits = [100] * inputDimension  # Limita inferioara a domeniului de cautare
iterationMax = 100  # Numarul maxim de iteratii


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


def initializeSwarm():
    return [Particle() for _ in range(noParticles)]


## Algoritm

if __name__ == "__main__":
    swarm = initializeSwarm()
    socialOptim = min(list(map(lambda x: x.position, swarm)), key=f)

    for iteration in range(iterationMax):
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

    # print(f(min(list(map(lambda x: x.position, swarm)), key=f))
    print(socialOptim, end=" => ")
    print(f(socialOptim))
