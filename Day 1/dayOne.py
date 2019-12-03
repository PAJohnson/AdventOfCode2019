#advent of code day 1
#Patrick Johnson 2019
#read csv into array of numbers
#process numbers into required fuel (floor(Mass / 3) - 2)
#sum required fuel
import csv
import math

def calcFuel(mass):
	return math.floor(mass/3)-2
	
#part two!
#calculate the fuel required to carry the fuel (recursion)
def fuelRequired(mass):
	Fuel = calcFuel(mass)
	reqFuel = 0
	while Fuel > 0:
		reqFuel = reqFuel + Fuel
		Fuel = calcFuel(Fuel)

	return reqFuel

mass = []

csvfile = open('input.txt', newline='')
csvreader = csv.reader(csvfile, delimiter=' ')
for row in csvreader:
	mass.append(int(row[0]))
	

#input file has been read

fuel = []
for i in range(len(mass)):
	fuel.append(fuelRequired(mass[i]))
	
#fuel required has been computed

sum = 0

for i in range(len(fuel)):
	sum = sum + fuel[i]
	
print(sum)


print(fuelRequired(1969))
