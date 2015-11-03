
"""
ore_cave_generator.py
---------------------

Uses cave_generator.py and the output of ore_file_generator.py and creates ore
fields within it's width and height. These ore fields can then be applied to a
regular cave system to make a ore-filled cave.
"""

import cave_generator as cgen
import yaml


class OreCaveGenerator:
  def __init__(self, width, height, filename):
    self.width = width
    self.height = height
    self.ores_file = filename
    self.loadOresFile()
    self.regenerateCave()
    print width, height

  def __str__(self):
    return str(self.cave_gen)

  def loadOresFile(self):
    with open(self.ores_file, 'r') as f:
      self.ores_dict = yaml.load(f.read())

  def regenerateCave(self):
    self.cave_gen = cgen.CaveGenerator(width=self.width,
                                       height=self.height,
                                       angle_deviation=180,
                                       path_width=(1,2))
    # (Minimum percent for caves, maximmum)
    percent_range = range(20, 60)
    # Determine the minimum and maximum z levels
    minz = self.ores_dict[self.ores_dict.keys()[0]]['z']
    maxz = minz
    for name in self.ores_dict:
      ore = self.ores_dict[name]
      if ore['z'] > maxz:
        maxz = ore['z']
      if ore['z'] < minz:
        minz = ore['z']
    # Loop Through all the types of ores, and generate a cave system for each
    for name in self.ores_dict:
      ore = self.ores_dict[name]
      # Set the empty space (space dug out by gen) to the ore's name
      self.cave_gen.empty = name
      # Set the percent to the ore percent projected onto percent_range
      self.cave_gen.caves_percent = percent_range[int(round( (len(percent_range)-1) * (ore['amount'] / 100.0) ))]
      # Find y_range now based on ore['z']
      y_level = self.height * ((ore['z'] - minz) / float(maxz - minz))
      variation = self.height * 0.05
      y_range = [int(round(y_level-variation)), int(round(y_level+variation))]
      # Shift y_range to be within bounds
      if y_range[0] < 0:
        y_range[1] += -y_range[0]
        y_range[0] = 0
      if y_range[1] > self.height - 1:
        y_range[0] -= (y_range[1] - self.height - 1)
        y_range[1] = self.height - 1
      print name, y_range
      self.cave_gen.generateCave(y_range=y_range)
    self.cave_gen.fillInEdges()
    self.land = self.cave_gen.land


if __name__ == "__main__":
  cave_gen = OreCaveGenerator(width=160, height=62, filename="../ores_test.yaml")
  print cave_gen
