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

You can also decide whether you would like to have a collision assisting tool or not by pressing the `h` key during your turn. There will then be a small white-ish square in the top left of the screen to indicate you that the help is enabled (note that the help is enabled by default).


## Goal
The objective of the game is to reach the finish line (white squares at the bottom left part of the screen) without 
colliding with another player or with a wall (in brown color). The road is represented by the grey colored square.

The game is coded in a way that you technically can't make a move that would lead you to lose (i.e. accelerating
and making you automatically lose, because you'd have too much speed to stop before a wall). If you have to slow down/change direction, you'll see a small "attention" sign on the top
left part of the screen, alerting you that you must change direction, and fast.

Note that if a player cannot make a move to save himself (i.e. 2 other players corner him), he will be forced out of the game, and will be unable to continue playing, letting the others play for blood.



