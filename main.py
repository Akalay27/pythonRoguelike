import pygame



class Game:

	CANVAS_WIDTH = 600
	CANVAS_HEIGHT = 600
	screen = pygame.display.set_mode((CANVAS_WIDTH,CANVAS_HEIGHT))
	"""Container for entire game"""
	def __init__(self, arg):
		super(Game, self).__init__()
	

class Map(object):
	def __init__(self, sX,sY):
		super(Map, self).__init__()
		self.sizeX = sX
		self.sizeY = sY


			





