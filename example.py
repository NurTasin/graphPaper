from graphPaper import *
#Ploting the graph of y=x^2+3x-1
virtualGraph=GraphPaper(700, 1300, "x^2+3x-1")
virtualGraph.setPixelUnit(10,10)
for x in range(-12,5):
	virtualGraph.mark(x, float(pow(x,2)+(8*x)-1))

virtualGraph.joinDots()
try:
	virtualGraph.waitUntilClick()
	virtualGraph.close()
except GraphicsError:
	pass
