#day 7 advent of code
#Patrick Johnson

from itertools import permutations 

haltList = []

class Signal:
	def __init__(self):
		self.signal = None
		self.set = False
		
	def get(self):
		self.set = False
		return self.signal
		
	def set(self,signal):
		self.signal = signal
		self.set = True
		
	def isSet(self):
		return self.set

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
	
class intCodeComp:
	def __init__(self,mem):
		self.mem = mem.copy()
		self.output = 0
		self.input = []
		self.halt = False
		self.inPtr = 0
		self.ip = 0
		
	def setInput(self,inList):
		self.input = inList
		
	def getOutput(self):
		return self.output
		
	def isHalted(self):
		return self.halt
	#do we need callbacks for the signal?
	#how to make compute pause when input is called
	#if items remain in inList, execute input instructions
	#else, if not inList, return.
	
	def computer(self):
		#mem is a list of instructions
		#this function runs through each instruction
		#add new instructions to the if/elif tree
		#now need to handle immediate and position modes!
		while self.ip < len(self.mem) and self.halt == 0:
			#print("at position: " + str(ip))
			#1 op, 3 params
			#interpretation
			if getDigit(self.mem[self.ip],0) == 1:
				#add
				parNum = 3
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
				
				self.mem[self.mem[self.ip+3]] = params[0] + params[1]
				#print('adding!')
				self.ip += 4
				
			elif getDigit(self.mem[self.ip],0) == 2:
				#1 op, 3 params
				#multiply
				parNum = 3
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
				
				self.mem[self.mem[self.ip+3]] = params[0] * params[1]
				#print('multiplying!')
				self.ip = self.ip + 4
				
			elif getDigit(self.mem[self.ip],0) == 3:
				#prompt for input, store
				#print("Input: " + str(inList[inPtr]))
				if not self.input:
					return
				else:
					self.mem[self.mem[self.ip+1]] = self.input[0]
					self.input = []
					self.ip = self.ip + 2
				
			elif getDigit(self.mem[self.ip],0) == 4:
				#outputs value of parameter
				#print(mem[mem[ip+1]])
				self.output = self.mem[self.mem[self.ip+1]]
				self.ip = self.ip + 2
				
			elif getDigit(self.mem[self.ip],0) == 5:
				#jump if true
				#if first param is non-zero, set ip to value of param 2
				parNum = 2
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
						
				if params[0] != 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 6:
				#jump if false
				#if the first param is zero, set ip to value of param 2
				parNum = 2
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
						
				if params[0] == 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 7:
				#less than
				#if 1st param is less than 2nd param, store 1 in position
				#given by 3rd param
				parNum = 3
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
						
				if params[0] < params[1]:
					self.mem[self.mem[self.ip+3]] = 1
				else:
					self.mem[self.mem[self.ip+3]] = 0
				self.ip += 4
				
			elif getDigit(self.mem[self.ip],0) == 8:
				#equals
				#if 1st param == 2nd param, store 1 in position given
				#by 3rd param
				parNum = 3
				params = []
				parmode = []
				for i in range(parNum):
					parmode.append(getDigit(self.mem[self.ip],i+2))
					if(parmode[i] == 1):
						params.append(self.mem[self.ip+1+i])
					elif(parmode[i] == 0):
						params.append(self.mem[self.mem[self.ip+1+i]])
				if params[0] == params[1]:
					self.mem[self.mem[self.ip+3]] = 1
				else:
					self.mem[self.mem[self.ip+3]] = 0
				self.ip += 4		
						
			elif self.mem[self.ip] == 99:
				#halt
				self.halt = True
				#print('halting!')
				self.ip += 1
			else:
				#error
				self.halt = 1
				#print('unrecognized opcode')
			


def computer(memory,inList):
	#mem is a list of instructions
	#this function runs through each instruction
	#add new instructions to the if/elif tree
	#now need to handle immediate and position modes!
	global haltList
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
			#print("Input: " + str(inList[inPtr]))
			val = inList[inPtr]
			inPtr += 1
			mem[mem[ip+1]] = val
			ip = ip + 2
			
		elif getDigit(mem[ip],0) == 4:
			#outputs value of parameter
			#print(mem[mem[ip+1]])
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
			#print('halting!')
			haltList.append(1)
			index = ip + 1
		else:
			#error
			halt = 1
			#print('unrecognized opcode')
		
		
		#print(index)
	
	return out

def thrustCompute(mem,phase):
	#5 amplifiers
	inL = [getDigit(phase,4),0]
	out = computer(mem,inL)
	#amp 2
	inL = [getDigit(phase,3),out]
	out = computer(mem,inL)
	#amp 3
	inL = [getDigit(phase,2),out]
	out = computer(mem,inL)
	#amp 4
	inL = [getDigit(phase,1),out]
	out = computer(mem,inL)
	#amp 5
	inL = [getDigit(phase,0),out]
	out = computer(mem,inL)
	
	return out
	
def thrustFeedback(mem,phase):
	#create five computers
	compList = [intCodeComp(mem) for i in range(5)]
	#set the inputs for each computer to the phase
	#run the computer with the phase. It should pause there
	for i in range(5):
		print("comp " + str(i) + " phase is " + str(getDigit(phase,4-i)))
		compList[i].setInput([getDigit(phase,4-i)])
		compList[i].computer()
		
	#initial input for computer 0 "a"
	compList[0].setInput([0])
	
	while compList[4].isHalted() is False:
		#run the computer sequence until comp 5 halts.
		compList[0].computer()
		compList[1].setInput([compList[0].getOutput()])
		compList[1].computer()
		compList[2].setInput([compList[1].getOutput()])
		compList[2].computer()
		compList[3].setInput([compList[2].getOutput()])
		compList[3].computer()
		compList[4].setInput([compList[3].getOutput()])
		compList[4].computer()
		compList[0].setInput([compList[4].getOutput()])
		
	return compList[4].getOutput()
	
	
def pListGen():
	perms = permutations([5,6,7,8,9])
	pList = []
	for perm in perms:
		pList.append(perm[0] * 10000 \
						+ perm[1] * 1000 \
						+ perm[2] * 100 \
						+ perm[3] * 10 \
						+ perm[4])
	return pList

def maxThrust(mem,pList):
	out = 0
	outList = []
	for phaseIn in pList:
		outp = thrustCompute(mem,phaseIn)
		print(str(phaseIn) + " : " + str(outp))
		outList.append(outp)
						
	return max(outList)
	
def maxFBThrust(mem,pList):
	out = 0
	outList = []
	for phaseIn in pList:
		outp = thrustFeedback(mem,phaseIn)
		print(str(phaseIn) + " : " + str(outp))
		outList.append(outp)
		
	return max(outList)

#part 1
program = arrayParse('input.txt')
#print(thrustCompute(program,10432))
#print(maxThrust(program,pListGen()))

#part 2
#feedback loop
print(maxFBThrust(program,pListGen()))
