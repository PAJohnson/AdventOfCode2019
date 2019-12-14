#Patrick Johnson
#advent of code day 12 2019

#N-body problem
#semi bad physics simulation
#moons of jupiter
#each moon has x,y,z position
#Io, Europa, Ganymede, Callisto

from dataclasses import dataclass

class Moon():
	
	def __init__(self,x,y,z):
		#init moon with position
		self.xp = x
		self.yp = y
		self.zp = z
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
	
def motionSim(moon1, moon2, moon3, moon4):
	#update velocities
	updateVel(moon1,moon2)
	updateVel(moon1,moon3)
	updateVel(moon1,moon4)
	updateVel(moon2,moon3)
	updateVel(moon2,moon4)
	updateVel(moon3,moon4)
	
	updatePos(moon1)
	updatePos(moon2)
	updatePos(moon3)
	updatePos(moon4)
	
def motionSteps(m1,m2,m3,m4,steps,printDes):
	for i in range(steps):
		if printDes:
			print("Time step " + str(i))
			printMoon(m1)
			printMoon(m2)
			printMoon(m3)
			printMoon(m4)
		motionSim(m1,m2,m3,m4)
		
def moonEnergy(moon):
	pot = abs(moon.xp) + abs(moon.yp) + abs(moon.zp)
	kin = abs(moon.xv) + abs(moon.yv) + abs(moon.zv)
	print("%s, %s" % (pot,kin))
	return pot*kin
	
def totalEnergy(m1,m2,m3,m4):
	return (moonEnergy(m1) + moonEnergy(m2) + moonEnergy(m3) + moonEnergy(m4))
	
	
m1 = Moon(1,2,-9)
m2 = Moon(-1,-9,-4)
m3 = Moon(17,6,8)
m4 = Moon(12,4,2)
#part 1
motionSteps(m1,m2,m3,m4,1000,False)
print(totalEnergy(m1,m2,m3,m4))

#part 2
#find how many steps it takes before universe repeats itself!
#number of steps before positions and velocities exactly match
#need to find a smarter way to calculate moonUpdate...
#can be directly calculate oscillation period?

