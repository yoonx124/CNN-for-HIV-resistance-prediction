
with open('template.inp', 'r') as file : 
	filedata = file.read()

with open('3list.txt', 'r') as listfile:
	i = 1
	for line in listfile:
		filename = "mut" + str(i) + ".inp"

		strlist = line.split()
		
		mut_list = ""
		for j in range(0, len(strlist)):
			if j % 2 == 0 :
				resnum = int(strlist[j])
				mut_list = mut_list + " " + str(resnum) + " " + strlist[j+1] + " " + str(99+resnum) + " " + strlist[j+1]
		newdata = filedata.replace('xxx', mut_list+'\n')

		i=i+1

		with open(filename, 'w') as file:
			file.write(newdata)



