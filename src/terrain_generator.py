

import pygame
from ore_loader import *
from cave_generator.cave_generator import *
from cave_generator.ore_cave_generator import *
import lib_medialoader as media


class Terrain:
  # This class is the cave system that is drawn
  def __init__(self):
    # Various Variables
    self.width = 80
    self.height = 160
    #self.x = 0
    #self.y = 0
    self.tile_size = 16
    self.ores_file = "../ores_test.yaml"
    self.ores = Ores(self.ores_file)
    # Cave generation
    self.regenerateCave()
    # Surfaces
    self.dirt_image = media.get("dirt.png")
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

  def getPixelWidth(self):
    return self.width * self.tile_size

  def getPixelHeight(self):
    return self.height * self.tile_size

  def getPixelSize(self):
    return (self.getPixelWidth(), self.getPixelHeight())

  def drawBackground(self):
    background_image = media.get("cave_background.png")
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

