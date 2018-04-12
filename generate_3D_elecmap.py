## This is an example to extract electrostatic interaction and record on each grid point
## In this case, MOLARIS was used to run molecular dynamic simulation.

import numpy as np
import sys
from multiprocessing import Pool


numMutants = 786
numLigAtom = 92
maxcoord = [29.5, 31.5,  25]
mincoord = [ 9.5, 14.5, 9.5]
interval = 0.5
gauss_sig = 0.5

path = './'
elec_filename = 'electro_res_atm.dat'

x = np.arange(mincoord[0],maxcoord[0]+interval , interval)
y = np.arange(mincoord[1],maxcoord[1]+interval , interval)
z = np.arange(mincoord[2],maxcoord[2]+interval , interval)

atomdict = {"C" : 1, "H" : 2, "O" : 3, "N" : 4, "S" : 5}

def writeElec(center_idx, point_elec, coord, atomtype):

	elecmat = np.zeros( (len(x), len(y), len(z), 7))
	for i in range(center_idx[0]-5,center_idx[0]+6):
		if(i < 0 or i >= len(x)):
			continue
		for j in range(center_idx[1]-5,center_idx[1]+6):
			if(j < 0 or j >= len(y)):
				continue
			for k in range(center_idx[2]-5,center_idx[2]+6):
				if(k < 0 or k >= len(z)):
					continue

				distance = np.sqrt((coord[0]-x[i])**2 + (coord[1]-y[j])**2 + (coord[2]-z[k])**2)
				elecmat[i][j][k][0] = point_elec * np.exp(-np.power(distance,2)/(2*gauss_sig**2))

				if(atomtype in atomdict):
					atm_idx = atomdict[atomtype]
					elecmat[i][j][k][atm_idx] = np.exp(-np.power(distance,2)/(2*gauss_sig**2))
				else:
					elecmat[i][j][k][6] = np.exp(-np.power(distance,2)/(2*gauss_sig**2))


			#	print(elecmat[i][j][k])
	
	return elecmat


def makeElecMap(elec, coords, atomtype): 	
	elecmat = np.zeros( (len(x), len(y), len(z), 7))

	#np.set_printoptions(threshold=np.inf)
	for i in range(0,numLigAtom):
		
		near_x_idx = int(np.around(coords[i][0] - mincoord[0])/interval)
		near_y_idx = int(np.around(coords[i][1] - mincoord[1])/interval)
		near_z_idx = int(np.around(coords[i][2] - mincoord[2])/interval)

		curr_elecmat = writeElec([near_x_idx, near_y_idx, near_z_idx], elec[i], coords[i], atomtype[i])
		elecmat = elecmat + curr_elecmat
		#print(elec[i], "  :  ", [near_x_idx, near_y_idx, near_z_idx])
		#if i==0:
		#	print(distmat[22,26,17])
		#	print(elecmat[22,26,15])
	return elecmat


def readFile(idx):
	path = './' + str(idx) + '/'
	#print("Generate eletro map " + str(idx))

	filename = path+elec_filename


	avg_elecmat = np.zeros( (len(x), len(y), len(z), 7))
	with open(filename, 'r') as file:
		flag = -1
		total_iter = 0
		for line in file:	
			if (len(line.split()) > 0 and  line.split()[0] == "------"):
				flag = flag * -1  ##becomes 1 if it is the beginning of a new block

				if(flag == -1):   ##the end of a block
					total_iter = total_iter+1
					avg_elecmat = avg_elecmat + makeElecMap(elec, coords, atomtype)
					#print(total_iter)
					#if(total_iter ==2):
					#	break

				i = 0
				elec = np.zeros((numLigAtom,1))
				coords =  np.zeros((numLigAtom,3))
				atomtype = np.chararray(numLigAtom)
				
				continue

			if(flag == 1):
				splitline = line.split()
				elec[i] =      float(splitline[4])
				coords[i][0] = float(splitline[5])
				coords[i][1] = float(splitline[6])
				coords[i][2] = float(splitline[7])
				atomtype[i] =  splitline[1][0]
				#print(total_iter, "///",i," : ", atomtype[i], " : ", elec[i], " , ", coords[i])
				i=i+1

		avg_elecmat = avg_elecmat/total_iter

		return avg_elecmat



#for i in range(1,numMutants+1):

if __name__ == '__main__':
	pool = Pool(processes=20)
	results = pool.map(readFile, range(1,787))

	data = np.array(results)
	np.save('elecmap_data_avg', data)



