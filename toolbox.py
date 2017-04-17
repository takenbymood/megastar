import random
from deap import creator, base, tools, algorithms,benchmarks
import operator

class msToolbox(base.Toolbox):
	def __init__(self):
		super(msToolbox,self).__init__()

class oneMax(msToolbox):
	def __init__(self):
		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMax,nFitness=0)
		super(oneMax,self).__init__()

		self.register("attr_bool", random.randint, 0, 1)
		self.register("individual", tools.initRepeat, creator.Individual, self.attr_bool, 100)
		self.register("population", tools.initRepeat, list, self.individual)

		self.register("evaluate", self.evalOneMax)
		self.register("mate", tools.cxTwoPoint)
		self.register("mutate", tools.mutFlipBit, indpb=0.05)
		self.register("select", tools.selTournament, tournsize=3)

	def evalOneMax(self,individual):
		return sum(individual),

class particleSwarm(msToolbox):
	def __init__(self):
		super(particleSwarm,self).__init__()
		creator.create("FitnessMin", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMin, speed=list, 
			smin=None, smax=None, best=None)
		
		self.register("individual", self.generate, size=2, pmin=-6, pmax=6, smin=-3, smax=3)
		self.register("population", tools.initRepeat, list, self.individual)
		self.register("update", self.updateParticle, phi1=2.0, phi2=2.0)
		self.register("evaluate", benchmarks.schaffer)

	def generate(self,size, pmin, pmax, smin, smax):
		part = creator.Individual(random.uniform(pmin, pmax) for _ in range(size)) 
		part.speed = [random.uniform(smin, smax) for _ in range(size)]
		part.smin = smin
		part.smax = smax
		return part

	def updateParticle(self,part, best, phi1, phi2):
		u1 = (random.uniform(0, phi1) for _ in range(len(part)))
		u2 = (random.uniform(0, phi2) for _ in range(len(part)))
		v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
		v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
		part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
		for i, speed in enumerate(part.speed):
			if speed < part.smin:
				part.speed[i] = part.smin
			elif speed > part.smax:
				part.speed[i] = part.smax
		part[:] = list(map(operator.add, part, part.speed))