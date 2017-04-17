import networkx as nx
import pydotplus
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import random
import morannode as mn

def createMegaStar(l,r,k,p=10):
	G = nx.DiGraph()
	G.add_node(0)
	G.add_node(1)
	cn = 2
	npl = r+k
	n = l*npl
	for i in range(l):
		for j in range(0,r):
			G.add_node(cn)
			G.add_edge(0,cn)
			cn += 1
		G.add_node(cn)
		an = cn
		for j in range(0,r):
			G.add_edge(an-j-1,an)
		cn+=1
		kn = cn
		for j in range(0,k):
			G.add_node(cn)
			G.add_edge(an,cn)
			cn += 1
		for j in range(0,k):
			G.add_edge(kn+j,1)
			for m in range(k):
				if m != j:
					G.add_edge(kn+j,kn+m)

	return G

def createBiStar(n,p=10):
	G = nx.DiGraph()
	G.add_node(0)
	G.add_edge(0,0)
	for i in range(1,n+1):
		G.add_node(i)
		G.add_edge(i,0)
		G.add_edge(0,i)
	return G

def createStar(n,p=10):
	G = nx.DiGraph()
	G.add_node(0)
	G.add_edge(0,0)
	for i in range(1,n+1):
		G.add_node(i)
		G.add_edge(i,0)
	return G

def createIslands(n,p=10):
	G = nx.DiGraph()
	for i in range(n):
		G.add_node(i)
	for i in range(n):
		for j in range(n):
			if i!=j:
				G.add_edge(i,j)
	return G

def createSinglets(n,p=10):
	G = nx.DiGraph()
	for i in range(n):
		G.add_node(i)
	return G

class MoranGraph:
	def __init__(self,g,p=10):
		self.graph = g
		for n in self.graph.nodes(data=True):
			n[1]['mNode']=mn.mnParticleSwarm(p)

	def evaluateNodes(self):
		for n in self.graph.nodes(data=True):
			n[1]['mNode'].evaluateNode()

	def normaliseFitness(self):
		totalFitness = 0

		for n in self.graph.nodes(data=True):
			for f in n[1]['mNode'].population:
				totalFitness += f.fitness.values[0]
		rTotalFitness=1.0/totalFitness
		for n in self.graph.nodes(data=True):
			for i in range(len(n[1]['mNode'].population)):
				f = n[1]['mNode'].population[i]
				f.nFitness = f.fitness.values[0]*rTotalFitness

	def moranProcess(self,maximise=True):
		self.normaliseFitness()
		s = random.uniform(0,1)
		t = 0
		for n in self.graph.nodes(data=True):
			for f in n[-1]['mNode'].population:
				t+=f.nFitness
				if(t>s):
					if (len(self.graph.edges(n[0]))<1):
						#print('node has no edges')
						return f
					destInd = random.choice(self.graph.edges(n[0]))
					if (destInd[-1] == n[0]):
						#print('node has no outgoing edges')
						return f
					dest = self.graph.node[destInd[-1]]
					destM = dest['mNode']
					toReplace = self.getMaxFitnessFromNode(destInd[-1])[-1]
					#print('before' + str( destM.population[toReplace].fitness.values[0]))
					destM.population[toReplace] = f
					#print('after' + str( destM.population[toReplace].fitness.values[0]))
					#print('moving ' + str(f) + ' to ' + str(destInd[-1]) + ' from ' +  str(n[0]))
					return (f)

	def getMaxFitnessFromNode(self,n):
		mFit = -1
		mInd = -1
		fittest = []
		for i in range(len(self.graph.node[n]['mNode'].population)):
			f = self.graph.node[n]['mNode'].population[i]
			if (f.fitness.values[0]>mFit):
				mFit = f.fitness.values[0]
				mInd = i
				fittest = f

		return (mFit,fittest,mInd)

	def getMinFitnessFromNode(self,n):
		mFit = -1
		mInd = -1
		fittest = []
		for i in range(len(self.graph.node[n]['mNode'].population)):
			f = self.graph.node[n]['mNode'].population[i]
			if (f.fitness.values[0]<mFit):
				mFit = f.fitness.values[0]
				mInd = i
				fittest = f

		return (mFit,fittest,mInd)

	def getMaxFitness(self):
		mFit = -1
		nInd = -1
		mInd = -1
		for i in range(len(self.graph.node)):
			f = self.getMaxFitnessFromNode(i)
			if f[0]>mFit:
				ind = f[1]
				mFit = f[0]
				mInd = f[-1]
				nInd = i

		return (nInd,mFit,mInd,ind)

	def getMinFitness(self):
		mFit = -1
		nInd = -1
		mInd = -1
		for i in range(len(self.graph.node)):
			f = self.getMinFitnessFromNode(i)
			if f[0]<mFit:
				ind = f[1]
				mFit = f[0]
				mInd = f[-1]
				nInd = i

		return (nInd,mFit,mInd,ind)

	def runStep(self):
		self.evaluateNodes()
		self.moranProcess()
