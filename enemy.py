from util import *
import math
import random
import time
from animationController import *

class Enemy (object):
	"""docstring for Enemy"""
	def __init__(self, x, y, health, damage):
	
		super(Enemy, self).__init__()

		self.pos = Point(x, y)
		self.damage = damage
		self.health = health

		self.alive = True
		self.enabled = False

		self.animController = AnimationController()
class Ball (Enemy):

	def __init__ (self,x,y,health,damage):

		super(Ball,self).__init__(x,y,health,damage)

		frames = sliceTilemap(pygame.image.load("textures\\ballEnemy.png"), (16,16),scaleSize=(64,64))
		
		self.animController.addAnimationState("disabled",[frames[1]],0.1)
		self.animController.addAnimationState("enabled",[frames[0]],0.1)
		self.animController.addAnimationState("dead",[frames[2]],0.1)
		self.velocity = Point(0, 0)

		self.animController.setState("disabled")
	def move(self,game):

		self.bbox = Rect(self.pos.x-15, self.pos.y-15, self.pos.x+15, self.pos.y+15)

		if self.health <= 0:
			self.alive = False
			self.animController.setState("dead")

		if self.alive and self.enabled:
			self.animController.setState("enabled")
			self.prevPos = Point(self.pos.x,self.pos.y)
			self.pos.x+=self.velocity.x
			self.pos.y+=self.velocity.y

			self.velocity.x*=0.90
			self.velocity.y*=0.90

			
			newTarget = Point(game.player.pos.x,game.player.pos.y-64)
			angle = math.atan2(newTarget.y-self.pos.y,newTarget.x-self.pos.x)+random.random()*0.1

			magnitude = 0.2
			if game.deltaTime < 10:
				magnitude *= game.deltaTime

			self.velocity.x+=math.cos(angle)*magnitude
			self.velocity.y+=math.sin(angle)*magnitude



			#collision detection --> bounce off walls
			currentTile = game.map.tileAt(int(self.pos.x//game.map.tileSize), int(self.pos.y//game.map.tileSize),fast=True)
			prevTile = game.map.tileAt(int(self.prevPos.x//game.map.tileSize), int(self.prevPos.y//game.map.tileSize),fast=True)

			if currentTile != prevTile and currentTile.type == game.map.Tile.WALL:
				direction = game.map.neighbors(prevTile.x, prevTile.y).index(currentTile)
				print("direction: ", direction)
				if direction == 0 or direction == 4:
					self.velocity.x*=-0.9
				if direction == 2 or direction == 6:
					self.velocity.y*=-0.9
				if direction in (1,3,5,7):
					self.velocity.x*=-0.9
					self.velocity.y*=-0.9



	def draw(self,game):
		drawPos = game.getCameraPoint(self.pos)
		game.screen.blit(self.animController.getFrame(),(int(drawPos[0])-32,int(drawPos[1])-32))