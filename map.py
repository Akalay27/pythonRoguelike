from util import *
import random
import pygame
import math
class Map(object):

	MAX_HALLWAY_LENGTH = 20
	MAX_ITERS = 4
	MAX_ROOMS = 15

	def __init__(self):


		self.rooms = []

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

		def getDoorCoordDir(self,direction):
			'''returns +x,y-, -x,-y etc for each direction 0-3 clockwise'''
			if direction == 0:
				moveDir = Point(1,0)
			elif direction == 1:
				moveDir = Point(0,1)
			elif direction == 2:
				moveDir = Point(-1,0)
			else:
				moveDir = Point(0,-1)
			return moveDir

		def calculateBBox(self):
			'''updates bounding box of the room. This must be called when moving or changing the room configuration'''
			self.bbox = Rect(min(t.x for t in self.tiles), min(t.y for t in self.tiles), max(t.x for t in self.tiles), max(t.y for t in self.tiles))
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

			self.calculateBBox()
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
						for room in self.roomArray:
							if room != hallway:
								if room.bbox.collidesWithRect(hallway.bbox):
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
			moveDir = self.getDoorCoordDir(tStart.direction)

			steps = manhattanDistance(tStart.toPoint(), tEnd.toPoint())
			leftWallDirection = self.getDoorCoordDir(((tStart.direction-1)%4))
			rightWallDirection = self.getDoorCoordDir(((tStart.direction+1)%4))
			for i in range(1,steps):
				stepPosition = Point(tStart.x+moveDir.x*i, tStart.y+moveDir.y*i)

				leftWall = Map.Tile(stepPosition.x+leftWallDirection.x, stepPosition.y+leftWallDirection.y, Map.Tile.WALL)
				rightWall = Map.Tile(stepPosition.x+rightWallDirection.x, stepPosition.y+rightWallDirection.y, Map.Tile.WALL)
				floor = Map.Tile(stepPosition.x, stepPosition.y, Map.Tile.FLOOR)
				self.tiles.append(leftWall)
				self.tiles.append(rightWall)
				self.tiles.append(floor)

			self.calculateBBox()



			

	
			
	class Tile:

		DOOR = 2
		WALL = 1
		FLOOR = 0

		def __init__ (self,x,y,t):
			self.x = x
			self.y = y
			self.type = t
			self.direction = -1


		def __str__ (self):
			return "Tile of type {} at {}, {}".format(self.type,self.x,self.y)
		def toPoint(self):
			return Point(self.x, self.y)
