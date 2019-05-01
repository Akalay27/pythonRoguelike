import pygame
import random
import sys

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
		
class Game:
	CANVAS_WIDTH = 1000
	CANVAS_HEIGHT = 600

	def __init__(self):
		
		pygame.init()

		self.screen = pygame.display.set_mode((self.CANVAS_WIDTH,self.CANVAS_HEIGHT))
		self.map = Map(40,40)
		self.cameraPos = Point(0,0)

		self.player = Player(65,65)
		

		self.gameLoop()


	def gameLoop(self):
		while 1:

			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()			

			self.map.draw(self.screen,self.cameraPos)

			self.cameraPos.x,self.cameraPos.y = lerp(self.cameraPos.x,self.player.pos.x,0.01), lerp(self.cameraPos.y,self.player.pos.y,0.01)
			self.player.draw(self.screen,self.cameraPos)
			self.player.move(self.map)
			pygame.display.flip()

class Map:

	wallGrid = []



	def __init__(self, sX,sY):

		self.generateMap(sX,sY)

		self.tileSize = 64
		self.sizeX = len(self.wallGrid[0])
		self.sizeY = len(self.wallGrid)
	def generateMap(self,sx,sy): # generates map with closed walls and random obstacles, temporary before BSP or loading map
		for y in range(sy):
			row = []
			for x in range(sx):
				val = int(random.random() > 0.8 or (x == 0 or x == sx-1 or y == 0 or y == sy-1))
				row.append(val)
			self.wallGrid.append(row)
		print(self.wallGrid)

	def tileAt(self,x,y):
		if self.wallGrid[y][x] == 1:
			return 1
		return 0
	def draw(self,cvs,cameraPos):
		for y in range(len(self.wallGrid)):
			for x in range(len(self.wallGrid[0])):
				if self.tileAt(x,y) == 1:
					tilePosX = Game.CANVAS_WIDTH/2-cameraPos.x+x*self.tileSize
					tilePosY = Game.CANVAS_HEIGHT/2-cameraPos.y+y*self.tileSize
					
					pygame.draw.rect(cvs,(0,0,255),(tilePosX,tilePosY,self.tileSize,self.tileSize))

class Player:
	
	def __init__(self, x, y):
		self.pos = Point(x,y)
		self.moveSpeed = 0.5
		self.direction = 0


	
	def draw(self,cvs,cameraPos):
		drawPos = Point(Game.CANVAS_WIDTH/2+self.pos.x-int(cameraPos.x), Game.CANVAS_HEIGHT/2+self.pos.y-int(cameraPos.y)).int()
		pygame.draw.circle(cvs,(255,0,0),drawPos,5)

	def move(self,m):
	
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

		tile = Point(newPos.x//m.tileSize, newPos.y//m.tileSize).int()
		print(tile)
		if m.tileAt(tile[0],tile[1]) != 1:
			self.pos = newPos


game = Game()




