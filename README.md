#PyDigger#

A remake of one of my older ideas for a 2d, side-view mining game.


Player is a robot
Robot digs useless and useful materials in self-dug and natural caves


###Step 1. The natural cave generator.###

+ Create full (solid rock) land of size width, height
+ Determine amount of caves based on area of land (width x height)
+ Iterate through caves
  + Pick a random spot in the land
  + Determine length of walk based on solidity of cave, up to a maximum based on area
  + Walk away from that spot in a random angle, and deviate slighty randomly
    + If a wall is hit, pick rotation and adjust angle 45-90 degrees until aiming away from wall
    + As walking, excavate all around randomly
    + Very occasionally, randomly make a small cavern around current location
      + Determine room diameter based on area of cave
+ Return finished land with caves


###Step 2. The Visualizer.###

+ Create a visualizer to visualize the caves, to make sure the generator doesn't need immediate tweaking
+ This can either be graphical, or it can output to a file

If going the file route:
+ Output to a file with the rock being 'X', and the empty space being ' '
+ View in mono font

If going the graphical route:
+ Perhaps adapt the graphics engine running the cave viewer to be the game engine
