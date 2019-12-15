#Patrick Johnson
#advent of code day 12 2019

#N-body problem
#semi bad physics simulation
#moons of jupiter
#each moon has x,y,z position
#Io, Europa, Ganymede, Callisto

from dataclasses import dataclass
import matplotlib.pyplot as plt
from itertools import permutations, combinations


def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)
    
    
#refactor later! too hard.
class Moon():
	
	def __init__(self,pos):
		#init moon with position
		self.xp = pos[0]
		self.yp = pos[1]
		self.zp = pos[2]
		self.xv = 0
		self.yv = 0
		self.zv = 0		

def updateVel(moon1, moon2):
	# "apply gravity"
	if moon1.xp != moon2.xp:
		moon1.xv += (moon2.xp-moon1.xp)/abs(moon1.xp-moon2.xp)
		moon2.xv -= (moon2.xp-moon1.xp)/abs(moon1.xp-moon2.xp)
	if moon1.yp != moon2.yp:
		moon1.yv += (moon2.yp-moon1.yp)/abs(moon1.yp-moon2.yp)
		moon2.yv -= (moon2.yp-moon1.yp)/abs(moon1.yp-moon2.yp)
	if moon1.zp != moon2.zp:
		moon1.zv += (moon2.zp-moon1.zp)/abs(moon1.zp-moon2.zp)
		moon2.zv -= (moon2.zp-moon1.zp)/abs(moon1.zp-moon2.zp)

		
def printMoon(moon):
	print("pos=<x=%s, y=%s, z=%s>, vel=<x=%s, y=%s, z=%s>" % \
			(moon.xp, moon.yp, moon.zp, moon.xv, moon.yv, moon.zv))
	
def updatePos(moon):
	moon.xp += moon.xv
	moon.yp += moon.yv
	moon.zp += moon.zv
	
def motionSim(m):
	#update velocities
	perm = combinations([0,1,2,3],2)
	for p in list(perm):
		updateVel(m[p[0]],m[p[1]])
	for moon in m:
		updatePos(moon)
	
def motionSteps(m,steps,printDes):
	for i in range(steps):
		if printDes:
			print("Time step " + str(i))
			printMoon(m)
		motionSim(m)
		
def moonEnergy(moon):
	pot = abs(moon.xp) + abs(moon.yp) + abs(moon.zp)
	kin = abs(moon.xv) + abs(moon.yv) + abs(moon.zv)
	print("%s, %s" % (pot,kin))
	return pot*kin
	
def totalEnergy(m):
	energy = sum([moonEnergy(moon) for moon in m])
	return energy
	
def parseInput(filename):
	f = open(filename)
	lines = []
	line = []
	init = []
	for row in f:
		lines = row.strip().strip('<').strip('>').split(', ')
		lines[0] = int(lines[0].strip('x').strip('='))
		lines[1] = int(lines[1].strip('y').strip('='))
		lines[2] = int(lines[2].strip('z').strip('='))
		init.append(lines)
		
	m1 = [init[0][0],init[0][1],init[0][2]]
	m2 = [init[1][0],init[1][1],init[1][2]]
	m3 = [init[2][0],init[2][1],init[2][2]]
	m4 = [init[3][0],init[3][1],init[3][2]]
	return [m1,m2,m3,m4]
		
def matchPos(m,pos,dim):
	true = []
	if dim == 'x':
		for i in range(len(m)):
			if m[i].xp == pos[i].xp:
				true.append(1)
			else:
				true.append(0)
		if sum(true) == 4:
			return True
	elif dim == 'y':
		for i in range(len(m)):
			if m[i].yp == pos[i].yp:
				true.append(1)
			else:
				true.append(0)
		if sum(true) == 4:
			return True
	elif dim == 'z':
		for i in range(len(m)):
			if m[i].zp == pos[i].zp:
				true.append(1)
			else:
				true.append(0)
		if sum(true) == 4:
			return True	
	else:
		return False
		
def findPeriod(m,start):
	count = 0
	found = [False,False,False]
	target = [True,True,True]
	period = [0,0,0]
	while target != found:
		#search for matches
		count += 1
		motionSim(m)
		if matchPos(m,start,'x') == True and found[0] == False:
			found[0] = True
			period[0] = count
			print("found x: " + str(count))
		if matchPos(m,start,'y') == True and found[1] == False:
			found[1] = True
			period[1] = count
			print("found y: " + str(count))
		if matchPos(m,start,'z') == True and found[2] == False:
			found[2] = True
			period[2] = count
			print("found z: " + str(count))
	return lcm(period[0]+1, lcm(period[1]+1, period[2]+1))

#part 1
start = parseInput('input.txt')
m = []
stm = []
for st in start:
	m.append(Moon(st))
	stm.append(Moon(st))

#hist = motionSteps(m,100,False)
#print(totalEnergy(m))

#part 2
#find how many steps it takes before universe repeats itself!
#number of steps before positions and velocities exactly match
#need to find a smarter way to calculate moonUpdate...
#can be directly calculate oscillation period?
#look at the data
#oscillations are not the way to go
#how to do this without a time history and comparing them?
#if orbit is periodic, will it always return to the initial state?
#assume initial state is dynamically stable
print(findPeriod(m,stm))
