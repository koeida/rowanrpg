from misc import *
from map import *
from display import *

def bearMotion(e,area):    
    if e.target == None:
        nearbyEntities = getEntitiesIn(e.x - 2,e.y - 2,e.x + 2,e.y + 2,area)       
        player = first(lambda e: e.kind == "player",area.entities)
        if player != None:
            target = player.id
            return e._replace(target=target)
        else:
            return e
    else:
        target = first(lambda a: a.id == e.target,area.entities)
        x = e.x
        y = e.y
        if target.x <= e.x:
            x -= 1
        if target.y <= e.y:
            y -= 1
        if target.x >= e.x:
            x += 1
        if target.y >= e.y:
            y += 1
        if abs(e.x - target.x) <= 1 and abs(e.y - target.y) <= 1:
            message("I am presently standing here eating you",libtcod.red)
        return e._replace(x = x, y = y)

def bumperMotion(e,area):
    movements = [[0,1],
                [0,-1],
                [-1,0],
                [1,0]]
    currentMovement = movements[e.direction]
    yMove = currentMovement[0]
    xMove = currentMovement[1]
    x = e.x + xMove
    y = e.y + yMove
    d = e.direction
    if bump(x,y,e.id,area):
        d += 1
        if d == 4:
            d = 0        
    return e._replace(x = x,y = y,direction=d)

def nullMotion(e,area):
    return e

def makeSquirrel(x,y,id):
    return Creature(x=x,y=y,direction=0,c="S",id=id,
                    movementFunc=bumperMotion,kind="creature",
                    blockMove=True,target=None,hp=5)

def makeBear(x,y,id):
    return Creature(x=x,y=y,direction=0,c="B",id=id,
                    movementFunc=bearMotion,kind="creature",
                    blockMove=True,target=None,hp=20)

def moveEntity(e,area):
    moved = e.movementFunc(e,area)    

    if bump(moved.x,moved.y,moved.id,area):
        return moved._replace(x = e.x,y=e.y)
    else:
        return moved