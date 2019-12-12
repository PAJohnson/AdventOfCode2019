#Patrick Johnson
#day 10 advent of code 2019
#asteroid visibility problem

#similar to the other question with line intersection stuff.

import math
from itertools import cycle

def parseInput(filename):
	#returns a list of lists
	#indexing as data[right][height] works as expected
	#easier to reason about
	data = []
	dataRow = []
	f = open(filename)
	for row in f:
		for char in row.strip():
			if char == '#':
				dataRow.append(1)
			elif char == '.':
				dataRow.append(0)
		data.append(dataRow)
		dataRow = []		
			
	#transform data from list of rows to list of columns
	height = len(data)
	width = len(data[0])
	col = []
	newData = []
	for w in range(width):
		for h in range(height):
			col.append(data[h][w])	
		newData.append(col)
		col = []
	return newData
	
def listToDict(data):
	newDict = {}
	for w in range(len(data)):
		for h in range(len(data[0])):
			newDict.update({(w,h) : data[w][h]})
			
	return newDict	

def getLIVector(vector):
	#given an arbitrary vector, find the smallest vector that is
	#a factor of the input vector that is still integers
	
	#find gcf of the components of the input vector, divide
	#the input vector by the gcf, return
	x = 0
	y = 0
	return (int(vector[0]/math.gcd(vector[0],vector[1])),int(vector[1]/math.gcd(vector[0],vector[1])))

def getNumObservable(posDict,posList):
	#get width and height from posList
	width = len(posList)
	height = len(posList[0])
	newDict = {}
	obsDict = {}
	#for coordinate in posDict
	#for coord, exist in posDict.items():
	coord = (3,4)
	#if that coordinate exists, check observable
	for coord, exist in posDict.items():
		if exist == 1:
			for w in range(width):
				for h in range(height):
					#for every point in posList
					if (w,h) != coord and posList[w][h] == 1:
						LIVector = getLIVector([w-coord[0],h-coord[1]])
						if LIVector in obsDict:
							obsDict[LIVector].append((w,h))
						else:
							obsDict.update({LIVector:[(w,h)]})
			newDict.update({coord : obsDict})
			#print("observable for point: " + str(coord) + " = " + str(obsDict))
			obsDict = {}
	return newDict
					
	

#convert to a dict?
def getPosition(data):
	posDict = listToDict(data)
	obsDict = getNumObservable(posDict,data)
	coMax = []
	obsMax = 0
	#want a dictionary of positions and #observable asteroids
	for coords, observable in obsDict.items():
		if observable > obsMax:
			obsMax = observable
			coMax = [coords]
	return coMax

def part1():
	maxObs = 0
	for coord, _ in obsDict.items():
		if len(obsDict[coord]) > maxObs:
			maxObs = len(obsDict[coord])
			maxKey = coord
		
	print(maxObs)

def getMaxKey(obsDict):
	maxObs = 0
	for coord, _ in obsDict.items():
		if len(obsDict[coord]) > maxObs:
			maxObs = len(obsDict[coord])
			maxKey = coord
		
	return maxKey

def getDistance(p1,p2):
	#return distance between points
	return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5
	
def makeVapeList(obsDict):
	vapeList = []
	keyList = list(obsDict.keys())
	numIter = 0
	index = 0
	for key,val in obsDict.items():
		numIter += len(val)
		
	while numIter > 0:
		for key,val in obsDict.items():
			if obsDict[key] != []:
				vapeList.append(obsDict[key][0])
				obsDict[key].remove(val[0])
				numIter -= 1
		
	return vapeList

def reorderDistance(obsDict,coord):
	#obsDict is ordered
	#coord is "origin"
	#for each key in obsDict, sort the value lists in obsDict by 
	#distance from coord
	for key, valList in obsDict.items():
		#make distance list
		pList = valList.copy()
		pListNew = []
		distList = []
		for point in valList:
			distList.append(getDistance(coord,point))
		#make new point list ordered by distance
		while distList:
			index = distList.index(min(distList))
			pListNew.append(pList[index])
			distList.remove(min(distList))
			pList.remove(pList[index])
		obsDict[key] = pListNew


def reorderDirection(obsDict):
	newDict = {}
	angleDict = {}
	angleList = []
	keyList = []
	newKeyList = []
	#before this, get a good grasp of the obsDict structure
	for key, _ in obsDict.items():
		angle = math.degrees(math.atan2(key[1],key[0]))
		if angle == 0.0:
			angle = 0.0
		else:
			angle += 360.0
		angle += 90
		if angle >= 360.0:
			angle -= 360
		angleList.append(angle)
		keyList.append(key)
	
	while angleList:
		index = angleList.index(min(angleList))
		newKeyList.append(keyList[index])
		angleList.remove(min(angleList))
		keyList.remove(keyList[index])
		
	#at this point, keyList is sorted by angle ccw starting at -90
	
	for i in range(len(newKeyList)):
		newDict.update({newKeyList[i] : obsDict[newKeyList[i]]})
	
	#newDict is now obsDict reordered in the correct way
	return newDict

def part2():
	maxKey = getMaxKey(obsDict)
	maxDict = obsDict[maxKey]
	maxDict = reorderDirection(maxDict)
	reorderDistance(maxDict,maxKey)
	vapeList = makeVapeList(maxDict)
	print(vapeList[200-1])

#part 1	
#print(parseInput('test1.txt'))
#print(listToDict(parseInput('test1.txt')))
posList = parseInput('input.txt')
posDict = listToDict(posList)
obsDict = getNumObservable(posDict,posList)
part1()

#part 2
#vaporize in clockwise order
#reorder dict twice
#reorder so that directions are in counterclockwise direction
#starting pointing straight down
#reorder the list of observable points in each direction so that
#the first point in the list is closest to coord ...

#reorder by direction
part2()
