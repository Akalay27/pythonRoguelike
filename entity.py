import math
from map import *
from main import Player


def moveUp(point, game):
 	pos = Point(pos.x, pos.y)
 	pos.y-= movespeed*game.deltaTime

class DumbSearch():
	
	def __init__(self, x, y):
		super(DumbSearch, self).__init__()
		self.pos = Point(x,y)
		self.movespeed = 3
		self.direction = 0

def angle(p, q):
	deltax = p.x - q.x
	deltay = p.y - q.y
	dist = math.sqrt(p.x*p.x+p.y*p.y)
	angle = math.atan2(deltax, deltay)
