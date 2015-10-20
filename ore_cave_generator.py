

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
      self.ores_array = yaml.load(f.read())

  def regenerateCave(self):
    self.cave_gen = cgen.CaveGenerator(width=self.width,
                                       height=self.height,
                                       angle_deviation=180,
                                       path_width=(1,2))
    percent_range = range(6, 21)
    
    for ore in self.ores_array:
      self.cave_gen.empty = ore['name']
      self.cave_gen.caves_percent = percent_range[int(round( (len(percent_range)-1) * (ore['amount'] / 100.0) ))]
      # Above works correctly, just need to find y_range now
    
    #ranges = (self.height - 10, (self.height/4)+(self.height/2), self.height/2, self.height/4, 10)
    ## Generate the cave system with 4 levels of complexity
    #for i in range(4):
      #self.cave_gen.caves_percent = percents[i]
      #self.cave_gen.generateCave(y_range=(ranges[i+1], ranges[i]))
    #self.cave_gen.fillInEdges()

if __name__ == "__main__":
  cave_gen = OreCaveGenerator(width=160, height=62, ores_file="ores_test.yaml")
  #print cave_gen.cave_gen
