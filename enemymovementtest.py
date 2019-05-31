import pygame
import math
from main import Game
pos = [300,300]


screen = game.screen


mousePos = pygame.mouse.get_pos()

pygame.draw.rect(screen,(255,0,0),(pos[0],pos[1],10,10))

difference = mousePos[0]-pos[0],mousePos[1]-pos[1]
angle = math.atan2(difference[1], difference[0])

pos[0]+=math.cos(angle)
pos[1]+=math.sin(angle)



