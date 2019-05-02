def lerp(prevVal,newVal,amnt):
	difference = (newVal-prevVal)
	add = difference*amnt
	return prevVal+add

class Point:
	def __init__ (self,x,y):
		self.x = x
		self.y = y
	def int(self):
		return int(self.x),int(self.y)

class Rect:
	def __init__ (x1,y1,x2,y2):
		self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2