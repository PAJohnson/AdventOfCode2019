#patrick Johnson 2019
#advent of code day 4
#seems pretty simple...

def hasDouble(number):
	numberString = str(number)
	hasDbl = 0
	for i in range(5):
		if(numberString[i] == numberString[i+1]):
			hasDbl = 1
	return hasDbl
	
def findRepeat(number):
	#find the smallest number of repeating digits
	#in the number starting from the beginning
	#122222 = 1, because 1 does not match 2
	#112222 = 2, because 1 matches 1
	#211222 = 1, because 2 does not match 1
	groupSize = 1
	i = 1
	numString = str(number)
	while i < len(numString) and numString[0] == numString[i]:
		groupSize += 1
		i += 1
	return groupSize
	
def minGroupSize(number):
	numString = str(number)
	minGroupSize = 0
	groupSize = 0
	groupList = []
	i = 0
	#want to find all groups of numbers
	#calculate lengths of groups, append to list
	#find min of groupList, return
	
	#loop through digits 0-9, if next num matches increment
	while(i < 6):
		size = findRepeat(numString[i:])
		i = i + size
		if size >= 2:
			groupList.append(size)
			
		
	return min(groupList)
	
def increasing(number):
	numberString = str(number)
	inc = 1
	for i in range(5):
		if(numberString[i] > numberString[i+1]):
			inc = 0
	return inc
	
def partOne():
	numList = []
	for i in range(893698-367479):
		numList.append(i+367479)
		
	solutions = 0
	for num in numList:
		if(hasDouble(num) and increasing(num)):
			solutions +=1
			print("solution! " + str(num))

	print(solutions)

#puzzle input is 367479 to 893698

def partTwo():
	numList = []
	for i in range(893698-367479):
		numList.append(i+367479)
		
	solutions = 0
	for num in numList:
		if(hasDouble(num) and increasing(num) and minGroupSize(num)==2):
			solutions +=1
			print("solution! " + str(num))

	print(solutions)
	
partTwo()
