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
from lib_misc import *
from cave_generator import CaveGenerator
from ore_cave_generator import OreCaveGenerator
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
    self.terrain = Terrain()
    self.mousetooltip = MouseToolTip(self.terrain)

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
          self.window.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.window.running = False
          #elif event.key == K_SPACE:
            #print self.mousetooltip.get_current()

  def draw(self):
    # All the draws:
    self.terrain.draw(self.window)
    # Remove eventually
    self.mousetooltip.draw(self.window)


class MouseToolTip:
  def __init__(self, terrain):
    self.terrain = terrain
    self.font = pygame.font.Font("freesansbold.ttf", 32)

  def get_current(self):
    mousex, mousey = pygame.mouse.get_pos()
    x = int(round(float(mousex + self.terrain.x - 8) / self.terrain.tile_size))
    y = int(round(float(mousey + self.terrain.y - 8) / self.terrain.tile_size))
    #return str(x) + " , " + str(y)
    return self.terrain.get(x, y)

  def draw(self, window):
    text = self.font.render(self.get_current(), True, (255, 255, 255))
    window.blit(text, (32, 32))


class Ores:
  def __init__(self, filename):
    self.filename = filename
    self.loadOresFile()
    # Surfaces
    # For each entry in self.ores_array add ['image'] keys and corresponding surfs
    self.generateOreSurfs()

  def get(self, key):
    return self.ores_dict[key]

  def generateOreSurfs(self):
    ore_image = media.get("./images/ore.png")
    for name in self.ores_dict:
      new_ore = ore_image.copy()
      new_ore.fill(getRandomColor(), None, pygame.BLEND_RGBA_MULT)
      self.ores_dict[name]['image'] = new_ore

  def loadOresFile(self):
    with open(self.filename, 'r') as f:
      self.ores_dict = yaml.load(f.read())


class Terrain:
  # This class is the cave system that is drawn
  def __init__(self):
    # Various Variables
    self.width = 80
    self.height = 160
    self.x = 0
    self.y = 0
    self.tile_size = 16
    self.ores_file = "ores_test.yaml"
    self.ores = Ores(self.ores_file)
    # Cave generation
    self.regenerateCave()
    # Surfaces
    self.dirt_image = media.get("./images/dirt.png")
    self.surface = pygame.Surface(self.getPixelSize())
    self.cave_surface = pygame.Surface(self.getPixelSize())
    self.background_surface = self.drawBackground()
    self.redrawSurface()

  def get(self, x, y):
    if self.cave_gen.pointInBounds(x, y):
      material = self.land[y][x]
      if material == False:
        return "air"
      elif material == True:
        return "dirt"
      else:
        return material
    else:
      return "void"

  def pan(self, x_offset=0, y_offset=0):
    # In the future this class will _NOT_ control where it's surface is drawn.
    self.x += x_offset
    self.y += y_offset

  def getPixelWidth(self):
    return self.width * self.tile_size

  def getPixelHeight(self):
    return self.height * self.tile_size

  def getPixelSize(self):
    return (self.getPixelWidth(), self.getPixelHeight())

  def drawBackground(self):
    background_image = media.get("./images/cave_background.png")
    result = pygame.Surface(self.getPixelSize())
    for y in range( int(math.ceil(float(result.get_height()) / background_image.get_height())) ):
      for x in range( int(math.ceil(float(result.get_width()) / background_image.get_width())) ):
        result.blit(background_image, (x*background_image.get_width(), y*background_image.get_height()))
    return result

  def redrawCaveSurface(self):
    purple = (255, 0, 255)
    # Fill with purple (the transparency color)
    self.cave_surface.fill(purple)
    for y in range(self.height):
      for x in range(self.width):
        if self.land[y][x] != False:
          # Not air, so there's something to draw
          # First draw the ground
          self.cave_surface.blit(self.dirt_image, (x*16, y*16))
          if self.land[y][x] != True:
            # Ore here!
            self.cave_surface.blit(self.ores.get(self.land[y][x])['image'], (x*16, y*16))
    self.cave_surface.set_colorkey(purple)

  def redrawSurface(self):
    self.redrawCaveSurface()
    self.surface.blit(self.background_surface, (0, 0))
    self.surface.blit(self.cave_surface, (0, 0))

  def regenerateCave(self):
    # - First generate regular cave system
    self.cave_gen = CaveGenerator(width=self.width,
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
    # - Next generate the ore fields
    self.ore_gen = OreCaveGenerator(width=self.width,
                                    height=self.height,
                                    filename=self.ores_file)
    # - Finally fill out the land variable with appropriate values
    self.land = []
    for y in range(self.height):
      layer = []
      for x in range(self.width):
        if self.cave_gen.land[y][x]:
          # This is the wall of the cave
          material = self.ore_gen.land[y][x]
          if material != True:
            # Ore is here, let's use it
            layer.append(material)
          else:
            # No ore here, just ground
            layer.append(True)
        else:
          # Empty air
          layer.append(False)
      self.land.append(layer)

  def draw(self, window):
    window.blit(self.surface, (-self.x, -self.y))

window = GameWindow()
# Start 'er up!
window.loop()
# Deconstruct all pygame stuff
pygame.quit()

