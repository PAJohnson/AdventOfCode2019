#Patrick Johnson
#Advent of Code day 8 2019

#looks easy - picture deal

def parseImage(filename):
	pixList = []
	end = False
	f = open(filename)
	while not end:
		c = f.read(1)
		if not c:
			end = True
		else:
			if c is not '\n':
				pixList.append(c)
			
	return pixList
	
def createLayers(pixList,width,height):
	layerList = []
	layer = []
	count = 0
	for j in range(len(pixList)):
		layer.append(pixList[j])
		if len(layer) == width*height:
			layerList.append(layer)
			layer = []
		
	return layerList
		
def findDigits(layer,digit):
	count = 0
	for i in range(len(layer)):
		if layer[i] == digit:
			count += 1
			
	return count
	
def render2(layers,w,h):
	#do this differently
	#create many lists
	outp = []
	outvis = [False for i in range(w*h)]
	for i in range(w*h):
		#for every pixel
		pList = []
		outvis = [False for i in range(w*h)]
		for j in range(len(layers)):
			pList.append(layers[j][i])
			#outvis.append(False)
			
		for k in range(len(pList)):
			#print(k)
			#print(i)
			if outvis[i] is False:
				if pList[k] is not '2':
					outp.append(pList[k])
					outvis[i] = True
				
	return outp
				
	
layers = createLayers(parseImage('input.txt'),25,6)
#countZero = []
#for lay in layers:
#	countZero.append(findDigits(lay,'0'))
	
#part 1	
#print(countZero)
#print(min(countZero))
#print(countZero.index(min(countZero)))
print(findDigits(layers[5],'1')*findDigits(layers[5],'2'))

#part 2
rend = render2(layers,25,6)
for i in range(len(rend)):
	if rend[i] == '0':
		rend[i] = '_'
	if rend[i] == '1':
		rend[i] = '#'

#print(rend)

print(''.join(rend[0*25:1*25]))
print(''.join(rend[1*25:2*25]))
print(''.join(rend[2*25:3*25]))
print(''.join(rend[3*25:4*25]))
print(''.join(rend[4*25:5*25]))
print(''.join(rend[5*25:6*25]))

