import pygame
import random
import sys
from map import *
from util import *
from animationController import *
from player import *
		
class Game:
	CANVAS_WIDTH = 1000
	CANVAS_HEIGHT = 600

	def __init__(self):
		

		self.screen = pygame.display.set_mode((self.CANVAS_WIDTH,self.CANVAS_HEIGHT),pygame.DOUBLEBUF | pygame.HWSURFACE)
		
		self.player = Player(0,0)

		self.map = Map()
		self.map.loadRooms("rooms.txt")
		self.map.generateMap()
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
			self.player.move(self)
			self.player.draw(self)
			
			
			#put player in center of start room
			print(self.clock.get_fps())
			
			pygame.display.flip()


	def getCameraPoint(self,point):
		return Point(self.CANVAS_WIDTH/2+point.x-int(self.cameraPos.x), self.CANVAS_HEIGHT/2+point.y-int(self.cameraPos.y)).int()
	



game = Game()




