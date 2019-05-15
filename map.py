from util import *
import random
import pygame
import math
from pathlib import Path

class Map(object):

	MAX_HALLWAY_LENGTH = 30
	MAX_ITERS = 4
	MAX_ROOMS = 30
	tileSize = 64

	borderTypes = {"0000":0,"0011":1,"1001":2,"1100":7,"0110":6,"1010":3,"1000":13,"0010":8,"0101":5,"0100":10,"0001":15,"1111":12,"1011":11,"1110":16,"0111":17,"1101":18}

	def __init__(self):


		self.rooms = []

		self.loadTextures("textures/tilemapTest1.png", 16)

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
		print(self.roomConfigurations)



	def generateMap(self):
		'''creates root room and generates all rooms of the map'''
		self.rooms = []
		origin = self.Room(self,self.rooms)

		origin.generateRoom()
		#origin.setPosition(-5, -5, 1)
		origin.createChildren()

	def tileAt(self,x,y,room=None,bbox=None):
		'''returns Map.Tile at location, returns Map.Tile of type None if no tile found, optionally searching in one specific room or in a rectangular area'''
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
		return Map.Tile(x,y, None)
	def roomAt(self,x,y):
		'''returns Map.Room at location, returns Map.Tile of type None if no tile found.'''
		for room in self.rooms:
			if room.bbox.insideOf(x,y):
				return room
		return Map.Tile(x,y, None)
	def neighbors(self,x,y,room=None): #clockwise from +x
		'''returns array of 8 neighbors around a Tile, starting from left (x+1,y) clockwise'''
		neighbors = []
		neighbors.append(self.tileAt(x+1,y,room))
		neighbors.append(self.tileAt(x+1,y+1,room))
		neighbors.append(self.tileAt(x,y+1,room))
		neighbors.append(self.tileAt(x-1,y+1,room))
		neighbors.append(self.tileAt(x-1,y,room))
		neighbors.append(self.tileAt(x-1,y-1,room))
		neighbors.append(self.tileAt(x,y-1,room))
		neighbors.append(self.tileAt(x+1,y-1,room))
		return neighbors



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
			
			doors = []

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
					doors.append(t)
			self.doors = doors

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
				self.bbox.x1-=1
				self.bbox.x2+=1
				self.bbox.y1-=2
				self.bbox.y2+=1
		def setPosition(self,x,y,doorDirection,selected=None):
			'''sets the position of the room based on a door Tile facing a certain direction or a pre-selected door tile''' 
			if selected != None:
				selectedDoor = selected
			else:
				#
				possibleDoors = []
				for doorTile in self.doors:
					if doorTile.direction == doorDirection:
						possibleDoors.append(doorTile)	
				if len(possibleDoors) == 0: return -1 
				selectedDoor = possibleDoors[random.randint(0,len(possibleDoors)-1)] #if there are 2 doors facing the right direction, then choose 1
				
			moveX = x-selectedDoor.x 
			moveY = y-selectedDoor.y
			for t in self.tiles: #shift entire room to new position
				t.x+=moveX
				t.y+=moveY

			self.calculateBBox(collideTest=False)
			return selectedDoor

		
		def createChildren(self):
			'''create iterations of room based on doors of Room'''
			self.children = []


			for doorTile in self.doors:
				doorTile.type = Map.Tile.WALL 

			selectedDoors = []

			self.numberOfChildren = random.randint(1, len(self.doors))

			while (len(selectedDoors) < self.numberOfChildren):
				door = self.doors[random.randint(0,len(self.doors)-1)]

				if door not in selectedDoors:
					selectedDoors.append(door)



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
						
				
			
				child.doors.remove(selectedDoor)
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
				else:
					doorTile.type = Map.Tile.DOOR
					self.children.append(child)


					#make 2 doors instead of 1

					secondOffset = self.getDoorCoordDir((doorTile.direction-1)%4,twoDirections=True)
					secondDoor, secondDoorChild = self.map.tileAt(doorTile.x+secondOffset.x,doorTile.y+secondOffset.y), self.map.tileAt(selectedDoor.x+secondOffset.x,selectedDoor.y+secondOffset.y)
					secondDoor.type, secondDoorChild.type = Map.Tile.DOOR, Map.Tile.DOOR
					secondDoor.direction, secondDoorChild.direction = doorTile.direction, selectedDoor.direction



				#make doors close off also better way of limiting rooms please
				if len(self.roomArray) > Map.MAX_ROOMS:

					for door in child.doors: #remove other doors of child if child isn't going to have more rooms
						if door != selectedDoor:
							door.type = Map.Tile.WALL
					return
				
				
				
				
			for child in self.children:
				child.createChildren()

				
	class Hallway(Room):
		"""Room connecting rooms together"""
		

		def generateHallway(self,tStart,tEnd): #make walls connecting rooms together, NOT including walls adjacent to doors.
			self.tiles = []
			moveDir = self.getDoorCoordDir(tStart.direction,twoDirections=True)

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
		self.textures = textures




			
	def generateTextures(self):


		for room in self.rooms:

			for tile in room.tiles:

				nb = self.neighbors(tile.x,tile.y)
				if tile.type == Map.Tile.FLOOR or tile.type == Map.Tile.DOOR and tile.wallType == 0:
					tile.texture = self.textures[10]
					pass

				

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
		return self.textures[19]


	def draw(self,game):
		tileRangeY = math.ceil(game.CANVAS_HEIGHT/self.tileSize/2)+1
		tileRangeX = math.ceil(game.CANVAS_WIDTH/self.tileSize/2)+1
		cameraTilePos = Point(int(game.cameraPos.x/self.tileSize), int(game.cameraPos.y/self.tileSize))
		
		
		for y in range(cameraTilePos.y-tileRangeY,cameraTilePos.y+tileRangeY):
			for x in range(cameraTilePos.x-tileRangeX,cameraTilePos.x+tileRangeX):
				drawPos = game.getCameraPoint(Point(x*self.tileSize,y*self.tileSize))
				
				tile = self.tileAt(x, y)

				if tile.texture != None:
					game.screen.blit(tile.texture,(drawPos[0],drawPos[1]))


	# def bakeTextures(self, room=None, tile=None): #turn all textures into 2d array for quick accessing.



	# 	if room == None and tile == None:



			
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
		def __str__ (self):
			return "Tile of type {} at {}, {}".format(self.type,self.x,self.y)
		def toPoint(self):
			return Point(self.x, self.y)
