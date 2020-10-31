import pygame
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
	def __str__(self):
		return "({},{})".format(self.x, self.y)
class Rect:

	def __init__ (self,x1,y1,x2,y2):
		self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
	def __str__ (self):
		return "Rect ({}, {}) to ({}, {})".format(self.x1,self.y1,self.x2,self.y2)

	def insideOf(self,x,y):
		'''returns true if point is inside of Rect'''
		return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

	def collidesWithRect(self,rect):
		if (self.x2 >= rect.x1 and self.x1 <= rect.x2 and self.y2 >= rect.y1 and self.y1 <= rect.y2):
			return True
		return False

def manhattanDistance(p1,p2):
	return abs(p1.x-p2.x)+abs(p1.y-p2.y)

def sliceTilemap(img,size,scaleSize=None):
	'''turns tilemap into array of pygame.Surface'''
	frames = []

	for y in range(0,img.get_height(),size[1]):
		for x in range(0,img.get_width(),size[0]):
			if scaleSize != None:
				frames.append(pygame.transform.scale(img.subsurface((x,y,size[0],size[1])),(scaleSize)))
	return frames

