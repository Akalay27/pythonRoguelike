import time
import pygame
class AnimationController(object):
	"""controls the animations"""
	def __init__(self):
		self.states = []
		
		self.currentState = None

	def addAnimationState(self,name,filename,size,speed,loop=False):

		tilemap = pygame.image.load(filename)


		frames = []

		for y in range(0,tilemap.get_height(),size):
			for x in range(0,tilemap.get_width(),size):
				frames.append(tilemap.subsurface((x,y,size,size)))

		state = AnimationController.AnimationState(name,frames,speed,loop)

		self.states.append(state)	

	def setState(self,name):
		for state in self.states:
			if state.name == name:
				self.currentState = state
				state.begin()

	def getFrame(self):
		return self.currentState.getFrame()


	class AnimationState(object):
		'''stores a single set of sprites and properties including speed and if looping'''
		def __init__(self,name,frames,speed,loop):
			self.frames = frames
			self.speed = speed
			self.loop = loop
			self.active = False
			self.name = name


		def begin(self):
			self.active = True
			self.startTime = time.time()
			self.frame = 0
		def getFrame(self):

			frame = int(((time.time()-self.startTime)/self.speed)%len(self.frames))

			return self.frames[frame]




		