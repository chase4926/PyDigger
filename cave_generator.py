
import random, math


def distance(x1, y1, x2, y2):
  return math.sqrt( ((float(x2) - float(x1)) ** 2) + ((float(y2) - float(y1)) ** 2) )

def offsetX(angle, radius):
  return math.sin((float(angle) / 180) * math.pi) * float(radius)

def offsetY(angle, radius):
  return -1 * math.cos((float(angle) / 180) * math.pi) * float(radius)


class CaveGenerator:
  def __init__(self, width=40, height=80, angle_deviation=60, caves_percent=100):
    self.angle_deviation = angle_deviation
    self.width = width
    self.height = height
    self.caves_percent = caves_percent
    self.land = []

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

  def generateCave(self):
    # Start with a full land mass
    self.land = self.createFullLand(self.width, self.height, True)
    # Determine amount of caves to carve
    caves = self.determineAmountOfCaves(self.width * self.height, self.caves_percent)
    # Determine size of rooms
    room_size = self.determineRoomSize(self.land)
    
    # Iterate through caves to carve all caves
    for i in range(caves):
      # Pick random spot to start cave
      x = random.sample(range(self.width), 1)[0]
      y = random.sample(range(self.height), 1)[0]
      # Determine length of walk based on function of area
      length = self.determineLengthOfWalk(self.land)
      # Pick a random angle to walk in
      angle = random.sample(range(360), 1)[0]
      # Boolean representing whether a room was made yet or not
      # ONLY 1 room/cave (hopefully this works well)
      room_made = False
      
      for step in range(length):
        # Deviate angle
        angle = self.deviateAngle(angle, self.angle_deviation)
        # Calculate probable x and y coordinates
        next_x = x + offsetX(angle, 1)
        next_y = y + offsetY(angle, 1)
        next_cornerpoints = self.getCornerPoints(next_x, next_y)
        # If the corner points are out of the wall, deviate angle from wall
        if not self.cornerPointsInBounds(next_cornerpoints):
          # Pick clockwise or counter clockwise
          mult = random.sample([-1, 1], 1)[0]
          while not self.cornerPointsInBounds(next_cornerpoints):
            angle = self.deviateAngleFromWall(angle, mult)
            next_x = x + offsetX(angle, 1)
            next_y = y + offsetY(angle, 1)
            next_cornerpoints = self.getCornerPoints(next_x, next_y)
        # The corner points are all in bounds, we'll keep those coordinates
        #print angle
        x = next_x
        y = next_y
        # Dig the corner points!
        self.digPoints(self.land, next_cornerpoints)
        # See whether we want a room or not
        if not room_made and self.roomWanted(self.land):
          room_made = True
          room_points = self.getRoomPoints(room_size)
          self.digPoints(self.land, self.translateRoomPoints(room_points, x, y))
    # Return the finished land mass with added caves
    return self

  def cornerPointsInBounds(self, corner_points):
    return (self.pointInBounds(*corner_points[0]) and
           self.pointInBounds(*corner_points[1]) and
           self.pointInBounds(*corner_points[2]) and
           self.pointInBounds(*corner_points[3]))

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

  def deviateAngle(self, angle, deviation=40):
    # Deviates randomly by deviation
    # mult deterines clockwise / counter clockwise
    mult = random.sample([-1, 1], 1)[0]
    return angle + (mult * (random.sample(range(deviation), 1)[0]))

  def deviateAngleFromWall(self, angle, mult):
    return angle + (mult * (random.sample(range(45), 1)[0]))

  def createFullLand(self, width, height, fill=None):
    #land = height*[width * [fill]]
    land = []
    for y in range(height):
      land.append(width * [fill])
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

  def getLandArea(self, land):
    return len(land) * len(land[0])

  def getLandSolidity(self, land):
    # Returns a float between 0 and 1 representing the percent solid
    # the land is.
    solidity = 0
    for layer in land:
      solidity += layer.count(True)
    return float(solidity) / float(self.getLandArea(land))

  def roomWanted(self, land, percent=75):
    # This returns True or False
    # True = Make a room
    # First the land needs to be over percent% solid
    solidity = self.getLandSolidity(land)
    if solidity > (float(percent) / 100.0):
      # Now that we know a room could "fit", we need to randomly decide
      if random.sample(range(self.determineLengthOfWalk(land) * 2), 1)[0] == 0:
        return True
      else:
        return False
    else:
      return False

  def determineRoomSize(self, land):
    # This should really just be a static number if the path width is static
    # If the walk path ever excavates more than 1 around it, change this to an equation
    #area = self.getLandArea(land)
    #return int(round( math.sqrt(area) / 10.0 ))
    return 9

  def determineLengthOfWalk(self, land):
    solidity = self.getLandSolidity(land)
    area = self.getLandArea(land)
    # The length of the cave is equal to the percentage of solid mass applied
    # to the square root of the area then divided by 2
    # (square root of area is smaller than longest side)
    length = int(round( (solidity * math.sqrt(area)) / 2 ))
    return length

  def determineAmountOfCaves(self, area, caves_percent=100):
    # caves_percent is the percentage of caves to have - 50 = 50%
    caves = float(area) / 400.0 # 400.0 gives a really nice amount of caves per land
    # Modify caves to the percent wanted
    caves = caves * (float(caves_percent) / 100.0)
    return int(round(caves))


## --Debug script--
#cave_generator = CaveGenerator(width=160, height=62, angle_deviation=60, caves_percent=100)
#print cave_generator.generateCave()
