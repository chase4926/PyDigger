#!/usr/bin/env python

'''
PyDigger: game.py
--------------------------------

Designed around 1280x720 (16:9).
Will adjust automatically to other resolutions without resorting to
scaling.
'''

# System imports
import time, random
# Pygame imports
import pygame
from pygame.locals import *
# Local imports
import cave_generator as cgen
import gameclock


# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()

# Various varibles
FPS = 0 # 0 = Unlimited
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False


class GameWindow:
  def __init__(self):
    # Set up the window
    flags = pygame.DOUBLEBUF
    if FULLSCREEN:
      flags = flags | pygame.FULLSCREEN
    self.displaysurf = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("PyDigger")
    self.clock = gameclock.GameClock(60, FPS)
    # Test
    self.terrain = Terrain()

  def main(self):
    self.running = True
    
    while self.running:
      self.clock.tick()
      if self.clock.update_ready:
        self.update()
      if self.clock.frame_ready:
        self.draw()

  def update(self):
    for event in pygame.event.get():
        if event.type == QUIT:
          self.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.running = False

  def draw(self):
    pygame.display.update()


class Terrain:
  # This class is the cave system that is drawn
  def __init__(self):
    self.width = 80
    self.height = 160
    self.regenerateCave()
    self.cave_surface = pygame.Surface((self.width, self.height))
    self.redrawCaveSurface()

  def redrawCaveSurface(self):
    brown = (100, 49, 12)
    purple = (255, 0, 255)
    # Fill with purple (the transparency color)
    self.cave_surface.fill(purple)
    for y in range(self.height):
      for x in range(self.width):
        if self.cave_gen.land[y][x]:
          self.cave_surface.set_at((x, y), brown)
    self.cave_surface.set_colorkey(purple)

  def regenerateCave(self):
    self.cave_gen = cgen.CaveGenerator(width=self.width,
                                       height=self.height,
                                       angle_deviation=45)
    percents = (75, 50, 25, 10)
    # 150  120  80  40  10
    ranges = (self.height - 10, (self.height/4)+(self.height/2), self.height/2, self.height/4, 10)
    # Generate the cave system with 4 levels of complexity
    for i in range(4):
      self.cave_gen.caves_percent = percents[i]
      self.cave_gen.generateCave(y_range=(ranges[i+1], ranges[i]))
    self.cave_gen.fillInEdges()
    self.cave_gen.save("./cave.txt")

window = GameWindow()
# Start 'er up!
window.main()
# Deconstruct all pygame stuff
pygame.quit()

