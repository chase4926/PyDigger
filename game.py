#!/usr/bin/env python

'''
PyDigger: game.py
--------------------------------

Designed around 1280x720 (16:9).
Will adjust automatically to other resolutions without resorting to
scaling.
'''

# System imports
import time, random, math
# Third party libraries
import yaml
# Pygame imports
import pygame
from pygame.locals import *
# Local imports
import cave_generator as cgen
import lib_medialoader as media

# Load images
media.load_images("./images")

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
    
    # Test
    self.terrain = Terrain()

  def blit(self, surface, coords):
    self.displaysurf.blit(surface, coords)

  def main(self):
    self.running = True
    
    while self.running:
      self.clock.tick(TPS)
      self.update()
      self.draw()

  def update(self):
    # Key is down (Holding down a key will keep triggering)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_DOWN]:
      self.terrain.pan(y_offset=4)
    if keys_pressed[pygame.K_UP]:
      self.terrain.pan(y_offset=-4)
    # Key presses (Holding down a key will only trigger once)
    for event in pygame.event.get():
        if event.type == QUIT:
          self.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.running = False

  def draw(self):
    # Fill with black to get rid of previous blits
    self.displaysurf.fill((0,0,0))
    # Now all the draws:
    self.terrain.draw(self)
    # "Flip" the display
    pygame.display.update()


class Ores:
  def __init__(self, filename):
    self.filename = filename
    self.load_ores_file()
    # Surfaces
    # For each entry in self.ores_array add ['image'] keys and corresponding surfs

  def generate_ore_surfs(self):
    ore_image = media.get("./images/ore.png")
    for ore in self.ores_array:
      print ore['name']

  def load_ores_file(self):
    with open(self.filename, 'r') as f:
      self.ores_array = yaml.load(f.read())

  def get_random_color(self):
    return (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))


class Terrain:
  # This class is the cave system that is drawn
  def __init__(self):
    # Various Variables
    self.width = 80
    self.height = 160
    self.x = 0
    self.y = 0
    self.tile_size = 16
    self.regenerateCave()
    self.ores = Ores("ores.yaml")
    # Surfaces
    self.dirt_image = media.get("./images/dirt.png")
    self.surface = pygame.Surface(self.getPixelSize())
    self.cave_surface = pygame.Surface(self.getPixelSize())
    self.background_surface = self.drawBackground(media.get("./images/cave_background.png"))
    self.redrawSurface()

  def pan(self, x_offset=0, y_offset=0):
    self.x += x_offset
    self.y += y_offset

  def getPixelWidth(self):
    return self.width * self.tile_size

  def getPixelHeight(self):
    return self.height * self.tile_size

  def getPixelSize(self):
    return (self.getPixelWidth(), self.getPixelHeight())

  def drawBackground(self, background_image):
    result = pygame.Surface(self.getPixelSize())
    for y in range( int(math.ceil(float(result.get_height()) / background_image.get_height())) ):
      for x in range( int(math.ceil(float(result.get_width()) / background_image.get_width())) ):
        result.blit(background_image, (x*background_image.get_width(), y*background_image.get_height()))
    return result

  def redrawCaveSurface(self):
    brown = (100, 49, 12)
    purple = (255, 0, 255)
    # Fill with purple (the transparency color)
    self.cave_surface.fill(purple)
    for y in range(self.height):
      for x in range(self.width):
        if self.cave_gen.land[y][x]:
          self.cave_surface.blit(self.dirt_image, (x*16, y*16))
    self.cave_surface.set_colorkey(purple)

  def redrawSurface(self):
    self.redrawCaveSurface()
    self.surface.blit(self.background_surface, (0, 0))
    self.surface.blit(self.cave_surface, (0, 0))
    # REMOVE ME!!!---
    #image = media.get("./images/ore.png")
    #image.fill((255, 0, 0), None, pygame.BLEND_RGBA_MULT)
    #self.surface.blit(image, (0,0))
    # ---

  def regenerateCave(self):
    self.cave_gen = cgen.CaveGenerator(width=self.width,
                                       height=self.height,
                                       angle_deviation=45)
    percents = (100, 75, 50, 25)
    # 150  120  80  40  10
    ranges = (self.height - 10, (self.height/4)+(self.height/2), self.height/2, self.height/4, 10)
    # Generate the cave system with 4 levels of complexity
    for i in range(4):
      self.cave_gen.caves_percent = percents[i]
      self.cave_gen.generateCave(y_range=(ranges[i+1], ranges[i]))
    self.cave_gen.fillInEdges()

  def draw(self, window):
    window.blit(self.surface, (-self.x, -self.y))

window = GameWindow()
# Start 'er up!
window.main()
# Deconstruct all pygame stuff
pygame.quit()

