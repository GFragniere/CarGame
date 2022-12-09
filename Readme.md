# A simple car game

This is a semi interactive game multi-user game

## Installation
To install everything, you'll need to run `pip install -r requirements.txt` in the terminal console.

## How it works
As of right now, it is a small single player game, but I will add the possibility to play with multiple different 
players, as well as a small AI that you can play against.

## Interface
When you launch the program, you'll have a window that pops up, showing you the base map of the game. Once you want
to move, you can use a key on the numpad in order to make one of the following move:

    5: Keep the same speed
    6: Accelerate to the right
    2: Accelerate downwards
    4: Accelerate to the left
    8: Accelerate upwards
    9: Accelerate up-right
    3: Accelerate down-right
    1: Accelerate down-left
    7: Accelerate up-left

In order to know where you'll end up on your next move, there is a small colored square that indicates you where you'll
end up if you keep the same speed. Every player has its own color, making it easier to see where everyone is and will go.

You can also decide whether you would like to have a collision assisting tool or not by pressing the `h` key during your turn.
There will then be a small white-ish square in the top right of the screen to indicate you that the help is enabled (note that the help is enabled by default).
The collision assisting tool will warn you if you are about to crash or run out of course by displaying a "warning sign" on the top left of the screen, indicating you that you should be careful on what move you decide to make next.
By pressing `h`, it will be deactivated until the `h` key is pressed again, allowing each player to decide if they want to have help or not.


## Goal
The objective of the game is to reach the finish line (white squares at the bottom left part of the screen) without 
colliding with another player, with a wall (in brown color) or going out of the course (screen). The road is represented by the grey colored square.

