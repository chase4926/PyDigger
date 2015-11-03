#!/usr/bin/env python

'''
PyDigger: game.py
--------------------------------

Designed around 1280x720 (16:9).
Will adjust automatically to other resolutions without resorting to
scaling.
'''

# System imports
import time, random, math, os
# Third party libraries
import yaml
# Pygame imports
import pygame
from pygame.locals import *
# Local library imports
from lib_misc import *
from cave_generator.cave_generator import CaveGenerator
from cave_generator.ore_cave_generator import OreCaveGenerator
import lib_medialoader as media
from ore_loader import *
# Local Classes
from terrain_generator import Terrain

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Load images
media.load_images("../images/")

# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()

# Various varibles
TPS = 60 # Ticks per second (DON'T CHANGE THIS!)
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
    self.clock = pygame.time.Clock()
    self.controller = Controller(self)

  def blit(self, surface, coords):
    self.displaysurf.blit(surface, coords)

  def loop(self):
    self.running = True
    
    while self.running:
      # Keep the game running smoothly
      self.clock.tick(TPS)
      # Update the controller
      self.controller.update()
      # Fill with black to get rid of previous blits
      self.displaysurf.fill((0,0,0))
      # Let the controller draw everything
      self.controller.draw()
      # "Flip" the display
      pygame.display.update()


class Controller:
  def __init__(self, window):
    self.window = window
    self.world = World()
    self.mousetooltip = MouseToolTip(self.world)

  def update(self):
    # Key is down (Holding down a key will keep triggering)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_DOWN]:
      self.world.pan(y_offset=4)
    if keys_pressed[pygame.K_UP]:
      self.world.pan(y_offset=-4)
    # Key presses (Holding down a key will only trigger once)
    for event in pygame.event.get():
        if event.type == QUIT:
          self.window.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.window.running = False
          #elif event.key == K_SPACE:
            #print self.mousetooltip.get_current()

  def draw(self):
    # All the draws:
    self.world.draw(self.window)
    # Remove eventually
    self.mousetooltip.draw(self.window)


class MouseToolTip:
  def __init__(self, world):
    self.world = world
    self.terrain = world.terrain
    self.font = pygame.font.Font("freesansbold.ttf", 32)

  def get_current(self):
    mousex, mousey = pygame.mouse.get_pos()
    x = int(round(float(mousex + self.world.terrain_x - 8) / self.terrain.tile_size))
    y = int(round(float(mousey + self.world.terrain_y - 8) / self.terrain.tile_size))
    return self.terrain.get(x, y)

  def draw(self, window):
    text = self.font.render(self.get_current(), True, (255, 255, 255))
    window.blit(text, (32, 32))


class World:
  def __init__(self):
    self.terrain = Terrain()
    self.terrain_x = 0
    self.terrain_y = 0

  def pan(self, x_offset=0, y_offset=0):
    self.terrain_x += x_offset
    self.terrain_y += y_offset

  def draw(self, window):
    window.blit(self.terrain.surface, (-self.terrain_x, -self.terrain_y))




window = GameWindow()
# Start 'er up!
window.loop()
# Deconstruct all pygame stuff
pygame.quit()

