import copy
import hm
import libtcodpy as libtcod
import random

from creatures import *
from display import *
from globals import *
from input import *
from map import *
from misc import *

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

    return newArea(game_map,[player,makeSquirrel(2,2,1),
                makeSquirrel(2,3,2)])

def main():
    global GameGlobals

    currentArea = testArea()
    initDisplay()

    message("Welcome to RowanRPG!",libtcod.red)
    while not libtcod.console_is_window_closed():
        GameGlobals.ticks += 1
        key = libtcod.console_check_for_keypress(True)
        if(key.vk != libtcod.KEY_NONE):
            shouldQuit,currentArea = handle_keys(key,currentArea)
            if shouldQuit:
                break
            for e in currentArea.entities:
                currentArea.map[e.y][e.x] = currentArea.map[e.y][e.x]._replace(changed = True)
            currentArea = currentArea._replace(entities=map(lambda e: moveEntity(e,currentArea),currentArea.entities))

        #render the screen
        display(currentArea)

main()