import networkx as nx
import pydotplus
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import random
import morannode as mn

def createBiStar(n,p=10):
	G = nx.DiGraph()
	G.add_node(0,mNode=mn.MoranNode(p))
	G.add_edge(0,0)
	for i in range(1,n+1):
		G.add_node(i,mNode=mn.MoranNode(p))
		G.add_edge(i,0)
		G.add_edge(0,i)
	return G

def createStar(n,p=10):
	G = nx.DiGraph()
	G.add_node(0,mNode=mn.MoranNode(p))
	G.add_edge(0,0)
	for i in range(1,n+1):
		G.add_node(i,mNode=mn.MoranNode(p))
		G.add_edge(i,0)
	return G

def createIslands(n,p=10):
	G = nx.DiGraph()
	for i in range(n):
		G.add_node(i,mNode=mn.MoranNode(p))
	for i in range(n):
		for j in range(n):
			if i!=j:
				G.add_edge(i,j)
	return G

def createSinglets(n,p=10):
	G = nx.DiGraph()
	for i in range(n):
		G.add_node(i,mNode=mn.MoranNode(p))
	return G

class MoranGraph:
	def __init__(self,g):
		self.graph = g

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

	def moranProcess(self):
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
					toReplace = self.getLeastFitFromNode(destInd[-1])[-1]
					#print('before' + str( destM.population[toReplace].fitness.values[0]))
					destM.population[toReplace] = f
					#print('after' + str( destM.population[toReplace].fitness.values[0]))
					#print('moving ' + str(f) + ' to ' + str(destInd[-1]) + ' from ' +  str(n[0]))
					return (f)

	def getFittestFromNode(self,n):
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

	def getLeastFitFromNode(self,n):
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

	def getFittest(self):
		mFit = -1
		nInd = -1
		mInd = -1
		for i in range(len(self.graph.node)):
			f = self.getFittestFromNode(i)
			if f[0]>mFit:
				ind = f[1]
				mFit = f[0]
				mInd = f[-1]
				nInd = i

		return (nInd,mFit,mInd,''.join(ind))


def main():

	islands = MoranGraph(createIslands(10,10))
	star = MoranGraph(createStar(9,10))
	bistar = MoranGraph(createBiStar(9,10))
	singlet = MoranGraph(createSinglets(10,10))


	for gen in range(1000):


		islands.evaluateNodes()
		islands.moranProcess()

		star.evaluateNodes()
		star.moranProcess()

		bistar.evaluateNodes()
		bistar.moranProcess()

		singlet.evaluateNodes()
		singlet.moranProcess()

		print (str(islands.getFittest()[1])+","+str(star.getFittest()[1])+","+str(bistar.getFittest()[1])+","+str(singlet.getFittest()[1]))
	
	print ('islands --- ' + str(islands.getFittest()))
	print ('star --- ' + str(star.getFittest()))
	print ('bistar --- ' + str(bistar.getFittest()))
	print ('singlet ---' + str(singlet.getFittest()))

	#pos = nx.spring_layout(G.graph)
	#nx.draw_networkx(G.graph, pos, cmap=plt.get_cmap('jet'),with_labels = True, edgelist=G.graph.edges(), arrows=True)
	#plt.show()

if __name__ == "__main__":
	main()