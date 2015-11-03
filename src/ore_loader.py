
"""
ore_loader.py
-------------
Generates a surface for each of the ores located in filename.
"""


import yaml
import pygame
import lib_medialoader as media
from lib_misc import getRandomColor


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
    ore_image = media.get("ore.png")
    for name in self.ores_dict:
      new_ore = ore_image.copy()
      new_ore.fill(getRandomColor(), None, pygame.BLEND_RGBA_MULT)
      self.ores_dict[name]['image'] = new_ore

  def loadOresFile(self):
    with open(self.filename, 'r') as f:
      self.ores_dict = yaml.load(f.read())

