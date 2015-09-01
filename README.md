GameofLife
Harley Vanselow 2015

The main code for this repository can be found in game_of_life_drawing/game_of_life_drawing.py

This application contains a python implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
On launch, the program will open a console and prompt the user to enter an x and y dimension size for the game grid.
Once an appropriate response is received, a canvas will be created with an initial seed. Right clicking the canvas will
start the simulation, while left clicking will place additional seeds. During the simulation left clicking will pause the
program and allow for additional seeds to be placed on the fly.

This program makes use of PPDrawer.py to supply methods and classes that enable game_of_life_drawing.py to spawn
and draw on a canvas. I did not design the majority of the PPDrawer file, but have made additions to it for use in this project.
