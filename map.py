from util import *
import random
import pygame
import math
from pathlib import Path
from animationController import *
from enemy import *
class Map(object):

	MAX_HALLWAY_LENGTH = 30
	MAX_ITERS = 4
	MAX_ROOMS = 10
	tileSize = 16

	ENEMY_RANGE = (2,4)

	borderTypes = {"0000":0,"0011":1,"1001":2,"1100":7,"0110":6,"1010":3,"1000":13,"0010":8,"0101":5,"0100":10,"0001":15,"1111":12,"1011":11,"1110":16,"0111":17,"1101":18}

	def __init__(self):


		self.rooms = []
		self.loadRooms("rooms.txt")
		self.textures = self.loadTextures("textures/tilemapTest1.png", 16)
		self.borders = self.loadTextures("textures/testBorders.png", 16)
		self.generateMap()
		self.generateTextures()
		self.combineTiles()
		self.currentEnemies = []
		for room in self.rooms:
			room.createDoors()
			if not isinstance(room,self.Hallway) and self.rooms.index(room) != 0:
				room.generateEnemies()
		
	def loadRooms(self,filename):
		# seperate txt into array of room configurations
		file = open("rooms.txt","r")

		self.roomConfigurations = []

		lines = file.readlines() 

		loadedRoom = []
		for line in lines:
			if "&" not in line:
				loadedRoom.append([i for i in line[:len(line)-1]])
			else:
				self.roomConfigurations.append(loadedRoom)
				loadedRoom = []
		
	def generateMap(self):
		self.rooms = []
		'''creates root room and generates all rooms of the map'''
		self.numberOfRooms = 0

		self.rooms = []
		origin = self.Room(self,self.rooms)

		origin.generateRoom()
		#origin.setPosition(-5, -5, 1)
		origin.createChildren()

		origin.entering = True	

	def tileAt(self,x,y,room=None,bbox=None,fast=False):
		'''returns Map.Tile at location, returns Map.Tile of type None if no tile found, optionally searching in one specific room or in a rectangular area'''
		
		if not fast:
			if room == None:

				for r in self.rooms:
					if bbox != None:
						if not r.bbox.collidesWithRect(bbox): continue
					if r.bbox.insideOf(x,y):
						for t in r.tiles:
							if t.x == x and t.y == y:
								return t
			else:
				for t in room.tiles:
					if t.x == x and t.y == y:
						return t
		else:
			return self.getTileFromArray(x, y)
		return Map.Tile(x,y, None)

	def roomAt(self,x,y):
		'''returns Map.Room at location, returns Map.Tile of type None if no tile found.'''
		for room in self.rooms:
			if room.bbox.insideOf(x,y):
				return room
		return None

	def neighbors(self,x,y,room=None,fast=False): #clockwise from +x
		'''returns array of 8 neighbors around a Tile, starting from left (x+1,y) clockwise'''
		neighbors = []
		neighbors.append(self.tileAt(x+1,y,room=room,fast=fast))
		neighbors.append(self.tileAt(x+1,y+1,room=room,fast=fast))
		neighbors.append(self.tileAt(x,y+1,room=room,fast=fast))
		neighbors.append(self.tileAt(x-1,y+1,room=room,fast=fast))
		neighbors.append(self.tileAt(x-1,y,room=room,fast=fast))
		neighbors.append(self.tileAt(x-1,y-1,room=room,fast=fast))
		neighbors.append(self.tileAt(x,y-1,room=room,fast=fast))
		neighbors.append(self.tileAt(x+1,y-1,room=room,fast=fast))
		return neighbors

	def combineTiles(self):
		'''for drawing tiles on the screen, using a large 2d array instead of individual objects using search function'''
		minX, maxX, minY, maxY = 0,0,0,0


		for room in self.rooms:
			for tile in room.tiles:

				if tile.x < minX: minX = tile.x
				if tile.x > maxX: maxX = tile.x
				if tile.y < minY: minY = tile.y
				if tile.y > maxY: maxY = tile.y

		self.bbox = Rect(minX, minY, maxX, maxY)

		self.allTiles = []

		for y in range(minY,maxY+1):
			row = []
			for x in range(minX,maxX+1):
				row.append(self.tileAt(x,y))
			self.allTiles.append(row)

	def getTileFromArray(self,x,y):
		if x >= self.bbox.x1 and x <= self.bbox.x2 and y >= self.bbox.y1 and y <= self.bbox.y2:
			return self.allTiles[y-self.bbox.y1][x-self.bbox.x1]
		return Map.Tile(x,y, None)


	def printMap(self):
		'''prints the Map in ascii format'''
		for y in range(-40,40):
			for x in range(-40,40):
				if (x,y) != (0,0):
					if self.tileAt(x,y).type != None:
						print(self.tileAt(x,y).type,end="")
					else:
						print(" ", end="")
				else:
					print("x",end="")
			print("")
	
			
	class Room:
		'''holds Map tiles located inside of the Room and creates children rooms'''
		def __init__ (self, map, rooms, iterationStep = 0):
			self.map = map
			self.roomArray = rooms
			self.roomArray.append(self)
			self.iterationStep = iterationStep
			self.numberOfChildren = 1

			self.enemies = []


			self.entered = False
			self.entering = False


		def setVisibility(self,visible):
			for tile in self.tiles:
				tile.visible = visible

		def generateRoom(self):
			'''chooses room configuration from Map's room file'''
			self.tiles = []
			configIndex = random.randint(0,len(self.map.roomConfigurations)-1)
			#print("CONFIG #{}".format(configIndex))
			config = self.map.roomConfigurations[configIndex]
			
			for y in range(len(config)):
				for x in range(len(config[y])):
					if config[y][x] != " ":
						self.tiles.append(Map.Tile(x,y,int(config[y][x])))
			
			self.calculateBBox()
			
			doorTiles = []

			for t in self.tiles:  #figure out direction of each door (so it generates outwards) 
				if t.type == Map.Tile.DOOR:
					nb = self.map.neighbors(t.x, t.y,self)
					if nb[4].type == Map.Tile.FLOOR:
						doorDirection = 0
					if nb[6].type == Map.Tile.FLOOR:
						doorDirection = 1
					if nb[0].type == Map.Tile.FLOOR:
						doorDirection = 2
					if nb[2].type == Map.Tile.FLOOR:
						doorDirection = 3
					t.direction = doorDirection
					doorTiles.append(t)
			self.doorTiles = doorTiles

		def getDoorCoordDir(self,direction,twoDirections=False):
			'''returns +x,y-, -x,-y etc for each direction 0-3 clockwise. If twoDirections is true then only +x or +y'''
			if twoDirections:
				if direction == 0 or direction == 2:
					moveDir = Point(1,0)
				else:
					moveDir = Point(0,1)
			else:
				if direction == 0:
					moveDir = Point(1,0)
				elif direction == 1:
					moveDir = Point(0,1)
				elif direction == 2:
					moveDir = Point(-1,0)
				else:
					moveDir = Point(0,-1)
			return moveDir

		def calculateBBox(self,collideTest=False):
			'''updates bounding box of the room. This must be called when moving or changing the room configuration collideTest expands bounding box up 2 and left, right, and bottom sides are expanded 1'''
			

			self.bbox = Rect(min(t.x for t in self.tiles), min(t.y for t in self.tiles), max(t.x for t in self.tiles), max(t.y for t in self.tiles))
			
			if collideTest:
				self.bbox.y1-=2
				
		def setPosition(self,x,y,doorDirection,selected=None):
			'''sets the position of the room based on a door Tile facing a certain direction or a pre-selected door tile''' 
			if selected != None:
				selectedDoor = selected
			else:
				#
				possibleDoors = []
				for doorTile in self.doorTiles:
					if doorTile.direction == doorDirection:
						possibleDoors.append(doorTile)	
				if len(possibleDoors) == 0: return -1 
				selectedDoor = possibleDoors[random.randint(0,len(possibleDoors)-1)] #if there are 2 doorTiles facing the right direction, then choose 1
				
			moveX = x-selectedDoor.x 
			moveY = y-selectedDoor.y
			for t in self.tiles: #shift entire room to new position
				t.x+=moveX
				t.y+=moveY

			self.calculateBBox(collideTest=False)
			return selectedDoor

		def createChildren(self):
			'''create iterations of room based on doorTiles of Room'''

			done = False
			self.children = []


			for doorTile in self.doorTiles:
				doorTile.type = Map.Tile.WALL 

			selectedDoors = []

			selectedDoors = self.doorTiles
			for doorTile in selectedDoors:

				child = Map.Room(self.map,self.roomArray,self.iterationStep+1)

				selectedDoor = -1
				connectingDirection = (doorTile.direction+2)%4
				while selectedDoor == -1: #get new configuration of room until the configuration contains a door facing the right direction
					child.generateRoom()
					selectedDoor = child.setPosition(doorTile.x, doorTile.y, connectingDirection)

				
				moveDir = self.getDoorCoordDir(doorTile.direction)
				invalidChild = False

				for distance in range(random.randint(3,8),Map.MAX_HALLWAY_LENGTH+1): #move new child away from this room until it doesn't collide with anything else
					
					newDoorPosition = Point(doorTile.x+moveDir.x*distance,doorTile.y+moveDir.y*distance)
					child.setPosition(newDoorPosition.x, newDoorPosition.y, (doorTile.direction+2)%4, selectedDoor)
					validPos = True
					for room in self.roomArray:
						if room != child:
							if room.bbox.collidesWithRect(child.bbox):
								validPos = False
								
					if validPos == True:
						break
					if distance == Map.MAX_HALLWAY_LENGTH:
						invalidChild = True
						doorTile.type = Map.Tile.WALL
						break
						
				
			
				child.doorTiles.remove(selectedDoor)

				if not invalidChild: #if hallway connection intersects with anything then also invalidate child
					if (manhattanDistance(doorTile.toPoint(),selectedDoor.toPoint()) > 1):
						hallway = Map.Hallway(self.map, self.roomArray)
						hallway.generateHallway(doorTile,selectedDoor)
						for r in self.roomArray:
							if r != hallway:
								if r.bbox.collidesWithRect(hallway.bbox):
									invalidChild = True

									doorTile.type = Map.Tile.WALL
									self.roomArray.remove(hallway)
									break

				if invalidChild:
					self.roomArray.remove(child)

					continue
				
				doorTile.type = Map.Tile.DOOR
				self.children.append(child)
				self.map.numberOfRooms+=1

				#make 2 doorTiles instead of 1

				secondOffset = self.getDoorCoordDir((doorTile.direction-1)%4,twoDirections=True)
				secondDoor, secondDoorChild = self.map.tileAt(doorTile.x+secondOffset.x,doorTile.y+secondOffset.y), self.map.tileAt(selectedDoor.x+secondOffset.x,selectedDoor.y+secondOffset.y)
				secondDoor.type, secondDoorChild.type = Map.Tile.DOOR, Map.Tile.DOOR
				secondDoor.direction, secondDoorChild.direction = doorTile.direction, selectedDoor.direction

				secondDoor.connected = True
				secondDoorChild.connected = True
				doorTile.connected = True
				selectedDoor.connected = True



				if self.map.numberOfRooms > Map.MAX_ROOMS:
					done = True
					break
						
				
				
				
				
			for child in self.children:
				if not done:
					child.createChildren()
				else:
					for tile in child.tiles: #remove other doorTiles of child if child isn't going to have more rooms
						if tile.connected == False and tile.type == Map.Tile.DOOR:
							tile.type = Map.Tile.WALL
						
		def createDoors(self):

			self.doors = []
			
			usedTiles = []
			for tile in self.tiles:
				if tile.type == Map.Tile.DOOR and tile not in usedTiles:
					nb = self.map.neighbors(tile.x, tile.y)
					if nb[0].type == Map.Tile.DOOR:

						usedTiles.extend((tile,nb[0]))
						self.doors.append(self.Door(tile.direction,(tile,nb[0])))

					if nb[6].type == Map.Tile.DOOR:
						usedTiles.extend((tile,nb[6]))
						self.doors.append(self.Door(tile.direction,(tile,nb[6])))

		class Door (object):

			def __init__ (self,direction,tiles):

				self.direction = direction
				self.tiles = tiles
				self.animController = AnimationController()
				self.locked = False
				self.open = False
				if self.direction == 1 or self.direction == 3:
					anim = sliceTilemap(pygame.image.load("textures\\doorFront.png"),(32,32), (Map.tileSize*2, Map.tileSize*2))
				else:
					anim = sliceTilemap(pygame.image.load("textures\\doorSide.png"),(16,48), (Map.tileSize, Map.tileSize*3))
				self.animController.addAnimationState("locked", [anim[0]], 0.1)
				self.animController.addAnimationState("unlocked", [anim[1]], 0.1)
				self.animController.addAnimationState("open", anim[1:], 0.05, loop=False)
				self.animController.addAnimationState("close", anim[len(anim)-1:0:-1], 0.05,loop=False)

				self.animController.setState("unlocked")


				for t in self.tiles:
					t.type = Map.Tile.WALL
				
			def openDoor(self):
				if self.open == False:
					
					if not self.locked:
						self.open = True
						for t in self.tiles:
							t.type = Map.Tile.FLOOR
						self.animController.setState("open")

			def closeDoor(self):
				if self.open == True:
					self.open = False

					for t in self.tiles:
						t.type = Map.Tile.WALL
					self.animController.setState("close")


			def lockDoor(self):

				self.locked = True
				if self.open:
					self.closeDoor()
				else:
					self.animController.setState("locked")


			def unlockDoor(self):

				self.locked = False
				if not self.open:
					self.animController.setState("unlocked")
				else:
					self.openDoor()

		

			def draw(self,game):

				if self.direction == 1 or self.direction == 3:
					texOffset = 1
				else:
					texOffset = 3

				drawPos = game.getCameraPoint(Point(self.tiles[0].x*Map.tileSize,(self.tiles[0].y-texOffset)*Map.tileSize))

				game.screen.blit(self.animController.getFrame(),(int(drawPos[0]),int(drawPos[1])))


		def generateEnemies(self):

			numberOfEnemies = random.randint(Map.ENEMY_RANGE[0], Map.ENEMY_RANGE[1])

			spawnTiles = []


			while len(spawnTiles) < numberOfEnemies:


				tile = self.tiles[random.randint(0,len(self.tiles)-1)]

				if tile.type == Map.Tile.FLOOR:

					invalid = False
					for n in self.map.neighbors(tile.x, tile.y):
						if n.type == Map.Tile.DOOR:
							invalid = True
							break
					if invalid: continue

					spawnTiles.append(tile)
			
			for tile in spawnTiles:

				self.enemies.append(Ball(tile.x*self.map.tileSize,tile.y*self.map.tileSize,10,10))

		def activateRoom(self):

			if not self.entered:
				self.entered = True

				for door in self.doors:
					door.lockDoor()

				for enemy in self.enemies:
					enemy.enabled = True

		def checkCompleted(self):

			numberAlive = 0

			for e in self.enemies:
				if e.health > 0: numberAlive+=1

			if numberAlive == 0:
				for door in self.doors:
					door.unlockDoor()

	class Hallway(Room):
		"""Room connecting rooms together"""
		

		def generateHallway(self,tStart,tEnd): #make walls connecting rooms together, NOT including walls adjacent to doorTiles.
			self.tiles = []
			moveDir = self.getDoorCoordDir(tStart.direction,twoDirections=True)

			if tStart.x > tEnd.x or tStart.y > tEnd.y:
				tStart, tEnd = tEnd, tStart


			steps = manhattanDistance(tStart.toPoint(), tEnd.toPoint())
			sideDirection = self.getDoorCoordDir(((tStart.direction-1)%4),twoDirections=True)
		
			for i in range(1,steps):
				stepPosition = Point(tStart.x+moveDir.x*i, tStart.y+moveDir.y*i)

				leftWall = Map.Tile(stepPosition.x+sideDirection.x*2, stepPosition.y+sideDirection.y*2, Map.Tile.WALL)
				rightWall = Map.Tile(stepPosition.x-sideDirection.x, stepPosition.y-sideDirection.y, Map.Tile.WALL)
				floorLeft = Map.Tile(stepPosition.x+sideDirection.x, stepPosition.y+sideDirection.y, Map.Tile.FLOOR)
				floorRight = Map.Tile(stepPosition.x, stepPosition.y, Map.Tile.FLOOR)
				self.tiles.append(floorLeft)
				self.tiles.append(floorRight)
				self.tiles.append(leftWall)
				self.tiles.append(rightWall)
				

			self.calculateBBox()

	def loadTextures(self,filename,size):
		
		img = pygame.image.load(filename)

		textures = []
		imgWidth, imgHeight = img.get_size()

		for y in range(0,imgHeight,size):
			for x in range(0,imgWidth,size):
				tex = pygame.transform.scale(img.subsurface(pygame.Rect(x,y,size,size)),(self.tileSize,self.tileSize))
				textures.append(tex)
		return textures
		
	def generateTextures(self):


		for room in self.rooms:

			for tile in room.tiles:

				nb = self.neighbors(tile.x,tile.y)
				if tile.type == Map.Tile.FLOOR or tile.type == Map.Tile.DOOR and tile.wallType == 0:
					
				
					tile.texture = self.textures[10]
					

				

				if tile.type == Map.Tile.WALL:
					

					wallSeg2 = self.tileAt(tile.x, tile.y-1)
					wallSeg3 = self.tileAt(tile.x, tile.y-2)

					if wallSeg2.type == None:
						room.tiles.append(wallSeg2)
					if wallSeg3.type == None:
						room.tiles.append(wallSeg3)


					#if below the floor tiles, then only occlude 1 tile in front. Otherwise occlude 2 like normal

					if nb[2].type == Map.Tile.FLOOR or nb[2].type == Map.Tile.DOOR: #front facing wall case
						tile.texture = self.textures[random.randint(5,9)]
						wallSeg2.texture = self.textures[random.randint(0,4)]
						wallSeg3.texture = self.getBorderTexture(nb)
						wallSeg2.wallType, wallSeg3.wallType, tile.wallType = 2 , 3, 1
						
						y = 1
						
						while self.tileAt(tile.x,tile.y-y).type == Map.Tile.WALL:
							nextAbove = self.tileAt(tile.x,tile.y-2-y)

							if self.roomAt(nextAbove.x,nextAbove.y) != room:
								break
							nextAbove.texture = self.getBorderTexture(self.neighbors(tile.x,tile.y-y))
							nextAbove.wallType = 3
							y+=1
							



					elif nb[6].type == Map.Tile.FLOOR and (nb[2].type == None or nb[2].type == Map.Tile.WALL) and tile.wallType != 3 and wallSeg2.wallType != 3: #bottom of room case
						wallSeg2.texture = self.getBorderTexture(self.neighbors(tile.x,tile.y))
						tile.texture = self.getBorderTexture(self.neighbors(tile.x,tile.y+1))
						wallSeg2.wallType = 3
						tile.wallType = 3

					elif tile.wallType == 0: #vertical sides of rooms, find bottom tile of the row and then iterate upwards
						tile.texture = self.getBorderTexture(nb)

						
						

						
						lowestTile = tile
						ly = 0
						while self.tileAt(tile.x,tile.y+ly) == Map.Tile.WALL:
							lowestTile = self.tileAt(tile.x,tile.y+ly)
							ly+=1

						y = 0

						offset = 1
						while self.tileAt(lowestTile.x,lowestTile.y-y).type == Map.Tile.WALL and self.tileAt(lowestTile.x,lowestTile.y-y).wallType != 3:
							nextAbove = self.tileAt(lowestTile.x,lowestTile.y-offset-y)
							

							if nextAbove.type == Map.Tile.FLOOR:
								offset = 1
							if nextAbove.type == None:
								room.tiles.append(nextAbove)
								room.calculateBBox()
							if self.roomAt(nextAbove.x,nextAbove.y) != room or self.neighbors(nextAbove.x,nextAbove.y-2)[6] == Map.Tile.FLOOR:
								break
							nextAbove.texture = self.getBorderTexture(self.neighbors(lowestTile.x,lowestTile.y-y))
							nextAbove.wallType = 3
							y+=1
							print(y)

							if y > 0:
								offset = 2

							

					room.calculateBBox()

					# elif tile.wallType == 0:

					# 	if (nb[0].type == Map.Tile.FLOOR and nb[4].type == None) or (nb[0].type == None or nb[4].type == Map.Tile.FLOOR):
					# 		tile.texture = self.getBorderTexture(self.neighbors(tile.x,tile.y+1))
					# 	else:
					# 		tile.texture = self.getBorderTexture(self.neighbors(tile.x,tile.y+2))
						



						
		for room in self.rooms:

			for tile in room.tiles: 

				if tile.wallType in (1,2):
						tile.type = Map.Tile.WALL			
						
					
						
						#set top wall segment later when all top wall segments are defined
					
						



				#if tile.type == Map.Tile.FLOOR:

	def getBorderTexture(self,nb):
		
		option = ""
		
		for t in (nb[0],nb[2],nb[4],nb[6]):
			if t.type == Map.Tile.WALL or t.type == None:
				option = option + "0"
			else:
				option = option + "1"

		#return self.textures[self.borderTypes[option]]  //WHEN THERE ARE NO BORDER TEXTURES
		return self.borders[self.borderTypes[option]]


	def draw(self,game,background=True):
		tileRangeY = math.ceil(game.CANVAS_HEIGHT/self.tileSize/2)+1
		tileRangeX = math.ceil(game.CANVAS_WIDTH/self.tileSize/2)+1
		cameraTilePos = Point(int(game.cameraPos.x/self.tileSize), int(game.cameraPos.y/self.tileSize))
		
		
		for y in range(cameraTilePos.y-tileRangeY,cameraTilePos.y+tileRangeY):
			for x in range(cameraTilePos.x-tileRangeX,cameraTilePos.x+tileRangeX):
				tile = self.tileAt(x, y,fast=True)
				
		
				if (tile.wallType == 3) and not background or background:

					drawPos = game.getCameraPoint(Point(x*self.tileSize,y*self.tileSize))
				
				

					if tile.texture != None:
						game.screen.blit(tile.texture,(drawPos[0],drawPos[1]))


		cameraBBox = Rect(game.cameraPos.x-game.screen.get_width(),game.cameraPos.y-game.screen.get_height(),game.cameraPos.x+game.screen.get_width(),game.cameraPos.y+game.screen.get_height())
		
		for room in self.rooms:

			worldBBox = Rect(room.bbox.x1*self.tileSize,room.bbox.y1*self.tileSize,room.bbox.x2*self.tileSize,room.bbox.y2*self.tileSize)

			if worldBBox.collidesWithRect(cameraBBox):
				for door in room.doors:
					if ((door.direction == 0 or door.direction == 2) and background) or ((door.direction == 1 or door.direction == 3) and not background):
						door.draw(game)
					
					doorWorldPos = Point(door.tiles[0].x*self.tileSize,door.tiles[0].y*self.tileSize)
					if manhattanDistance(doorWorldPos, game.player.pos) < 200:
						door.openDoor()

				for enemy in room.enemies:
					enemy.draw(game)
					enemy.move(game)

	class Tile:

		DOOR = 2
		WALL = 1
		FLOOR = 0

		def __init__ (self,x,y,t):
			self.x = x
			self.y = y
			self.type = t
			self.direction = -1

			self.texture = None

			self.wallType = 0 #only for setting correct border tile

			self.connected = False

			self.visible = False
		def __str__ (self):
			return "Tile of type {} at {}, {}".format(self.type,self.x,self.y)
		def toPoint(self):
			return Point(self.x, self.y)
