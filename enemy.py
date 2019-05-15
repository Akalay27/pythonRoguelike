from Entity import Entity
class Enemy(Entity):
	"""docstring for Enemy"""
	def __init__(self, x, y, health, damage):
		super(Enemy, self).__init__()
		self.x = x
		self.y = y
		self.damage = damage
		self.health = health

