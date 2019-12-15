#Patrick Johnson
#advent of code 2019 day 13

import os

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
		self.pause = False
		
	def setInput(self,inList):
		self.pause = False
		self.input = inList
		
	def getOutput(self):
		outL = self.output.copy()
		self.output = []
		return outL
		
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
				self.pause = True
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
		while self.ip < len(self.mem) and self.halt == 0 and self.pause == False:
			self.step()


def getColor(colorDict,coord):
	#0 is black
	#1 is white
	color = 0
	try:
		color = colorDict[tuple(coord)][0]
		return color
	except KeyError:
		colorDict.update({tuple(coord):[0,0]})
		color = 0
		return color

	
def setColor(colorDict,coord,color):
	#colorDict[coord][1] is 0 if not painted
	#otherwise, it is incremented by 1 each time it gets painted
	try:
		colorDict[tuple(coord)][0] = color
		colorDict[tuple(coord)][1] += 1
	except KeyError:
		colorDict.update({tuple(coord):[0,0]})
		colorDict[tuple(coord)][0] = color
		colorDict[tuple(coord)][1] += 1


def dictToGrid(colorDict):
	#get x and y dimensions
	xmin = 0
	xmax = 0
	ymin = 0
	ymax = 0
	xl = []
	yl = []
	for key,val in colorDict.items():
		xl.append(key[0])
		yl.append(key[1])
	xmin = min(xl)
	xmax = max(xl)
	ymin = min(yl)
	ymax = max(yl)
	xspan = xmax-xmin+1
	yspan = ymax-ymin+1
	grid = [['_' for x in range(xspan)] for y in range(yspan)]
	for key,val in colorDict.items():
		#paint grid
		#change to '#'
		xc = key[0]-xmin
		yc = key[1]-ymin
		#print("coord = " + str(xc) + ',' + str(yc))
		if val[0] == 3:
			paddleCoord = [xc,yc]
		if val[0] == 4:
			ballCoord = [xc,yc]
		if val[0] > 0:
			grid[yc][xc] = '#'
		elif val[0] == 0:
			grid[yc][xc] = ' '
		
			
	#print(grid)
	for i in range(len(grid)):
		print(''.join(grid[len(grid)-i-1]))
	return ballCoord[0]-paddleCoord[0]
	
def getInput(inpt):
	inp = input()
	inp.strip()
	if not inp:
		return inpt
	else:
		inp = inp[0]
		if inp == 'a':
			return -1
		elif inp == 'd':
			return 1
		elif inp == 's':
			return 0
		else:
			return 'z'
	
def part1():
	program = arrayParse('input.txt')
	comp = intCodeComp(program)
	colorDict = {}

	comp.computer()
		
	outp = comp.getOutput()

	for i in range(int(len(outp)/3)):
		setColor(colorDict,(outp[i*3],outp[i*3+1]),outp[i*3+2])
		
	#dictToGrid(colorDict)
	numBlock = 0
	for key,val in colorDict.items():
		#sum # of block tiles
		if val[0] == 2:
			numBlock += 1
			
	print("num blocks: " + str(numBlock))
	print(numBlock*55)

part1()

program = arrayParse('input.txt')
program[0] = 2
comp = intCodeComp(program)
colorDict = {}
seg = 0
segOld = seg
segList = []
run = True
inp = 0
while run == True:
	comp.computer()
	outp = comp.getOutput()
	for i in range(int(len(outp)/3)):
		if outp[i*3] == -1 and outp[i*3+1] == 0:
			seg = outp[i*3+2]
		else:
			setColor(colorDict,(outp[i*3],outp[i*3+1]),outp[i*3+2])
	#move based on diff between x coord of ball and paddle
	inp = dictToGrid(colorDict)
	if seg-segOld != 0:
		segList.append(seg-segOld)
	segOld = seg
	print("seg = " + str(seg))
	print("segL = " + str(segList))
	comp.setInput([inp])
