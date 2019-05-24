from Entity import entity
from util import *
class Enemy(Entity):
	"""docstring for Enemy"""
	def __init__(self, x, y, health, damage):
	
		super(Enemy, self).__init__()

		self.pos = Point(x, y)
		self.damage = damage
		self.health = health










