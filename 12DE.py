import random
import math
class Problem:
    def __init__(self):
        self.minim = -5
        self.max = 5
        self.rminim = 0
        self.rmax = 0
        #self.readFromFile()
    
    def Ackleys(self, x, y):
         a = -20*math.pow(math.exp(1), -0.2*math.sqrt(0.5*(x*x+y*y))) - math.pow(math.exp(1), 0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))) + math.exp(1) + 20 
         return a

    def readFromFile(self):
        f=open("matrix.txt","r")
        matrix = []
        for line in f:
            members=line.split(' ')
            row=[]
            for cell in members:
                if self.rminim == 0:
                    self.rminim = int(cell)
                else:
                    self.rmax = int(cell)
        f.close()

class Individual:
    def __init__(self):
        self.x = random.uniform(-5,5)
        self.y = random.uniform(-5,5)
        self.state = [self.x, self.y]
        self.size = len(self.state)

    def fitness(self, problem):
        fit = problem.Ackleys(self.x, self.y)
        return abs(problem.minim-fit)

    def crossover(self,individ1, donorVector):
        crossoverRate = 0.5

        i = 0
        trialVector = Individual()
        while i < len(individ1.state):
            if random.random() > crossoverRate:
                trialVector.state[i] = individ1.state[i]
            else:
                trialVector.state[i] = donorVector[i]
            i+= 1
        return trialVector

    def equation(self, parent1, parent2, parent3, Factor):
        l = []
        for i in range(parent1.size):
            nr = (parent2.state[i]-parent3.state[i])*Factor+parent1.state[i]
            l.append(nr)
        return l

    def mutate(self, parent1, parent2, parent3):
        mutationProb = 0.5
        i = random.randint(0, self.size -1)
        factor = 0.5
        donorVector = self.equation(parent1, parent2, parent3, factor)
            
        return donorVector

class Population:
    def __init__(self, sizePop, noInd):
        self.noInd = noInd
        self.sizePop = sizePop
        self.population = [Individual() for _ in range(self.sizePop)]

    def findParent(self, p):
        for i in range(self.sizePop):
            if p == self.population[i]:
                return i
        return None

    def evaluate(self,p):
        sum = 0
        for x in self.population:
            sum += x.fitness(p)
        return sum

    def evolve(self):
        mutationProb = 0.5
        for i in range(self.sizePop):
            candidate = self.population[i]
            parents = random.sample(self.population, 2)
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            childCandidate = candidate.crossover(parent1, parent2)
            child = candidate.mutate(childCandidate)

            #print("Mutated")
            locationP1 = self.findParent(parent1)
            locationP2 = self.findParent(parent2)
            if parent1.fitness() < parent2.fitness():
                self.population[locationP1] = child
            else:
                self.population[locationP2] = child

    def reunion(self, toAdd):
        self.sizePop = self.sizePop + toAdd.size
        self.population =self.population+ [toAdd]

    def selection(self, n, p):
        if n < self.sizePop:
            self.population = sorted(self.population, key = lambda Individual: Individual.fitness(p))
            self.population = self.population[:n]
            self.sizePop = n

    def selectionDE(self, trialVector, p):
        for i in range(len(self.population)):
            if trialVector.fitness(p) < self.population[i].fitness(p):
                self.population[i] = trialVector
    
    def best(self, n, p):
        aux = sorted(self.population, key = lambda Individual: Individual.fitness(p))
        return aux[:n]

class Algorthm:
    def __init__(self, noInd, sizePop, generations):
        self.p = Problem()
        self.population = Population(sizePop, noInd)
        self.noInd = noInd
        self.sizePop = sizePop
        self.generations = generations
        
    def iteration(self):
        indexes = range(self.noInd)
        no = self.noInd // 2
        offspring = Population(self.sizePop, no)
        k=1
        for k in range(no):
            parent1, parent2, parent3 = random.sample(self.population.population, 3)
            donorVector = self.population.population[k].mutate(parent1, parent2, parent3)
            trialVector = self.population.population[k].crossover(parent1, donorVector)
        offspring.evaluate(self.p)
        #self.population.selectionDE(trialVector, self.p)
        self.population.reunion(trialVector)
        self.population.selection(self.noInd, self.p)


    def run(self):
        for k in range(self.generations):
            self.iteration()
        return self.population.best(3,self.p)


a = Algorthm(30, 30,10000)
solution = a.run()
print(solution[0].state, solution[0].fitness(a.p))
#assert solution[0].fitness(a.p) == 5.0