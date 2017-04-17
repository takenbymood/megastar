import random
from deap import creator, base, tools, algorithms
import numpy
import string
from difflib import SequenceMatcher
import toolbox as tb

class MoranNode:
	def __init__(self,popsize):
		self.popsize=popsize
		self.toolbox = tb.oneMax()
		self.population = self.toolbox.population(n=self.popsize)

	def evaluateNode(self):
		offspring = algorithms.varAnd(self.population, self.toolbox, cxpb=0.6, mutpb=0.25)
		fits = self.toolbox.map(self.toolbox.evaluate, offspring)
		for fit, ind in zip(fits, offspring):
			ind.fitness.values = fit
		self.population = self.toolbox.select(offspring, k=len(self.population))
	
class mnParticleSwarm(MoranNode):
	def __init__(self,popsize):
		self.popsize=popsize
		self.toolbox = tb.particleSwarm()
		self.population = self.toolbox.population(n=self.popsize)
		self.best = None

	def evaluateNode(self):
		for part in self.population:
			part.fitness.values = self.toolbox.evaluate(part)[0],
			if not part.best or part.best.fitness < part.fitness:
				part.best = creator.Individual(part)
				part.best.fitness.values = part.fitness.values
			if not self.best or self.best.fitness < part.fitness:
				self.best = creator.Individual(part)
				self.best.fitness.values = part.fitness.values
		for part in self.population:
			self.toolbox.update(part, self.best)
		
		