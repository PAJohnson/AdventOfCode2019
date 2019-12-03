#advent of code day 2
#Patrick Johnson 2019
#simple assembler! cool!

import csv

#might be handy to have a function that parses a list of numbers
#and returns an array
def arrayParse(fileName):
	data = []

	f = open(fileName)
	fstring = f.read()
	data = list(map(int,fstring.split(',')))
	f.close()
	return data

def opInterpret(opcodes):
	#opcodes is a list of instructions
	#this function runs through each instruction
	newOps = opcodes.copy()
	index = 0
	halt = 0
	while index < len(newOps) and halt == 0:
		#interpretation
		if newOps[index] == 1:
			#add
			newOps[newOps[index+3]] = newOps[newOps[index+1]] + newOps[newOps[index+2]]
			#('adding!')
		elif newOps[index] == 2:
			#multiply
			newOps[newOps[index+3]] = newOps[newOps[index+1]] * newOps[newOps[index+2]]
			#print('multiplying!')
		elif newOps[index] == 99:
			#halt
			halt = 1
			#print('halting!')
		else:
			#error
			halt = 1
			#print('unrecognized opcode')
		
		index = index + 4
		#print(index)
	
	return newOps
	
def findNV(opcodes,key):
	noun = 0
	verb = 0
	newOps = opcodes.copy()
	result = 0
	for noun in range(99):
		for verb in range(99):
			newOps = opcodes.copy()
			newOps[1] = noun
			newOps[2] = verb
			result = opInterpret(newOps)
			if result[0] == key:
				print('Found!')
				answer = 100*noun + verb
			
	return answer
		
	

opcodes = arrayParse('input.txt')
#do some testing
#do the replacement as described in problem
opcodes[1] = 12
opcodes[2] = 2
result = opInterpret(opcodes)
print(result[0])

#part 2!
#find the inputs for opcodes[1] and opcodes[2] that causes
#opcodes[0] to equal 19690720
key = 19690720
print(findNV(arrayParse('input.txt'),key))
