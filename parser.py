"""
Taking an fMRI data file, this program first extracts a table out of a row 
and then generates a csv file containing all the tables.

In a lab at uWaterloo, participants were shown 40 picture set,
each set containing 15 pictures. Researchers were interested in parts of data
generated for each picture. So, they wanted a table for each participant 
with 40*15=600 rows and 13 columns"""

import numpy as np 

def ListToMatrix(dataList):

	"""This function generates a 600 by 7 matrix from a list of (length > 3100)"""
	
	rawMatrix=[[None]*7]*600 # an empty matrix in python
	dataMatrix=np.array(rawMatrix) #to convert the empty matrix to a NumPy matrix
	
	for n in range(40):  # a loop for 40 picture sets
	
		for i in range(15):  # a loop for 15 pictures
		
			for j in range(4):  # a loop for to fill first 4 column of the matrix
				dataMatrix[15*n + i][j]=dataList[21 + n*77 + i*4 + j]
			
			# the following is to fill the columns 5 to 7
			dataMatrix[15*n + i][4]=dataList[81 + n*77 + i]
			dataMatrix[15*n + i][5]=dataList[96 + n*77 ]
			dataMatrix[15*n + i][6]=dataList[97 + n*77 ]
	
	return dataMatrix
	
# let's read the file 

# you need to replace the 'fMRI.csv' in the following line with the address of the data file in your computer

rawFile=open('fMRI.csv')
listOfLines=rawFile.readlines()

# since we don't care about the first two lines, we parse the rest

parsedLines=[]

for i in range(2,len(listOfLines)):
	parsedLines.append(listOfLines[i].split(','))

matrices=[]	
for i in range(len(parsedLines)):	
	matrices.append(ListToMatrix(parsedLines[i]))
	
# now let's bring in the side information, this information are common for all participant 

sideMatrix=np.genfromtxt('Example_File.csv',dtype=None, delimiter=',')
sideList=[list(x) for x in sideMatrix]

sideBySide=[]

for i in range(len(matrices)):
	sideBySide.append(np.hstack((sideList,matrices[i])))
	
verticalFile=np.vstack(sideBySide)

# now that we have the data, we put them in a csv file

import csv

# you have to provide the address for the output file: replace the 'parsedData.csv' with your desired name
with open('parsedData.csv', 'w') as output:
    writer=csv.writer(output,lineterminator='\n')
    writer.writerows(verticalFile)


