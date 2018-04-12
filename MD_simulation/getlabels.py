import numpy as np

numMutants = 786
first_thresh = 3
second_thresh = 15


labels = np.zeros((numMutants, 1))
with open('foldlist.txt', 'r') as listfile:
	i = 0
	for line in listfile:
		number = float(line)
		if number <= first_thresh :
			labels[i] = 0
		elif number <= second_thresh :
			labels[i] = 1
		else :
			labels[i] = 2
		i=i+1

	
	np.save('labels', labels)

			

