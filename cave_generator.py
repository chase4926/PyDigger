
import random, math
from lib_misc import *


class CaveGenerator:
  def __init__(self, width=40, height=80, angle_deviation=60, caves_percent=100):
    self.angle_deviation = angle_deviation
    self.width = width
    self.height = height
    self.area = width * height
    self.caves_percent = caves_percent
    # Start with a full land mass
    self.land = self.createFullLand()

  def __str__(self):
    string = ""
    solid_char="X"
    empty_char=" "
    for layer in self.land:
      for item in layer:
        if item:
          string += solid_char
        else:
          string += empty_char
      string += "\n"
    return string

  def generateCave(self, x_range=None, y_range=None):
    # Determine amount of caves to carve
    caves = self.getAmountOfCaves()
    
    # Iterate through caves to carve all caves
    for i in range(caves):
      # Pick random spot to start cave
      x, y = self.getRandomPoint(x_range, y_range)
      # Determine length of walk based on function of area
      length = self.getLengthOfWalk()
      # Pick a random angle to walk in
      angle = random.randint(0, 359)
      # Get path width list
      path_width = getRandomGradient(length, 3, 5)
      
      for step in range(length):
        # Deviate angle
        angle = self.deviateAngle(angle)
        # Calculate probable x and y coordinates
        next_x = x + offsetX(angle, 1)
        next_y = y + offsetY(angle, 1)
        next_points = self.getPathPoints(next_x, next_y, path_width[step])
        # If the points are out of the wall, deviate angle from wall
        if not self.pointsInBounds(next_points):
          # Pick clockwise or counter clockwise
          mult = random.sample([-1, 1], 1)[0]
          tries = 0
          while not self.pointsInBounds(next_points) and tries < 8:
            tries += 1
            angle = self.deviateAngleFromWall(angle, mult)
            next_x = x + offsetX(angle, 1)
            next_y = y + offsetY(angle, 1)
            next_points = self.getPathPoints(next_x, next_y, path_width[step])
          if tries >= 8:
            break
        # The points are in bounds, we'll keep those coordinates
        x = next_x
        y = next_y
        # Dig the points!
        self.digPoints(self.land, next_points)
    # Return the finished land mass with added caves
    return self

  def pointsInBounds(self, points):
    for point in points:
      if not self.pointInBounds(*point):
        return False
    return True

  def digPoints(self, land, points):
    for point in points:
      x, y = point
      if self.pointInBounds(x, y):
        land[y][x] = False

  def pointInBounds(self, x, y):
    return (x >= 0 and x < self.width) and (y >= 0 and y < self.height)

  def getCornerPoints(self, x, y):
    points = []
    for modx in (-0.5, 0.5):
      for mody in (-0.5, 0.5):
        points.insert(0, (int(round(x + modx)), int(round(y + mody))))
    return points

  def getPathPoints(self, x, y, radius):
    return self.translateRoomPoints(self.getRoomPoints(radius), x, y)

  def translateRoomPoints(self, points, x, y):
    result_points = []
    for point in points:
      ox, oy = point
      result_points.insert(0, (int(round(ox+x)), int(round(oy+y))))
    return result_points

  def getRoomPoints(self, size):
    points = []
    center = float(size) / 2.0
    for y in range(size):
      for x in range(size):
        if distance(x, y, center, center) <= center:
          points.insert(0, (x - int(center), y - int(center)))
    return points

  def deviateAngle(self, angle):
    # Deviates randomly by deviation
    # mult deterines clockwise / counter clockwise
    mult = random.sample([-1, 1], 1)[0]
    return angle + (mult * (random.randint(0, self.angle_deviation)))

  def deviateAngleFromWall(self, angle, mult):
    return angle + (mult * (random.randint(25, 90)))

  def createFullLand(self, fill=True):
    land = []
    for y in range(self.height):
      land.append(self.width * [fill])
    return land

  def fillInEdges(self, land):
    # Makes the edges of land solid
    height = len(land)
    width = len(land[0])
    for y in range(height):
      if y == 0 or y == height - 1:
        for x in range(width):
          land[y][x] = True
      else:
        land[y][0] = True
        land[y][width-1] = True
    return land

  def getRandomPoint(self, x_range=None, y_range=None):
    # Returns a random point in land
    # n_range => (min, max)
    if x_range != None:
      x = random.randint(0, abs(x_range[0] - x_range[1]) - 1) + x_range[0]
    else:
      x = random.randint(0, self.width - 1)
    if y_range != None:
      y = random.randint(0, abs(y_range[0] - y_range[1]) - 1) + y_range[0]
    else:
      y = random.randint(0, self.height - 1)
    return x, y

  def getLandSolidity(self):
    # Returns a float between 0 and 1 representing the percent solid
    # the land is.
    solidity = 0
    for layer in self.land:
      solidity += layer.count(True)
    return float(solidity) / float(self.area)

  def getLengthOfWalk(self):
    # The length of the cave is equal to the percentage of solid mass applied
    # to the square root of the area then divided by 2
    # (square root of area is smaller than longest side)
    solidity = self.getLandSolidity()
    return int(round( (solidity * math.sqrt(self.area)) / 2 ))

  def getAmountOfCaves(self):
    # caves_percent is the percentage of caves to have - 50 = 50%
    caves = float(self.area) / 400.0 # 400.0 gives a really nice amount of caves per land
    # Modify caves to the percent wanted
    caves = caves * (float(self.caves_percent) / 100.0)
    return int(round(caves))


## --Debug script--
#cave_gen = CaveGenerator(width=160, height=62, angle_deviation=60, caves_percent=100)
#print cave_gen.generateCave()
#print cave_gen.getCornerPoints(4, 5)
#print cave_gen.getPathPoints(4, 5, 3) # Default radius is 3!!!
