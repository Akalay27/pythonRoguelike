import pygame
from util import *
from animationController import *

class Player:
	
	def __init__(self, x, y):
		self.pos = Point(x,y)
		self.moveSpeed = 4
		self.direction = 0
		self.animController = AnimationController()
		self.walkAnimationSpeed = 0.15
		#setting up player AnimationController

		frames = sliceTilemap(pygame.image.load("textures\\PlayerTilemap.png"), 32,(128,128))

		self.animController.addAnimationState("stand_forward", [frames[16]],0)
		self.animController.addAnimationState("stand_back", [frames[17]],0)
		self.animController.addAnimationState("stand_right", [frames[18]],0)
		self.animController.addAnimationState("stand_left", [frames[19]],0)
		self.animController.addAnimationState("walk_forward", frames[0:4], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_back", frames[4:8], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_right", frames[8:12], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_left", frames[12:16], self.walkAnimationSpeed, True)
		
	def draw(self,game): 
		drawPos = game.getCameraPoint(self.pos)
		#pygame.draw.circle(game.screen,(0,0,255),drawPos,5)

		game.screen.blit(self.animController.getFrame(),(int(drawPos[0]-64),int(drawPos[1]-128)))
		
	def move(self,game):
		
		
		

		pressedKeys = pygame.key.get_pressed()

		newPos = Point(self.pos.x,self.pos.y)
		moving = False
		if pressedKeys[pygame.K_w]:
			newPos.y-= self.moveSpeed*game.deltaTime
			moving = True
			self.direction = 0
		if pressedKeys[pygame.K_s]:
			newPos.y+= self.moveSpeed*game.deltaTime
			self.direction = 1
			moving = True
		if pressedKeys[pygame.K_a]:
			newPos.x-= self.moveSpeed*game.deltaTime
			self.direction = 2
			moving = True
		if pressedKeys[pygame.K_d]:
			newPos.x+= self.moveSpeed*game.deltaTime
			self.direction = 3
			moving = True


		if self.direction == 0 and moving: self.animController.setState("walk_back")
		elif self.direction == 1 and moving: self.animController.setState("walk_forward")
		elif self.direction == 2 and moving: self.animController.setState("walk_left")
		elif self.direction == 3 and moving: self.animController.setState("walk_right")
		elif self.direction == 0 and not moving: self.animController.setState("stand_back")
		elif self.direction == 1 and not moving: self.animController.setState("stand_forward")
		elif self.direction == 2 and not moving: self.animController.setState("stand_left")
		elif self.direction == 3 and not moving: self.animController.setState("stand_right")

		tile = Point(newPos.x//game.map.tileSize, newPos.y//game.map.tileSize).int()
		
		if game.map.tileAt(tile[0],tile[1]).type != 1:
			self.pos = newPos