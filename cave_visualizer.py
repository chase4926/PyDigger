#!/usr/bin/env python

'''
Visualizer for cave_generator.py
--------------------------------

SPACE : Generate new cave system

Use the normal close button "X" to close the program.
'''

# System imports
import time, random
# Pygame imports
import pygame
from pygame.locals import *
# Local imports
import cave_generator as cgen


# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()
COLOR_BLACK = (0, 0, 0)
COLOR_BROWN = (100, 49, 12)
SCALE = 8


def draw_cave(surface, cave):
  land = cave.land
  for y in range(len(land)):
    for x in range(len(land[y])):
      if land[y][x]:
        surface.set_at((x, y), COLOR_BROWN)
      else:
        surface.set_at((x, y), COLOR_BLACK)

def main():
  # Generate a cave
  cave_gen = cgen.CaveGenerator(width=160, height=100, angle_deviation=60, caves_percent=100)
  cave_gen.generateCave()
  # Set up the window
  displaysurf = pygame.display.set_mode((cave_gen.width*SCALE, cave_gen.height*SCALE), pygame.DOUBLEBUF)
  pygame.display.set_caption("Cave Visualizer")
  # Surface to draw the cave on
  cave_surf = pygame.Surface((cave_gen.width, cave_gen.height))
  # Surface to scale the cave surface on
  draw_surf = pygame.Surface((cave_gen.width*SCALE, cave_gen.height*SCALE))
  # Draw & scale the cave
  draw_cave(cave_surf, cave_gen)
  pygame.transform.scale(cave_surf, (cave_gen.width*SCALE, cave_gen.height*SCALE), draw_surf)
  # Blit cave drawing
  displaysurf.blit(draw_surf, (0, 0))
  
  running = True
  
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      if event.type == KEYDOWN:
        if event.key == K_SPACE:
          print "Generating new cave..."
          cave_gen.generateCave()
          draw_cave(cave_surf, cave_gen)
          pygame.transform.scale(cave_surf, (cave_gen.width*SCALE, cave_gen.height*SCALE), draw_surf)
          displaysurf.blit(draw_surf, (0, 0))
    pygame.display.update()


# Start 'er up!
main()
# Deconstruct all pygame stuff
pygame.quit()

