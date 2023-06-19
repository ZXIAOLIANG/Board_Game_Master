# Board_Game_Master
This is the teaching project for the programming basics course in Python
## Overview
This project builds a simple board game launcher which inlcudes a menu screen and two board games (tic-tac-toe and Gomoku).
## Dependencies:
- pygame
## Teaching
The teaching session can be splitted into four parts.
### Part 1: Introduction to pygame
The first part focuses on introducing the pygame package to students by building a menu scene and the tic-tac-toe game logic.

Key points for students:
- pygame basics: fps, display, draw, blit
- how to draw a button using pygame
- game loop (state machine)

### Part 2: Object Oriented Programming
The second part focused on improving the code quality of the first part by split different components to different classes.

Key points for students:
- class
- inheritance
- easier addition of more board games

The game design also integrated some simple model-view-controller (MVC) idea, which can be briefly introduced to students.

**Note**: No new features are added in this part.

### Part 3: Drop down menu 
This part focuses on implementing a drop down menu on the menu scene.

Key points for students:
- more usage of pygame draw functions
- updated game loop (state machine)

### Part 4: Gomoku
This part adds the Gomoku game

Key points for students:
- similarity and difference between tic-tac-toe and Gomoku
- efficient win condition check for Gomoku