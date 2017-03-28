import random
from deap import creator, base, tools, algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax,nFitness=0)

class MoranNode:
	def __init__(self,popsize):
		self.popsize=popsize

		self.toolbox = base.Toolbox()

		self.toolbox.register("attr_bool", random.randint, 0, 1)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, n=10)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("evaluate", self.evalOneMax)
		self.toolbox.register("mate", tools.cxTwoPoint)
		self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
		self.toolbox.register("select", tools.selTournament, tournsize=3)

		self.population = self.toolbox.population(n=popsize)

	def evalOneMax(self,individual):
		return sum(individual),

	def evaluateNode(self):
		offspring = algorithms.varAnd(self.population, self.toolbox, cxpb=0.5, mutpb=0.1)
		fits = self.toolbox.map(self.toolbox.evaluate, offspring)
		for fit, ind in zip(fits, offspring):
			ind.fitness.values = fit
		self.population = self.toolbox.select(offspring, k=len(self.population))