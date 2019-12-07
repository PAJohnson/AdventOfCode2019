#day 6 advent of code
#Patrick Johnson

#orbit problem
#create a linked list or tree type of structure
#count the number of direct and indirect orbits
import csv
from functools import partial

#input is not ordered and orbit list might not form a single tree

class Tree:
	def __init__(self, root, depth):
		#root is a name
		#leaves is a list of trees
		self.root = root
		self.leaves = []
		self.depth = depth
		
	def getLeaves(self):
		return self.leaves
		
	def addLeaf(self,tree):
		self.leaves.append(tree)	
		
def onRight(relList, item):
	ret = 0
	for rel in relList:
		if item == rel[1]:
			return 1
	
	return ret		

def listSort(relListO):
	#this function takes a relation list and sorts
	#it such that makeTree will work
	#the left side of each successive relation must exist
	#above it as the right side somewhere (with exception
	#of COM)	
	relList = relListO.copy()	
	newList = []
	#extract COM
	for rel in relList:
		if rel[0] == 'COM':
			newList.append(rel)
			relList.remove(rel)
			
	while len(relList) > 0:
		for rel in relList:
			if onRight(newList,rel[0]):
				newList.append(rel)
				relList.remove(rel)
				
	return newList
			
def findOrbit(relList,item):
	for rel in relList:
		if rel[1] == item:
			return rel[0]
			
def getDepth(dList, key):
	for item in dList:
		if key == item[0]:
			return item[1]
	
	

def addOrbit(tree,name,val):
	if name == tree.root:
		tree.addLeaf(Tree(val,tree.depth+1))
		#print("node: " + val + " depth = " + str(tree.depth))
	else:
		if not tree.leaves:
			return
		else:
			for leaf in tree.getLeaves():
				addOrbit(leaf,name,val)

flatTree = []

def printTree(tree):
	global flatTree
	smallList = []
	#print("root: " + tree.root + " leaves: ", end='')
	for leaf in tree.getLeaves():
		print(leaf.root + "," + str(leaf.depth))
		smallList.append(leaf.root)
		smallList.append(leaf.depth)
		flatTree.append(smallList)
		#return list(leaf.root,str(leaf.depth))
	if not tree.leaves:
		return
	else:
		for leaf in tree.leaves:
			printTree(leaf)

def makeList(relList,key):
	newKey = key
	newList = []
	while newKey != "COM":
		for rel in relList:
			if rel[1] == newKey:
				newKey = rel[0]
				newList.append(rel)
				
	return newList

def parseOrbits(filename):
	orbitList = []
	f = open(filename)
	for row in f:
		#split the row into the orbiting objects
		rowList = list(str(row).strip().split(')'))
		orbitList.append(rowList)
			
	#orbitList is now a list of relations between objects
	return orbitList
	
def makeTree(relList):
	#return some kind of tree type structure
	#relations between items are help in relList
	
	#start by hard-coding first part of tree
	#this will not work if the list is not sorted!
	#have to do this smarter
	orbTree = Tree(relList[0][0],0)
	orbTree.addLeaf(Tree(relList[0][1],1))
	
	for rel in relList[1:]:
		addOrbit(orbTree,rel[0],rel[1])
			
	return orbTree
		
		
def countOrbits(tree, depth):
	count = depth
	#print("root: " + tree.root + " depth = " + str(depth))
	if not tree.leaves:
		return depth
	else:
		for leaf in tree.leaves:
			count += countOrbits(leaf,depth+1)
		return count
		
		
def commonOrigin(listOne,listTwo):
	length1 = len(listOne)
	length2 = len(listTwo)
	llist = [length1,length2]
	comDepth = 0
	for i in range(min(llist)):
		if listOne[i] == listTwo[i]:
			comDepth += 1
			
	return comDepth

def getCommon(orbList,keyOne,keyTwo):
	global flatTree
	keyLOne = makeList(orbList,keyOne)
	keyLTwo = makeList(orbList,keyTwo)
	keyLOne.reverse()
	keyLTwo.reverse()
	depthSrc = len(keyLOne)
	depthDest = len(keyLTwo)
	depthCom = commonOrigin(keyLOne,keyLTwo)
	dist = (depthSrc - depthCom) + (depthDest - depthCom)
	return dist
	
#part 1
#now, to count orbits



orbL = parseOrbits('input.txt')
orbLNew = listSort(orbL)
#print(orbL)
#print(orbLNew)
orbTree = makeTree(orbLNew)
printTree(orbTree)
print(getCommon(orbLNew,'YOU','SAN'))
#print(getDepth(flatTree,'K'))
#print(countOrbits(orbTree,0))



#part 2
#find minimum distance between two points
print("san orbits: " + findOrbit(orbL,'SAN'))
print("you orbit: " + findOrbit(orbL,'YOU'))

#want to return a list containing the path to an item in the tree
#is it possible without upward references??

	#find minimum distance between source and dest in the tree
	#make two new trees
	#one tree is from COM to source, save depth
	#one tree is from COM to dest, save depth
	#find the common point with the highest depth
	#dist = (depthSrc - depthCom) + (depthDest - depthCom)

print(getCommon(orbLNew,"YOU","SAN")-2)
