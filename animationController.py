import time
import pygame
class AnimationController(object):
	"""controls the animations"""
	def __init__(self):
		self.states = []
		
		self.currentState = None

	def addAnimationState(self,name,frames,speed,loop=False):

		state = AnimationController.AnimationState(name,frames,speed,loop)

		self.states.append(state)	
		
	def setState(self,name):
		for state in self.states:
			if state.name == name:
				self.currentState = state
				state.begin()
			else:
				state.active = False


	def getFrame(self):

		if self.currentState != None:
			return self.currentState.getFrame()
		else:
			return self.states[0].getFrame()


	class AnimationState(object):
		'''stores a single set of sprites and properties including speed and if looping'''
		def __init__(self,name,frames,speed,loop):
			self.frames = frames
			self.speed = speed
			self.loop = loop
			self.active = False
			self.name = name

			
			self.stillFrame = len(self.frames) == 1

		def begin(self):
			if self.active == False:
				self.active = True
				self.startTime = time.time()
				
		def getFrame(self):
			if not self.stillFrame:
				if self.loop == True:
					frame = int(((time.time()-self.startTime)/self.speed)%len(self.frames))
				else:
					frame = int((time.time()-self.startTime)/self.speed)
					if frame >= len(self.frames):
						frame = len(self.frames)-1
			else:
				frame = 0
			return self.frames[frame]




		