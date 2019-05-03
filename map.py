from util import *
import random
class Map(object):


	def __init__(self, sX,sY):


		self.tileSize = 32


	def loadRooms(self,filename):
		# seperate txt into array of room configurations
		file = open("rooms.txt","r")


		self.roomConfigurations = []


		lines = file.readlines() 

		loadedRoom = []
		for line in lines:
			if "&" not in line:
				loadedRoom.append([int(i) for i in line[:len(line)-1]])
			else:
				self.roomConfigurations.append(loadedRoom)
				loadedRoom = []
		print(self.roomConfigurations)







	def generateMap(self,sx,sy): # generates map with closed walls and random obstacles, temporary before BSP or loading map
		for y in range(sy):
			row = []
			for x in range(sx):
				val = int(random.random() > 0.8 or (x == 0 or x == sx-1 or y == 0 or y == sy-1))
				row.append(val)
			self.tiles.append(row)
		print(self.tiles)

	def tileAt(self,x,y):
		if self.tiles[y][x] == 1:
			return 1
		return 0
	def draw(self,cvs,cameraPos):
		for y in range(len(self.tiles)):
			for x in range(len(self.tiles[0])):
				if self.tileAt(x,y) == 1:
					tilePosX = Game.CANVAS_WIDTH/2-cameraPos.x+x*self.tileSize
					tilePosY = Game.CANVAS_HEIGHT/2-cameraPos.y+y*self.tileSize
					
					pygame.draw.rect(cvs,(0,0,255),(tilePosX,tilePosY,self.tileSize,self.tileSize))
	class Room:

		def __init__ (self, parent=None):
			self.tiles = []
			self.parent = parent

			
			#self.bbox = Rect(min(t.x for t in tiles), min(t.y for t in tiles), max(t.x for t in tiles), max(t.y for t in tiles))
		def generateRoom(self,x,y,spawnOnDoor=False):

			


	class Tile:

		def __init__ (self,x,y,t):
			self.x = x
			self.y = y
			self.type = t


m = Map(50, 50)


m.loadRooms("rooms.txt")
