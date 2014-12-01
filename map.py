import copy
import libtcodpy as libtcod
import random

from globals import *
from misc import *

class Tile:
    def __init__(self,c,fg,bg,walkable = True):
        self.c = c
        self.onTick = lambda s: None
        self.fg = fg
        self.bg = bg
        self.animRate = 2
        self.changed = True
        self.animated = False
        self.walkable = walkable
    def tick(self):
        if self.animated and (ticks % self.animRate) == 0:
            self.changed = True
            self.onTick(self)

class Area:
    def __init__(self,newMap,entities):
        m = copy.deepcopy(newMap)
        color_hill          = libtcod.Color(102,204,0)
        color_low_ground    = libtcod.Color(51,102,0)
        color_med_ground    = libtcod.Color(76,153,0)
        color_shore         = libtcod.Color(123,154,0)
        color_shallow_water = libtcod.Color(105, 161, 255)
        color_deep_water    = libtcod.Color(25,90,206)
        tiles = {
            5:Tile(" ",libtcod.white,color_hill),
            4:Tile(" ",libtcod.white,color_med_ground),
            3:Tile(" ",libtcod.white,color_low_ground),
            2:Tile(" ",libtcod.white,color_shore),
            1:Tile(" ",libtcod.white,color_shallow_water),
            0:Tile(" ",libtcod.white,color_deep_water,False)}
        tiles[0].onTick = lambda self: shimmer(self,25,90,206,10,10,20)
        tiles[0].animated = True
        tiles[1].onTick = lambda self: shimmer(self,105,161,255,5,5,10)
        tiles[1].animated = True
        for y in range(len(m)):
            for x in range(len(m[0])):
                m[y][x] = copy.deepcopy(tiles[m[y][x]])
                m[y][x].animRate = random.randint(100,500)
        self.map = m
        self.entities = entities

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

def makeStairs(x,y,destMap,destX,destY):
    global entities
    s = Entity()
    s.x = x
    s.y = y
    s.c = ">"
    s.id = len(entities) + 1
    s.kind = "stairs"
    s.movementType = "stationary"
    s.destMap = destMap
    s.destX = destX
    s.destY = destY
    s.blockMove = False
    return s     

def shimmer(self,sr,sg,sb,rr,rg,rb):
    makeRange = lambda r: random.randint(-1 * r,r)
    limit = lambda v: within(v,0,255)
    colorMods = zip([sr,sg,sb],map(makeRange,[rr,rg,rb]))
    r,g,b = map(lambda vs: limit(vs[0] + vs[1]),colorMods)
    self.bg = libtcod.Color(r,g,b)

def thingInTheWay(entities,x,y,eid):
    return (len(filter(lambda e: e.x  == x   and 
                                 e.y  == y   and 
                                 e.id != eid and 
                                 e.blockMove,entities)) > 0)