import random
from deap import creator, base, tools, algorithms
import numpy
import string
from difflib import SequenceMatcher



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax,nFitness=0)

targetString = "Shall I compare thee to a summer's day? Thou art more lovely and more temperate. Rough winds do shake the darling buds of May, And summer's lease hath all too short a date."
legalChars = string.ascii_letters+" '.?,"

def similar(a, b):
	f = 0
	for i in range(len(a)):
		# d = abs(legalChars.index(a[i]) - legalChars.index(b[i]))
		# f += 1.0/(min(d,len(legalChars)-d)+1)
		if a[i] == b[i]:
			f+=1
	return f

class MoranNode:
	def __init__(self,popsize):
		self.popsize=popsize

		self.toolbox = base.Toolbox()

		self.toolbox.register("attr_bool", random.randint, 0, 1)
		self.toolbox.register("attr_letter",random.choice,legalChars)


		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_letter, n=len(targetString))
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("evaluate", self.evalString)
		self.toolbox.register("mate", tools.cxTwoPoint)
		self.toolbox.register("mutate", self.mutateChar, indpb=0.05)
		self.toolbox.register("select", tools.selTournament, tournsize=3)

		self.population = self.toolbox.population(n=popsize)

		hof = tools.HallOfFame(1)

		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", numpy.mean)
		stats.register("std", numpy.std)
		stats.register("min", numpy.min)
		stats.register("max", numpy.max)

	def mutateChar(self,individual,indpb):
		for i in xrange(len(individual)):
			if random.random() < indpb:
				c = individual[i]
				index = legalChars.index(c)
				nindex = random.randint(0,len(legalChars))
				if nindex >= len(legalChars):
					nindex = nindex - len(legalChars)
				individual[i] = legalChars[nindex]
		return individual,

	def evalString(self,individual,target=targetString):
		return similar(''.join(individual),target),

	def evalOneMax(self,individual):
		return sum(individual),

	def evaluateNode(self):
		offspring = algorithms.varAnd(self.population, self.toolbox, cxpb=0.6, mutpb=0.25)
		fits = self.toolbox.map(self.toolbox.evaluate, offspring)
		for fit, ind in zip(fits, offspring):
			ind.fitness.values = fit
		self.population = self.toolbox.select(offspring, k=len(self.population))
		