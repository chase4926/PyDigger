#PyDigger#

A remake of one of my older ideas for a 2d, side-view mining game.


This is a very rough draft design document, if it isn't grammatically correct,
that's to be expected.

---

Player is a robot
Robot digs useless and useful materials in self-dug and natural caves


###Part 1. The natural cave generator.###

+ Start with a land of size width, height (Possibly already has caves)
+ Determine amount of caves based on area of land (width x height)
+ Iterate through caves
  + Pick a random spot in the land
  + Determine length of walk based on solidity of cave, up to a maximum based on area
  + Walk away from that spot in a random angle, and deviate slighty randomly
    + If a wall is hit, pick rotation and adjust angle 45-90 degrees until aiming away from wall
    + As walking, excavate all around randomly
    + Very occasionally, randomly make a small cavern around current location
      + Room diameter dependant on path diameter, currently path diameter is statics
+ Return finished land with caves

###Part 2. The Visualizer.###

+ Create a visualizer to visualize the caves, to make sure the generator doesn't need immediate tweaking
+ This can either be graphical, or it can output to a file or terminal

File and terminal have the inherant flaw that the text is taller than it is wide,
we don't want this, as pixels in this model are square.

If going the graphical route:
+ Add graphics - currently uses solid color
+ Perhaps adapt the graphics engine running the cave viewer to be the game engine

###Part 3. The Game.###

#Tech#

Runs on my cheap laptop almost as good as on my desktop.
Everyone should be able to run this on thier computer.
Low enough default resolution to accomodate this.
Moddable
Use as few outside libraries as possible. As much for practice as anything else.

---

#Design#

Have to dig rare ores towards some goal
Use ores to build defenses on surface (ores can be used in raw form, ore processing is boring)
Defend against something (wildlife)
Have to dig strategically to be able to climb back out
Probably won't be major upgrades like jetpack etc. later to make this negligable

Surface is like tower defense -lite-
Not much strategy in tower placement, more on purchasing and mining
Move to different locations after all waves of enemies are defeated
Different locations have differently structured cave systems.


