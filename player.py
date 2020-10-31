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

		self.attackingEnemies = []

		#setting up player AnimationController

		frames = sliceTilemap(pygame.image.load("textures\\PlayerTilemap.png"), (32,32),(128,128))

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
	
	def calculateBBox(self):
		self.bbox = Rect(x1, y1, x2, y2)





	def swing(self,direction):

		across = 50 
		forward = 50

		damage = 10



		if direction == 0:
			hitBox = Rect(self.pos.x, self.pos.y-across/2, self.pos.x+forward, self.pos.y+across/2)
		if direction == 1:
			hitBox = Rect(self.pos.x-across/2, self.pos.y, self.pos.x+across/2, self.pos.y+forward)
		if direction == 2:
			hitBox = Rect(self.pos.x-forward, self.pos.y-across/2, self.pos.x, self.pos.y+across/2)
		if direction == 3:
			hitBox = Rect(self.pos.x-across/2, self.pos.y-forward, self.pos.x+across/2, self.pos.y)


		for e in self.attackingEnemies:

			if e.bbox.collidesWithRect(hitBox):

				e.health -= 10






	def move(self,game):
		
		
		currentRoom = game.map.roomAt(self.pos.x//game.map.tileSize, self.pos.y//game.map.tileSize)
		if currentRoom != None:
			currentRoom.setVisibility(visible=True)




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
		
		#attack

		if pressedKeys[pygame.K_SPACE]:
			if self.direction == 3: self.swing(0)
			elif self.direction == 1: self.swing(1)
			elif self.direction == 2: self.swing(2)
			elif self.direction == 3: self.swing(3)

		if game.map.tileAt(tile[0],tile[1]).type != game.map.Tile.WALL:
			self.pos = newPos