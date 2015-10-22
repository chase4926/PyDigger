

import cave_generator as cgen
import yaml


class OreCaveGenerator:
  def __init__(self, width, height, ores_file):
    self.width = width
    self.height = height
    self.ores_file = ores_file
    self.load_ores_file()
    self.regenerateCave()

  def load_ores_file(self):
    with open(self.ores_file, 'r') as f:
      self.ores_dict = yaml.load(f.read())

  def regenerateCave(self):
    self.cave_gen = cgen.CaveGenerator(width=self.width,
                                       height=self.height,
                                       angle_deviation=180,
                                       path_width=(1,2))
    # (Minimum percent for caves, maximmum)
    percent_range = range(20, 40)
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
      print (ore['amount'] / 100.0)
      self.cave_gen.caves_percent = percent_range[int(round( (len(percent_range)-1) * (ore['amount'] / 100.0) ))]
      # Find y_range now based on ore['z']
      y_level = self.height * ((ore['z'] - minz) / float(maxz - minz))
      variation = self.height * 0.05
      range_y = [int(round(y_level-variation)), int(round(y_level+variation))]
      if range_y[0] < 0:
        range_y[1] += -range_y[0]
        range_y[0] = 0
      if range_y[1] > self.height - 1:
        range_y[0] -= (range_y[1] - self.height - 1)
        range_y[1] = self.height - 1
      self.cave_gen.generateCave(y_range=(range_y[0], range_y[1]))
    self.cave_gen.fillInEdges()

if __name__ == "__main__":
  cave_gen = OreCaveGenerator(width=160, height=62, ores_file="ores_test.yaml")
  print cave_gen.cave_gen
