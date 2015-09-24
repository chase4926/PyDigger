
import random, time

class CaveGenerator:
  def generateCave(self, width=3, height=3):
    # Start with a full land mass
    land = self.createFullLand(width, height, True)
    # Determine amount of caves to carve
    caves = self.determineAmountOfCaves(width*height)
    # Iterate through caves to carve all caves
    for i in range(caves):
      # Determine random spot to start cave
      x = random.sample(range(width), 1)
      y = random.sample(range(height), 1)
    # Return the finished land mass with added caves
    return land

  def createFullLand(self, width, height, fill=None):
    return height*[width * [fill]]

  def determineAmountOfCaves(self, area):
    caves = area / 100.0
    return int(round(caves))

# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# --Debug script--
cave_generator = CaveGenerator()
print cave_generator.generateCave()
