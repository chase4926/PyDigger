#PyDigger#

A remake of one of my older ideas for a 2d, side-view mining game.

This is a very rough draft design document, if it isn't grammatically correct,
that's to be expected.

---


###Ore dispersal###

+ Use a public resource on Earth's ores and pull data from it to create yaml file
+ Convert the yaml file to something game-ready
+ Use CaveGenerator to make ore veins
  + Start with the common veins
  + The later veins overwrite the previous; but they're rarer so it's not as common
+ Lay ore veins onto the walls of the generated cave system.


Perhaps restrict the number of ores per level? Or permanently?


###The Game###

####Tech####

+ Runs on my cheap laptop almost as good as on my desktop.
+ Everyone should be able to run this on their computer.
+ Low enough default resolution to accommodate this.
+ Moddable
+ Use as few outside libraries as possible. As much for practice as anything else.


####Design####

+ Player controls subterranean robot from surface
+ Have to dig rare ores towards some goal
+ Use ores to build defenses on surface (ores can be used in raw form, ore processing is boring)
+ Defend against something (wildlife)
+ Have to dig strategically to be able to climb back out
+ Probably won't be major upgrades like jetpack etc. later to make this negligible

Surface is like tower defense -lite-
Not much strategy in tower placement, more on purchasing and mining
Move to different locations after all waves of enemies are defeated
Different locations have differently structured cave systems.

