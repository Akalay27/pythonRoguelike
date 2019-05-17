import pygame
import random
import sys
from map import *
from util import *
from animationController import *

		
class Game:
	CANVAS_WIDTH = 1000
	CANVAS_HEIGHT = 600

	def __init__(self):
		

		self.screen = pygame.display.set_mode((self.CANVAS_WIDTH,self.CANVAS_HEIGHT),pygame.DOUBLEBUF | pygame.HWSURFACE)
		
		self.player = Player(0,0)

		self.map = Map()
		self.map.loadRooms("rooms.txt")
		self.map.generateMap()
		self.map.printMap()
		self.map.generateTextures()
		self.player.pos.x = (self.map.rooms[0].bbox.x2-self.map.rooms[0].bbox.x1)/2*self.map.tileSize+self.map.tileSize*0.5
		self.player.pos.y = (self.map.rooms[0].bbox.y2-self.map.rooms[0].bbox.y1)/2*self.map.tileSize+self.map.tileSize*0.5
		
		self.cameraPos = Point(0,0)

		self.clock = pygame.time.Clock()
		self.gameLoop()


	def gameLoop(self):
		
		while 1: 
			self.clock.tick()

			self.deltaTime = 60/(self.clock.get_fps()+0.0001)
			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()			

			
			self.cameraPos.x,self.cameraPos.y = self.player.pos.x,self.player.pos.y
			#self.cameraPos.x,self.cameraPos.y = lerp(self.cameraPos.x,self.player.pos.x,0.01), lerp(self.cameraPos.y,self.player.pos.y,0.01)
			self.map.draw(self)
			self.player.draw(self)
			self.player.move(self)
			
			#put player in center of start room
			print(self.clock.get_fps())
			
			pygame.display.flip()


	def getCameraPoint(self,point):
		return Point(self.CANVAS_WIDTH/2+point.x-int(self.cameraPos.x), self.CANVAS_HEIGHT/2+point.y-int(self.cameraPos.y)).int()
	
class Player:
	
	def __init__(self, x, y):
		self.pos = Point(x,y)
		self.moveSpeed = 4
		self.direction = 0
		self.animation = AnimationController()

		self.animation.addAnimationState("test", "textures\\testanim.png", 8, 0.1)
		self.animation.setState("test")
	
	def draw(self,game): 
		drawPos = game.getCameraPoint(self.pos)
		#pygame.draw.circle(game.screen,(0,0,255),drawPos,5)

		game.screen.blit(self.animation.getFrame(),(0,0))
		
	def move(self,game):
		
		


		pressedKeys = pygame.key.get_pressed()

		newPos = Point(self.pos.x,self.pos.y)
		if pressedKeys[pygame.K_w]:
			newPos.y-= self.moveSpeed*game.deltaTime
		if pressedKeys[pygame.K_s]:
			newPos.y+= self.moveSpeed*game.deltaTime
		if pressedKeys[pygame.K_a]:
			newPos.x-= self.moveSpeed*game.deltaTime
		if pressedKeys[pygame.K_d]:
			newPos.x+= self.moveSpeed*game.deltaTime

		tile = Point(newPos.x//game.map.tileSize, newPos.y//game.map.tileSize).int()
		
		if game.map.tileAt(tile[0],tile[1]).type != 1:
			self.pos = newPos


game = Game()




