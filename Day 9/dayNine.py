#Patrick Johnson
#advent of code day 9 2019

#need to add "relative mode" for parameters
#computer memory space needs to be quite large!
#the graceful way to do this would be to append to the memory when needed...
#or, use a dict instead of a list for the "tape"!


def arrayParse(fileName):
	data = []

	f = open(fileName)
	fstring = f.read()
	data = list(map(int,fstring.split(',')))
	f.close()
	return data
	
def getDigit(number, place):
	return number // 10**place % 10

class intCodeComp:
	def __init__(self,mem):
		#self.mem = mem.copy()
		self.mem = {}
		for i in range(len(mem)):
			self.mem[i] = mem[i]
		self.output = []
		self.input = []
		self.halt = False
		self.inPtr = 0
		self.ip = 0
		self.relBase = 0
		
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
	
	def getNPars(self,n):
		params = []
		parmode = []
		#print("getNPars called n = " + str(n) + " , ip = " + str(self.ip))
		for i in range(n):
			parmode.append(getDigit(self.mem[self.ip],i+2))
			if(parmode[i] == 1):
				#immediate
				params.append(self.mem[self.ip+1+i])
			elif(parmode[i] == 0):
				#position
				#print(self.ip+1+i)
				#print(self.mem[self.ip+1+i])
				#print(self.mem[self.mem[self.ip+1+i]])
				try:
					params.append(self.mem[self.mem[self.ip+1+i]])
				except KeyError:
					#expand dictionary
					ogLen = len(self.mem)
					for j in range(self.mem[self.ip+1+i]-len(self.mem)+1):
						self.mem.update({ogLen+j : 0})
					#print(len(self.mem))
					params.append(self.mem[self.mem[self.ip+1+i]])
			elif(parmode[i] == 2):
				#relative
				#print("relative mode: " + str(self.mem[self.ip+1+i]) + " + " + str(self.relBase) + " = " + str(self.mem[self.mem[self.ip+1+i]+self.relBase]))
				try:
					params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				except KeyError:
					#expand dictionary
					ogLen = len(self.mem)
					for j in range(self.mem[self.ip+1+i]+self.relBase-len(self.mem)+1):
						self.mem.update({ogLen+j : 0})
					#print(len(self.mem))
					params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				
		return params
	
	def getParams(self):
		#figure out parameter mode, return parameters
		params = []
		
		if getDigit(self.mem[self.ip],0) == 1:
			#add, par = 3
			params = self.getNPars(3)
			
		elif getDigit(self.mem[self.ip],0) == 2:
			#multiply, par = 3
			params = self.getNPars(3)
			
		elif getDigit(self.mem[self.ip],0) == 3:
			#prompt for input
			#no need for anything here
			params = self.getNPars(1)
			
		elif getDigit(self.mem[self.ip],0) == 4:
			#only output
			params = self.getNPars(1)
			
		elif getDigit(self.mem[self.ip],0) == 5:
			#jump if true
			#par = 2
			params = self.getNPars(2)
			
		elif getDigit(self.mem[self.ip],0) == 6:
			#jump if false
			#par = 2
			params = self.getNPars(2)
		
		elif getDigit(self.mem[self.ip],0) == 7:
			#less than
			#par = 3
			params = self.getNPars(3)
			
		elif getDigit(self.mem[self.ip],0) == 8:
			#equals
			#par = 3
			params = self.getNPars(3)
			
		elif getDigit(self.mem[self.ip],0) == 9:
			#relative base change
			params = self.getNPars(1)
	
		return params
		
	def computer(self):
		#mem is a list of instructions
		#this function runs through each instruction
		#add new instructions to the if/elif tree
		#now need to handle immediate and position modes!
		while self.ip < len(self.mem) and self.halt == 0:
			#1 op, 3 params
			#interpretation
			
			if getDigit(self.mem[self.ip],0) == 1:
				#add
				#print("at position: " + str(self.ip))
				#print("op = add " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				params = self.getParams()
				if getDigit(self.mem[self.ip],4) == 2:
					self.mem[self.mem[self.ip+3]+self.relBase] = params[0] + params[1]
				else:
					self.mem[self.mem[self.ip+3]] = params[0] + params[1]
				#print('adding!')
				self.ip += 4
				
			elif getDigit(self.mem[self.ip],0) == 2:
				#1 op, 3 params
				#multiply
				#print("at position: " + str(self.ip))
				#print("op = mult " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				params = self.getParams()
				
				if getDigit(self.mem[self.ip],4) == 2:
					self.mem[self.mem[self.ip+3]+self.relBase] = params[0] * params[1]
				else:
					self.mem[self.mem[self.ip+3]] = params[0] * params[1]
				#print('multiplying!')
				self.ip = self.ip + 4
				
			elif getDigit(self.mem[self.ip],0) == 3:
				#prompt for input, store
				#print("Input: " + str(inList[inPtr]))
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = input " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				if not self.input:
					return
				elif getDigit(self.mem[self.ip],2) == 2:
					self.mem[self.mem[self.ip+1]+self.relBase] = self.input[0]
					self.input = []
					self.ip = self.ip + 2
				else:
					self.mem[self.mem[self.ip+1]] = self.input[0]
					self.input = []
					self.ip = self.ip + 2
				
			elif getDigit(self.mem[self.ip],0) == 4:
				#outputs value of parameter
				#print(mem[mem[ip+1]])
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = output " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				#print(params)
				self.output.append(params[0])
				self.ip = self.ip + 2
				
			elif getDigit(self.mem[self.ip],0) == 5:
				#jump if true
				#if first param is non-zero, set ip to value of param 2
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = jumpTrue " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				
				if params[0] != 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 6:
				#jump if false
				#if the first param is zero, set ip to value of param 2
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = jumpFalse " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				
				if params[0] == 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 7:
				#less than
				#if 1st param is less than 2nd param, store 1 in position
				#given by 3rd param
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = lessThan? " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				
				if getDigit(self.mem[self.ip],4) == 2:
					if params[0] < params[1]:
						self.mem[self.mem[self.ip+3]+self.relBase] = 1
					else:
						self.mem[self.mem[self.ip+3]+self.relBase] = 0
				else:
					if params[0] < params[1]:
						self.mem[self.mem[self.ip+3]] = 1
					else:
						self.mem[self.mem[self.ip+3]] = 0
				self.ip += 4
				
			elif getDigit(self.mem[self.ip],0) == 8:
				#equals
				#if 1st param == 2nd param, store 1 in position given
				#by 3rd param
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = equals? " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				
				#print("eq, params: " + str(params))
				if getDigit(self.mem[self.ip],4) == 2:
					if params[0] == params[1]:
						self.mem[self.mem[self.ip+3]+self.relBase] = 1
					else:
						self.mem[self.mem[self.ip+3]+self.relBase] = 0
				else:
					if params[0] == params[1]:
						self.mem[self.mem[self.ip+3]] = 1
					else:
						self.mem[self.mem[self.ip+3]] = 0
				self.ip += 4		
				
			elif self.mem[self.ip] == 99:
				#halt
				#print("at position: " + str(self.ip))
				#print("op = halt " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				self.halt = True
				#print('halting!')
				self.ip += 1
				
			elif getDigit(self.mem[self.ip],0) == 9:
				#modify relative base
				params = self.getParams()
				#print("at position: " + str(self.ip))
				#print("op = relBase " + str(self.mem[self.ip]) + " " + str(self.getParams()) + " " + str(self.relBase))
				
				self.relBase += params[0]
				
				#print(self.relBase)
				
				self.ip += 2
				
			else:
				#error
				self.halt = 1
				
			#print("at position: " + str(self.ip))
			#print(self.mem.values())




program = arrayParse('input.txt')
#print(program)
comp = intCodeComp(program)
comp.setInput([2])
#print(comp.mem)
comp.computer()
print(comp.getOutput())
