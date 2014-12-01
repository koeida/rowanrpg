import copy
import libtcodpy as libtcod
import operator
import random

from collections import namedtuple
from globals import *
from misc import *

Tile = namedtuple('Tile',['c','fg','bg','ontick','animRate','changed','walkable','animated'])
Area = namedtuple('Area',['entities','map'])

def tickTile(tile,ticks):
    if tile.animated and (ticks % tile.animRate) == 0:
        tile = tile.ontick(tile)
        return tile._replace(changed=True)
    else:
        return tile

def newTile(c,fg,bg,walkable=True):
    return Tile(c=c, fg = fg, bg = bg, ontick = lambda s: None,animRate = 200,
                changed = True, walkable = walkable, animated = False)

def shimmerFunc(tile):
    return lambda t: shimmer(t,[tile.bg.r,tile.bg.g,tile.bg.b],[10,10,20])

def newArea(newMap,entities):
    m = copy.deepcopy(newMap)
    color_hill          = libtcod.Color(102,204,0)
    color_low_ground    = libtcod.Color(51,102,0)
    color_med_ground    = libtcod.Color(76,153,0)
    color_shore         = libtcod.Color(123,154,0)
    color_shallow_water = libtcod.Color(105, 161, 255)
    color_deep_water    = libtcod.Color(25,90,206)
    tiles = {
        5:newTile(" ",libtcod.white,color_hill),
        4:newTile(" ",libtcod.white,color_med_ground),
        3:newTile(" ",libtcod.white,color_low_ground),
        2:newTile(" ",libtcod.white,color_shore),
        1:newTile(" ",libtcod.white,color_shallow_water),
        0:newTile(" ",libtcod.white,color_deep_water,False)}
    tiles[0] = tiles[0]._replace(ontick=shimmerFunc(tiles[0]),animated=True)
    tiles[1] = tiles[1]._replace(ontick=shimmerFunc(tiles[1]),animated=True)

    m = map2d(lambda e: copy\
                        .deepcopy(tiles[e])\
                        ._replace(animRate=random.randint(50,200)),m)
    return Area(map = m,entities = entities)

def bump(x,y,id,area):
    return (not area.map[y][x].walkable or 
            thingInTheWay(area.entities,x,y,id) or 
            isOffscreen(x,y,area.map))

def getEntitiesIn(cx,cy,ex,ey,a):
    results = []
    for y in range(cy,ey + 1):
        for x in range(cx,ex + 1):
            es = filter(lambda e: e.x == x and e.y == y,a.entities)
            results += es
    return results

def isOffscreen(x,y,m):
    return x < 0 or x >= len(m[0]) or y < 0 or y >= len(m)

def makeStairs(x,y,id,destArea,destX,destY):
    return Stairs(x=x, y=y, c="S", id=id, kind="mapFeature", 
                  blockMove=False, destX=destX, destY=destY, destArea=destArea)

def shimmer(tile,initialRGB,rangeRGB):
    randomInRange = lambda r: random.randint(-1 * r,r)
    colorChanges  = map(randomInRange,rangeRGB)

    changed = zipWith(operator.add, initialRGB, colorChanges)
    r,g,b   = map(colorLimit,changed)
    return tile._replace(bg=libtcod.Color(r,g,b))

def thingInTheWay(entities,x,y,eid):    
    blockableThings = filter(lambda e: e.x  == x   and 
                                       e.y  == y   and 
                                       e.id != eid and 
                                       e.blockMove,entities)
    return len(blockableThings) > 0
    