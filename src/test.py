import cPickle
import sys

if __name__ == '__main__':
	nodes = dict()
	with open(sys.argv[1]) as IN:
		IN.readline()
		
		for line in IN:
			nodes[line.strip().split(' ')[0]] = 1
	with open(sys.argv[2]) as IN:
		IN.readline()
		for line in IN:
			assert(line.strip().split(' ')[0] in nodes)