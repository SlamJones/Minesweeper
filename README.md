# Minesweeper
A simple graphical minesweeper game

Based on the game as found in most Windows systems
(Or at least it used to be!)

Player is presented with a grid of clickable buttons.
Several of the buttons on the grid are "mined," to
represent landmines.  If user clicks on a mine, then
they achieve the Failure condition.

The objective is to click all the un-mined buttons, so
as to leave only the mines undistrubed on the grid.  
If the user does so, then they achieve the Victory 
condition.

If the player clicks on a button that has no adjacent 
mines, then all other buttons with no adjacent mines 
will be revealed.  This often leads to a large portion 
of the grid to be revealed early in the game.

Achieving either condition will present an info box 
informing the user of the achieved condition.  The
user is then returned to the main menu.

There are three difficulty settings: Easy, Medium, Hard
Easy: 8 x 8 grid (64 buttons) with 8 mines
Medium: 12 x 12 grid (144 buttons) with 12 mines
Hard: 16 x 16 grid (256 buttons) with 16 mines
