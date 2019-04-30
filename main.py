import pygame
import random
import sys

class Game:
	CANVAS_WIDTH = 1000
	CANVAS_HEIGHT = 600
	def __init__(self):
		super(Game, self).__init__()
		pygame.init()
		self.screen = pygame.display.set_mode((self.CANVAS_WIDTH,self.CANVAS_HEIGHT))
		self.m = Map(40,40)
		self.gameLoop()

	def gameLoop(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()			

			self.m.draw(self.screen)

			pygame.display.flip()
class Map(object):

	wallGrid = []

	def __init__(self, sX,sY):
		super(Map, self).__init__()
		self.sizeX = sX
		self.sizeY = sY
		self.generateMap()

		self.tileSize = 32
	def generateMap(self):
		for y in range(self.sizeY):
			row = []
			for x in range(self.sizeX):
				val = int(random.random() > 0.8)
				row.append(val)
			self.wallGrid.append(row)
		print(self.wallGrid)

	def tileAt(self,x,y):
		if self.wallGrid[y][x] == 1:
			return 1
		return 0
	def draw(self,cvs,mapPos=[0,0]):
		for y in range(len(self.wallGrid)):
			for x in range(len(self.wallGrid[0])):
				if self.tileAt(x,y) == 1:
					tilePosX = Game.CANVAS_WIDTH/2-mapPos[0]+x*self.tileSize
					tilePosY = Game.CANVAS_HEIGHT/2-mapPos[1]+y*self.tileSize
					
					pygame.draw.rect(cvs,(0,0,255),(tilePosX,tilePosY,self.tileSize,self.tileSize))




			

game = Game()



