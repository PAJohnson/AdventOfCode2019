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
	
	def getNPars(self,n):
		params = []
		parmode = []
		for i in range(n):
			parmode.append(getDigit(self.mem[self.ip],i+2))
			if(parmode[i] == 1):
				#immediate
				params.append(self.mem[self.ip+1+i])
			elif(parmode[i] == 0):
				#position
				try:
					if n > 1 and i == n-1:
						params.append(self.mem[self.ip+1+i])
					else:
						params.append(self.mem[self.mem[self.ip+1+i]])
				except KeyError:
					#expand dictionary
					#smaller dict attempt
					self.mem.update({self.mem[self.ip+1+i] : 0})
					if n > 1 and i == n-1:
						params.append(self.mem[self.ip+1+i])
					else:
						params.append(self.mem[self.mem[self.ip+1+i]])
			elif(parmode[i] == 2):
				#relative
				try:
					if n > 1 and i == n-1:
						params.append(self.mem[self.ip+1+i]+self.relBase)
					else:
						params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				except KeyError:
					#expand dictionary
					self.mem.update({self.mem[self.ip+1+i]+self.relBase : 0})
					if n > 1 and i == n-1:
						params.append(self.mem[self.ip+1+i]+self.relBase)
					else:
						params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				
		return params
		
	def computer(self):
		while self.ip < len(self.mem) and self.halt == 0:
			if getDigit(self.mem[self.ip],0) == 1:
				#add
				#print("at position: " + str(self.ip))
				params = self.getNPars(3)
				print(str(self.ip) + "op = add " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				if getDigit(self.mem[self.ip],4) == 2:
					self.mem[self.mem[self.ip+3]+self.relBase] = params[0] + params[1]
					#print("comp: " + str(self.mem[self.ip+3]+self.relBase) + " " + str(params[2]))
				else:
					self.mem[self.mem[self.ip+3]] = params[0] + params[1]
					#print("comp: " + str(self.mem[self.ip+3]) + " " + str(params[2]))
				#print('adding!')
				self.ip += 4
				
			elif getDigit(self.mem[self.ip],0) == 2:
				#1 op, 3 params
				#multiply
				#print("at position: " + str(self.ip))
				params = self.getNPars(3)
				print(str(self.ip) + "op = mult " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
				if getDigit(self.mem[self.ip],4) == 2:
					self.mem[self.mem[self.ip+3]+self.relBase] = params[0] * params[1]
				else:
					self.mem[self.mem[self.ip+3]] = params[0] * params[1]
				#print('multiplying!')
				self.ip = self.ip + 4
				
			elif getDigit(self.mem[self.ip],0) == 3:
				#prompt for input, store
				#print("Input: " + str(inList[inPtr]))
				params = self.getNPars(1)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = input " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
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
				params = self.getNPars(1)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = output " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				self.output.append(params[0])
				self.ip = self.ip + 2
				
			elif getDigit(self.mem[self.ip],0) == 5:
				#jump if true
				#if first param is non-zero, set ip to value of param 2
				params = self.getNPars(2)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = jumpTrue " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
				if params[0] != 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 6:
				#jump if false
				#if the first param is zero, set ip to value of param 2
				params = self.getNPars(2)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = jumpFalse " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
				if params[0] == 0:
					self.ip = params[1]
				else:
					self.ip += 3
				
			elif getDigit(self.mem[self.ip],0) == 7:
				#less than
				#if 1st param is less than 2nd param, store 1 in position
				#given by 3rd param
				params = self.getNPars(3)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = lessThan? " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
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
				params = self.getNPars(3)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = equals? " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
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
				params = self.getNPars(1)
				#print("at position: " + str(self.ip))
				print(str(self.ip) + "op = relBase " + str(self.mem[self.ip]) + " " + str(params) + " " + str(self.relBase))
				
				self.relBase += params[0]
				
				#print(self.relBase)
				
				self.ip += 2
				
			else:
				#error
				self.halt = 1
				
			#print("at position: " + str(self.ip))
			#print(self.mem.values())




program = arrayParse('test1.txt')
#print(program)
comp = intCodeComp(program)
comp.setInput([1])
#print(comp.mem)
comp.computer()
print(comp.getOutput())
