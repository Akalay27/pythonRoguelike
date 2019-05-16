import time

class AnimationController(object):
	"""controls the animations"""
	def __init__(self):
		self.states = []
	
	def addAnimationState(self,tilemap,resolution,speed,loop=False)

		


	class AnimationState(object):
		'''stores a single set of sprites and properties including speed and if looping'''
		def __init__(self,sprites,speed,loop):
			self.sprites = sprites
			self.speed = speed
			self.loop = loop
			self.active = False


		def begin(self):
			self.active = True
			self.startTime = time.time()
			self.frame = 0
		def getFrame(self):

			frame = ((time.time()-self.startTime)/self.speed)%len(self.sprites)

			return self.sprites(frame)




		