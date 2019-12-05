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

def computer(memory):
	#mem is a list of instructions
	#this function runs through each instruction
	#add new instructions to the if/elif tree
	mem = memory.copy()
	ip = 0
	halt = 0
	while ip < len(mem) and halt == 0:
		#interpretation
		if mem[ip] == 1:
			#add
			mem[mem[ip+3]] = mem[mem[ip+1]] + mem[mem[ip+2]]
			#('adding!')
			ip = ip + 4
		elif mem[ip] == 2:
			#multiply
			mem[mem[ip+3]] = mem[mem[ip+1]] * mem[mem[ip+2]]
			#print('multiplying!')
			ip = ip + 4
		elif mem[ip] == 99:
			#halt
			halt = 1
			#print('halting!')
			index = ip + 1
		else:
			#error
			halt = 1
			#print('unrecognized opcode')
		
		
		#print(index)
	
	return mem
	
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
			result = computer(newOps)
			if result[0] == key:
				print('Found!')
				answer = 100*noun + verb
			
	return answer
		
	

opcodes = arrayParse('input.txt')
#do some testing
#do the replacement as described in problem
opcodes[1] = 12
opcodes[2] = 2
result = computer(opcodes)
print(result[0])

#part 2!
#find the inputs for opcodes[1] and opcodes[2] that causes
#opcodes[0] to equal 19690720
key = 19690720
print(findNV(arrayParse('input.txt'),key))
