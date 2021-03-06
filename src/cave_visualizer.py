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
from cave_generator.cave_generator import *


# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()

# Various varibles
FPS = 0 # 0 = Unlimited
COLOR_BLACK = (0, 0, 0)
COLOR_PURPLE = (255, 0, 255)
COLOR_BROWN = (100, 49, 12)
# Cave generator config
WIDTH = 250
HEIGHT = 150
SCALE = 4


class GameWindow:
  def __init__(self):
    # Generate a cave
    # Every day I seem to prefer different settings on this
    self.cave_gen = CaveGenerator(width=WIDTH, height=HEIGHT, angle_deviation=45, caves_percent=75)
    self.cave_gen.generateCave(y_range=(100, 140))
    # Set up the window
    self.displaysurf = pygame.display.set_mode((self.cave_gen.width*SCALE, self.cave_gen.height*SCALE), pygame.DOUBLEBUF)
    pygame.display.set_caption("Cave Visualizer")
    self.clock = pygame.time.Clock()
    # Surface to draw the cave on
    self.cave_surf = pygame.Surface((self.cave_gen.width, self.cave_gen.height))
    # Surface to scale the cave surface on
    self.draw_surf = pygame.Surface((self.cave_gen.width*SCALE, self.cave_gen.height*SCALE))
    # Draw & scale the cave
    self.redraw_cave()

  def paint_cave(self, cave, surface):
    surface.fill(COLOR_BLACK)
    land = cave.land
    for y in range(len(land)):
      for x in range(len(land[y])):
        if land[y][x]:
          surface.set_at((x, y), COLOR_BROWN)
        else:
          surface.set_at((x, y), COLOR_PURPLE)

  def redraw_cave(self):
    # Fill with black to get rid of previous blits
    self.displaysurf.fill(COLOR_BLACK)
    self.paint_cave(self.cave_gen, self.cave_surf)
    pygame.transform.scale(self.cave_surf, (self.cave_gen.width*SCALE, self.cave_gen.height*SCALE), self.draw_surf)
    # Remove background color for transparency
    self.draw_surf.set_colorkey(COLOR_PURPLE)
    self.displaysurf.blit(self.draw_surf, (0, 0))

  def main(self):
    self.running = True
    
    while self.running:
      self.clock.tick(60)
      #if self.clock.update_ready:
      self.update()
      #if self.clock.frame_ready:
      self.draw()
      pygame.display.update()

  def update(self):
    for event in pygame.event.get():
        if event.type == QUIT:
          self.running = False
        if event.type == KEYDOWN:
          if event.key == K_SPACE:
            print("Generating new cave...")
            self.cave_gen.caves_percent = 25
            self.cave_gen.generateCave(y_range=(10, 100))
            self.redraw_cave()

  def draw(self):
    pass


window = GameWindow()
# Start 'er up!
window.main()
# Deconstruct all pygame stuff
pygame.quit()

