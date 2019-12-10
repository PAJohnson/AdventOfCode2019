#Patrick Johnson
#advent of code day 9 2019

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

	def getParams(self,n):
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
					params.append(self.mem[self.mem[self.ip+1+i]])
				except KeyError:
					self.mem.update({self.mem[self.ip+1+i] : 0})
					params.append(self.mem[self.mem[self.ip+1+i]])
			elif(parmode[i] == 2):
				#relative
				try:
					params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				except KeyError:
					self.mem.update({self.mem[self.ip+1+i]+self.relBase : 0})
					params.append(self.mem[self.mem[self.ip+1+i]+self.relBase])
				
		return params
	
	def step(self):
		#runs 1 instruction
		if getDigit(self.mem[self.ip],0) == 1:
			#add
			params = self.getParams(3)
			if getDigit(self.mem[self.ip],4) == 2:
				self.mem[self.mem[self.ip+3]+self.relBase] = params[0] + params[1]
			else:
				self.mem[self.mem[self.ip+3]] = params[0] + params[1]
			self.ip += 4
			
		elif getDigit(self.mem[self.ip],0) == 2:
			#multiply
			params = self.getParams(3)
			
			if getDigit(self.mem[self.ip],4) == 2:
				self.mem[self.mem[self.ip+3]+self.relBase] = params[0] * params[1]
			else:
				self.mem[self.mem[self.ip+3]] = params[0] * params[1]
			self.ip = self.ip + 4
			
		elif getDigit(self.mem[self.ip],0) == 3:
			#prompt for input, store
			params = self.getParams(1)
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
			params = self.getParams(1)
			self.output.append(params[0])
			self.ip = self.ip + 2
			
		elif getDigit(self.mem[self.ip],0) == 5:
			#jump if true
			#if first param is non-zero, set ip to value of param 2
			params = self.getParams(2)	
			if params[0] != 0:
				self.ip = params[1]
			else:
				self.ip += 3
			
		elif getDigit(self.mem[self.ip],0) == 6:
			#jump if false
			#if the first param is zero, set ip to value of param 2
			params = self.getParams(2)
			if params[0] == 0:
				self.ip = params[1]
			else:
				self.ip += 3
			
		elif getDigit(self.mem[self.ip],0) == 7:
			#less than
			#if 1st param is less than 2nd param, store 1 in position
			#given by 3rd param
			params = self.getParams(3)
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
			params = self.getParams(3)
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
			self.halt = True
			self.ip += 1
			
		elif getDigit(self.mem[self.ip],0) == 9:
			#modify relative base
			params = self.getParams(1)
			self.relBase += params[0]
			self.ip += 2
			
		else:
			#error
			self.halt = 1	
		
	def computer(self):
		while self.ip < len(self.mem) and self.halt == 0:
			self.step()





program = arrayParse('input.txt')
#print(program)
comp = intCodeComp(program)
comp.setInput([2])
#print(comp.mem)
comp.computer()
print(comp.getOutput())
