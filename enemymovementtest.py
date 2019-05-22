import pygame
import math
pos = [300,300]

size = width,height = (600,600)

screen = pygame.display.set_mode(size)
t = 0
while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()			
	mousePos = pygame.mouse.get_pos()

	pygame.draw.rect(screen,(255,0,0),(pos[0],pos[1],10,10))

	difference = mousePos[0]-pos[0],mousePos[1]-pos[1]
	angle = math.atan2(difference[1], difference[0])

	pos[0]+=math.cos(angle)*1*(math.sin(t)+1)/5
	pos[1]+=math.sin(angle)*1*(math.sin(t)+1)/5
	pygame.display.flip()


