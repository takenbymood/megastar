import networkx as nx
import pydotplus
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import random
import morannode as mn

def createStar(n):
	G = nx.DiGraph()
	G.add_node(0)
	edges = []
	for i in range(n):
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
				print f.nFitness
				totalFitness += f.fitness.values[0]
		rTotalFitness=1.0/totalFitness
		for n in self.graph.nodes(data=True):
			for i in range(len(n[1]['mNode'].population)):
				f = n[1]['mNode'].population[i]
				f.nFitness = f.fitness.values[0]*rTotalFitness

	def selectIndividual(self):
		self.normaliseFitness()
		s = random.uniform(0,1)
		t = 0
		for n in self.graph.nodes(data=True):
			for f in n[1]['mNode'].population:
				t+=f.nFitness
				if(t>s):
					return (f)


def main():
	G = MoranGraph(createStar(10))
	G.evaluateNodes()
	print G.selectIndividual()

	pos = nx.spring_layout(G.graph)
	nx.draw_networkx(G.graph, pos, cmap=plt.get_cmap('jet'),with_labels = True, edgelist=G.graph.edges(), arrows=True)
	plt.show()

if __name__ == "__main__":
	main()