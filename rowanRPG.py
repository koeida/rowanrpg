import random
import copy
import hm
import libtcodpy as libtcod

from globals import *
from misc import *
from display import *
from map import *
from creatures import *
from input import *

def testArea():
    game_map = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,3,3,3,3,3,3,3,3,0],
        [0,0,0,0,0,0,0,0,0,0]]
    player = Creature(x=4, y=4, direction=0, c="@", id=0,
                      movementFunc=nullMotion, kind="player",
                      blockMove=True, target=None, hp=50)  

    return Area(game_map,[player,makeSquirrel(2,2,1),
                makeSquirrel(2,3,2),makeBear(3,3,3)])

def main():
    global ticks
    
    currentArea = testArea()
    initDisplay()

    message("Welcome to RowanRPG!",libtcod.red)
    while not libtcod.console_is_window_closed():
        ticks += 1
        key = libtcod.console_check_for_keypress(True)
        if(key.vk != libtcod.KEY_NONE):
            shouldQuit,currentArea = handle_keys(key,currentArea)
            if shouldQuit:
                break
            for e in currentArea.entities:
                currentArea.map[e.y][e.x].changed = True
            currentArea.entities = map(lambda e: moveEntity(e,currentArea),currentArea.entities)

        #render the screen
        display(currentArea)

main()