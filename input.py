import libtcodpy as libtcod
from copy import *
from globals import *
from map import *

def handle_keys(key,currentArea):
    shouldQuit = False
    currentArea = copy.deepcopy(currentArea)
    p = currentArea.entities[0]

    if key.vk == libtcod.KEY_ESCAPE:
        shouldQuit = True #exit game
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    newX = p.x
    newY = p.y
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        newY -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        newY += 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        newX -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        newX += 1
    else:
        k = chr(key.c)        

    if not bump(newX,newY,p.id,currentArea):
        currentArea.map[p.y][p.x] = currentArea.map[p.y][p.x]._replace(changed = True)
        currentArea.entities[0] = p._replace(x = newX,y = newY)

    return [shouldQuit,currentArea]