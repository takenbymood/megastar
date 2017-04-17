import network as mnet
import toolbox as tb

def main():

	islands = mnet.MoranGraph(mnet.createMegaStar(4,3,3,10))

	csv = "n,islands\n"

	f = open('fitness.csv', 'w')
	f.write(csv)

	for gen in range(1000):
		islands.runStep()
		line = str(gen)+","+str(islands.getMaxFitness()[1])
		print(line)
		f.write(line+"\n")

	#print ('islands --- ' + str(islands.getFittest()[-1]))


if __name__ == "__main__":
	main()