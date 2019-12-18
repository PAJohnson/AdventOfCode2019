#Patrick Johnson
#Advent of Code 2019 day 14

#jugs of water type of puzzle

#good data structure?

#want [A,10,[[ORE,10]]] kind of structure 

import math
import time
		
def parseInput2(filename):
	
	#dict of dicts?
	# {'name' : {'qty' : numMade, 'req' : [['reqName',reqNum]] } }
	rules = {}
	f = open(filename)
	ruleStrings = []
	for row in f:
		#break input into array of strings
		#parse strings as rules later
		ruleStrings.append(row.strip())
	for rule in ruleStrings:
		#make rule out of rule string
		resList = []
		reqList = []
		reqs = []
		qty = 0
		resList = rule.split(' => ')
		reqList = resList[0]
		resList = resList[1]
		resList = resList.split(' ')
		qty = int(resList[0])
		res = resList[1]
		reqList = reqList.split(', ')
		for req in reqList:
			req = req.split(' ')
			reqs.append([req[1],int(req[0])])
		rules.update({ res : { 'qty' : qty, 'req' : reqs } })	
	
	return rules
		
def ruleParseOrder(rules):
	#rules is a composite dict
	# {'name' : {'qty' : numMade, 'req' : [['reqName',reqNum]] } }
	#turn into dict of {name : [reqs]}
	#what do we want? a new dict with depth information
	#so that we can parse by depth first order
	#how to get depth
	ruleDepth = {}
	ruleParseDict = {}
	for key,val in rules.items():
		name = key
		reqsList = []
		for reqs in val['req']:
			reqsList.append(reqs[0])
		ruleParseDict.update({name : reqsList})
		
	#find fuel
	ruleDepth.update({'ORE' : 0})
	while len(ruleDepth) != len(ruleParseDict)+1:
		for key,val in ruleParseDict.items():
			for req in val:
				if req in ruleDepth:
					depth = ruleDepth[req] + 1
					#append depths until ruleDepth list is full
					ruleDepth.update({ key : depth})
	maxDepth = 0
	for key, val in ruleDepth.items():
		if val > maxDepth:
			maxDepth = val
	for key, val in ruleDepth.items():
		ruleDepth[key] = maxDepth-ruleDepth[key]
		
	#make new dict of vals, collate depths
	depthList = [[] for i in range(maxDepth+1)]
	for key,val in ruleDepth.items():
		depthList[val].append(key)
		
	return depthList
		
def reqsDict(rules):
	reqsDict = {}
	for key in rules:	
		reqsDict.update({key : 0})	
	return reqsDict

def requiredList(required):
	l = []
	for req in required:
		if required[req] != 0:
			l.append(req)
	return l
	
def requiredUpdate(rules,required,leftovers,r):
	#update required to include components and qty required by r
	#according to rules
	if leftovers[r] >= required[r]:
		leftovers[r] -= required[r]
		qty = 0
	elif leftovers[r] < required[r]:
		qty = required[r] - leftovers[r]
		leftovers[r] = 0
	#print(leftovers)
	if qty != 0:
		leftovers[r] += (math.ceil((qty/rules[r]['qty']))*rules[r]['qty'] - qty)
		for comp in rules[r]['req']:
			required[comp[0]] += math.ceil((qty/rules[r]['qty'])) * comp[1]
	required[r] = 0
	
def reqDepth(required,depthDict,parseOrder):
	#return lowest depth of a required element
	depth = len(parseOrder)
	for key,val in required.items():
		if depthDict[key] < depth and val != 0:
			depth = depthDict[key]
	return depth
	
def part1(fuelReq):
	ore = 0
	parseIndex = 0
	required = reqsDict(rules)
	required.update({'ORE' : 0})
	required['FUEL'] = fuelReq
	leftovers = {}
	for key,val in required.items():
		leftovers.update({key:0})
	for l in parseOrder:
		if 'FUEL' in l:
			parseIndex = parseOrder.index(l)
	while required['ORE'] == 0 and parseIndex < len(parseOrder):
		allowedReq = parseOrder[parseIndex].copy()
		checkFor = requiredList(required)
		for r in checkFor:
			if r in allowedReq:
				#mutate required here
				requiredUpdate(rules,required,leftovers,r)
				allowedReq.remove(r)
				
		parseIndex += 1

		if reqDepth(required,depthDict,parseOrder) < parseIndex:
			parseIndex = reqDepth(required,depthDict,parseOrder)
	return required['ORE']

def part2():
	#given 1 trillion ore, what is max amount of FUEL that can be produced?
	oreCargo = 	1000000000000
				
	fuelReq = 10000
	fuelDiff = 1000000
	oldDirection = 0
	while fuelDiff > 1:
		oreReq = part1(fuelReq)
		print("oreReq = " + str(oreReq) + " fuelReq = " + str(fuelReq))
		if oreReq < oreCargo:
			#bump up fuelReq
			direction = 1
			fuelReq += fuelDiff
		elif oreReq > oreCargo:
			direction = -1
			fuelReq -= fuelDiff
		if oldDirection != direction:
			fuelDiff = int(fuelDiff/2)
		oldDirection = direction
	print("oreReq = " + str(part1(fuelReq)) + " fuelReq = " + str(fuelReq))
	while part1(fuelReq) < oreCargo:
		fuelReq += 1
	while part1(fuelReq) > oreCargo:
		fuelReq -= 1
	
	return fuelReq
		
#testing
rules = parseInput2('input.txt')
#print(rules)
parseIndex = 0
parseOrder = ruleParseOrder(rules)
#print(parseOrder)
required = reqsDict(rules)
#print(required)
required.update({'ORE' : 0})
#still not getting right answer!!!
#is there a smarter way???
depthDict = {}
leftovers = {}
needed  = requiredList(required)
for i in range(len(parseOrder)):
	for req in parseOrder[i]:
		depthDict.update({req:i})
for key,val in required.items():
	leftovers.update({key:0})
print(part1(1))

print(part2())
