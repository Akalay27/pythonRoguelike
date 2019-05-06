import pygame
import random
import sys
from map import *
from util import *

		
class Game:
	CANVAS_WIDTH = 1000
	CANVAS_HEIGHT = 600

	tileSize = 32

	def __init__(self):
		
		pygame.init()

		self.screen = pygame.display.set_mode((self.CANVAS_WIDTH,self.CANVAS_HEIGHT),pygame.DOUBLEBUF | pygame.HWSURFACE)
		
		self.player = Player(0,0)

		self.map = Map()
		self.map.loadRooms("rooms.txt")
		self.map.generateMap()
		self.map.printMap()
		
		self.player.pos.x = (self.map.rooms[0].bbox.x2-self.map.rooms[0].bbox.x1)/2*self.tileSize+self.tileSize*0.5
		self.player.pos.y = (self.map.rooms[0].bbox.y2-self.map.rooms[0].bbox.y1)/2*self.tileSize+self.tileSize*0.5
		
		self.cameraPos = Point(0,0)


		self.gameLoop()


	def gameLoop(self):
		while 1:

			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()			

			self.drawMap()
			self.cameraPos.x,self.cameraPos.y = self.player.pos.x,self.player.pos.y
			#self.cameraPos.x,self.cameraPos.y = lerp(self.cameraPos.x,self.player.pos.x,0.01), lerp(self.cameraPos.y,self.player.pos.y,0.01)
			self.player.draw(self)
			self.player.move(self)
			#self.map.generateMap()
			#put player in center of start room

			
			pygame.display.flip()


	def getCameraPoint(self,point):
		return Point(self.CANVAS_WIDTH/2+point.x-int(self.cameraPos.x), self.CANVAS_HEIGHT/2+point.y-int(self.cameraPos.y)).int()
	def drawMap(self):
		tileRangeY = math.ceil(self.CANVAS_HEIGHT/self.tileSize/2)+1
		tileRangeX = math.ceil(self.CANVAS_WIDTH/self.tileSize/2)+1
		cameraTilePos = Point(int(self.cameraPos.x/self.tileSize), int(self.cameraPos.y/self.tileSize))
		
		
		for y in range(cameraTilePos.y-tileRangeY,cameraTilePos.y+tileRangeY):
			for x in range(cameraTilePos.x-tileRangeX,cameraTilePos.x+tileRangeX):
				drawPos = self.getCameraPoint(Point(x*self.tileSize,y*self.tileSize))
				if self.map.tileAt(x, y).type == Map.Tile.WALL:
					pygame.draw.rect(self.screen,(0,0,255),(drawPos[0],drawPos[1],self.tileSize,self.tileSize))
				elif self.map.tileAt(x, y).type == Map.Tile.FLOOR:
					pygame.draw.rect(self.screen,(0,0,100),(drawPos[0],drawPos[1],self.tileSize,self.tileSize))
				elif self.map.tileAt(x, y).type == Map.Tile.DOOR:
					pygame.draw.rect(self.screen,(100,0,100),(drawPos[0],drawPos[1],self.tileSize,self.tileSize))
class Player:
	
	def __init__(self, x, y):
		self.pos = Point(x,y)
		self.moveSpeed = 10
		self.direction = 0


	
	def draw(self,game):
		drawPos = game.getCameraPoint(self.pos)
		pygame.draw.circle(game.screen,(255,0,0),drawPos,5)

	def move(self,game):
	
		pressedKeys = pygame.key.get_pressed()

		newPos = Point(self.pos.x,self.pos.y)
		if pressedKeys[pygame.K_w]:
			newPos.y-= self.moveSpeed
		if pressedKeys[pygame.K_s]:
			newPos.y+= self.moveSpeed
		if pressedKeys[pygame.K_a]:
			newPos.x-= self.moveSpeed
		if pressedKeys[pygame.K_d]:
			newPos.x+= self.moveSpeed

		tile = Point(newPos.x//game.tileSize, newPos.y//game.tileSize).int()
		print(tile)
		if game.map.tileAt(tile[0],tile[1]).type != 1:
			self.pos = newPos


game = Game()




