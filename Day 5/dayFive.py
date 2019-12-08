#Patrick Johnson
#advent of code day 5

def arrayParse(fileName):
	data = []

	f = open(fileName)
	fstring = f.read()
	data = list(map(int,fstring.split(',')))
	f.close()
	return data

#from stack overflow
def getDigit(number, place):
	return number // 10**place % 10

def computer(memory,inList):
	#mem is a list of instructions
	#this function runs through each instruction
	#add new instructions to the if/elif tree
	#now need to handle immediate and position modes!
	mem = memory.copy()
	ip = 0
	halt = 0
	inPtr = 0
	out = 0
	while ip < len(mem) and halt == 0:
		#print("at position: " + str(ip))
		#1 op, 3 params
		#interpretation
		if getDigit(mem[ip],0) == 1:
			#add
			parNum = 3
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
			
			mem[mem[ip+3]] = params[0] + params[1]
			#print('adding!')
			ip = ip + 4
			
		elif getDigit(mem[ip],0) == 2:
			#1 op, 3 params
			#multiply
			parNum = 3
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
			
			mem[mem[ip+3]] = params[0] * params[1]
			#print('multiplying!')
			ip = ip + 4
			
		elif getDigit(mem[ip],0) == 3:
			#prompt for input, store
			print("Input: ")
			val = inList[inPtr]
			inPtr += 1
			mem[mem[ip+1]] = val
			ip = ip + 2
			
		elif getDigit(mem[ip],0) == 4:
			#outputs value of parameter
			print(mem[mem[ip+1]])
			out = mem[mem[ip+1]]
			ip = ip + 2
			
		elif getDigit(mem[ip],0) == 5:
			#jump if true
			#if first param is non-zero, set ip to value of param 2
			parNum = 2
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
					
			if params[0] != 0:
				ip = params[1]
			else:
				ip += 3
			
		elif getDigit(mem[ip],0) == 6:
			#jump if false
			#if the first param is zero, set ip to value of param 2
			parNum = 2
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
					
			if params[0] == 0:
				ip = params[1]
			else:
				ip += 3
			
		elif getDigit(mem[ip],0) == 7:
			#less than
			#if 1st param is less than 2nd param, store 1 in position
			#given by 3rd param
			parNum = 3
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
					
			if params[0] < params[1]:
				mem[mem[ip+3]] = 1
			else:
				mem[mem[ip+3]] = 0
			ip += 4
			
		elif getDigit(mem[ip],0) == 8:
			#equals
			#if 1st param == 2nd param, store 1 in position given
			#by 3rd param
			parNum = 3
			params = []
			parmode = []
			for i in range(parNum):
				parmode.append(getDigit(mem[ip],i+2))
				if(parmode[i] == 1):
					params.append(mem[ip+1+i])
				elif(parmode[i] == 0):
					params.append(mem[mem[ip+1+i]])
			if params[0] == params[1]:
				mem[mem[ip+3]] = 1
			else:
				mem[mem[ip+3]] = 0
			ip += 4		
					
		elif mem[ip] == 99:
			#halt
			halt = 1
			print('halting!')
			index = ip + 1
		else:
			#error
			halt = 1
			print('unrecognized opcode')
		
		
		#print(index)
	
	return mem


#print(getDigit(3,1))
program = arrayParse('input.txt')
#program = [3,3,1107,-1,8,3,4,3,99]
mem = computer(program)
