import networkx as nx
import pydotplus
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import random
import morannode as mn

def createStar(n):
	G = nx.DiGraph()
	G.add_node(0,mNode=mn.MoranNode(10))
	G.add_edge(0,0)
	edges = []
	for i in range(1,n+1):
		G.add_node(i,mNode=mn.MoranNode(10))
		G.add_edge(i,0)
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
					destInd = random.choice(self.graph.edges(n[0]))
					if (destInd[-1] == n[0]):
						#print('node has no outgoing edges')
						return f
					dest = self.graph.node[destInd[-1]]
					destM = dest['mNode']
					toReplace = random.randint(0,len(destM.population)-1)
					destM.population[toReplace] = f
					#print('moving ' + str(f) + ' to ' + str(destInd[-1]) + ' from ' +  str(n[0]))
					return (f)

	def getFittestFromNode(self,n):
		mFit = -1
		mInd = -1
		for i in range(len(self.graph.node[n]['mNode'].population)):
			f = self.graph.node[n]['mNode'].population[i]
			if (f.fitness.values[0]>mFit):
				mFit = f.fitness.values[0]
				mInd = i

		return (mFit,mInd)


def main():

	G = MoranGraph(createStar(3))


	for gen in range(100):
		G.evaluateNodes()
		G.moranProcess()
		print (G.getFittestFromNode(0)[0])

	pos = nx.spring_layout(G.graph)
	nx.draw_networkx(G.graph, pos, cmap=plt.get_cmap('jet'),with_labels = True, edgelist=G.graph.edges(), arrows=True)
	plt.show()

if __name__ == "__main__":
	main()