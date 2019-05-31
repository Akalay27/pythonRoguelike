import pygame
from util import *
from animationController import *
from enum import Enum


class Direction(Enum):
	None_ =  0
	Up = 1
	Down = 2
	Left = 3
	Right = 4

	def state(self, moving):
		if moving:
			if self.name == 'None_':
				return 'walk_back'
			elif self.name == 'Up':
			 	return"walk_back"
			elif self.name == 'Down': 
				return "walk_forward"
			elif self.name == "Left": 
				return "walk_left"
			elif self.name == 'Right': 
				return "walk_right"
		else:
			if self.name == 'Up':
				return "stand_back"
			elif self.name == "Down":
				return "stand_forward"
			elif self.name == "Left":
				return "stand_left"
			elif self.name == 'Right':
				return 'stand_right'




class Entity(object):
	"""docstring for Entity"""
	def __init__(self, x, y):
		super(Entity, self).__init__()
		self.pos = Point(x,y)
		self.direction = Direction.None_
		self.animController = AnimationController()
		self.moving = False

	def __move(self, direction, speed, timeStep, game):
		newPos = Point(self.pos.x,self.pos.y)
		if self.direction == Direction.Up:
			newPos.y-= speed * timeStep
		elif self.direction == Direction.Down:
			newPos.y+= speed * timeStep
		elif self.direction == Direction.Left:
			newPos.x-= speed * timeStep
		elif self.direction == Direction.Right:
			newPos.x+= speed * timeStep

		self.direction = direction
		self.moving = True
		tile = Point(newPos.x//game.map.tileSize, newPos.y//game.map.tileSize).int()
		
		if game.map.tileAt(tile[0],tile[1]).type != 1:
			self.pos = newPos


	def moveUp(self, game, speed):
		self.__move(Direction.Up, speed, game.deltaTime, game)
		
	def moveDown(self, game, speed):
		self.__move(Direction.Down, speed, game.deltaTime, game)
	
	def moveLeft(self, game, speed):
		self.__move(Direction.Left, speed, game.deltaTime, game)
	

	def moveRight(self, game, speed):
		self.__move(Direction.Right, speed, game.deltaTime, game)
	

	def draw(self,game): 
		drawPos = game.getCameraPoint(self.pos)
		#pygame.draw.circle(game.screen,(0,0,255),drawPos,5)

		game.screen.blit(self.animController.getFrame(),(int(drawPos[0]-64),int(drawPos[1]-128)))

class Player(Entity):
	
	def __init__(self, x, y):
		super().__init__(x,y)
		self.moveSpeed = 4
		#self.direction = 0
		self.walkAnimationSpeed = 0.15
		#setting up player AnimationController

		frames = sliceTilemap(pygame.image.load("textures/PlayerTilemap.png"), 32,(128,128))

		self.animController.addAnimationState("stand_forward", [frames[16]],0)
		self.animController.addAnimationState("stand_back", [frames[17]],0)
		self.animController.addAnimationState("stand_right", [frames[18]],0)
		self.animController.addAnimationState("stand_left", [frames[19]],0)
		self.animController.addAnimationState("walk_forward", frames[0:4], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_back", frames[4:8], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_right", frames[8:12], self.walkAnimationSpeed, True)
		self.animController.addAnimationState("walk_left", frames[12:16], self.walkAnimationSpeed, True)
		
	
		
	def move(self,game):
		
		
		currentRoom = game.map.roomAt(self.pos.x//game.map.tileSize, self.pos.y//game.map.tileSize)

		currentRoom.setVisibility(visible=True)




		pressedKeys = pygame.key.get_pressed()


		if pressedKeys[pygame.K_SPACE]:
			self.moveSpeed = 8
			self.walkAnimationSpeed = 0.20
		else:
			self.moveSpeed = 4
			self.walkAnimationSpeed = 0.15
		#for running (space to run)

		
		self.moving = False
		if pressedKeys[pygame.K_w]:
			self.moveUp(game, self.moveSpeed)
		if pressedKeys[pygame.K_s]:
			self.moveDown(game, self.moveSpeed)
		if pressedKeys[pygame.K_a]:
			self.moveLeft(game, self.moveSpeed)
		if pressedKeys[pygame.K_d]:
			self.moveRight(game,  self.moveSpeed)

		self.animController.setState(self.direction.state(self.moving))
