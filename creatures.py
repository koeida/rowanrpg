from misc import *
from map import *
from display import *

def bearMotion(e,area):
    e = copy.deepcopy(e)
    
    if e.target == None:
        #Is player around?
        lookCx = e.x - 2
        lookCy = e.y - 2
        lookEx = e.x + 2
        lookEy = e.y + 2
        nearbyEntities = getEntitiesIn(lookCx,lookCy,lookEx,lookEy,area)       
        player = first(lambda e: e.kind == "player",area.entities)
        if player != None:
            message("I eat you now.",libtcod.red)
            e.target = player.id
    else:
        target = first(lambda a: a.id == e.target,area.entities)
        if target.x <= e.x:
            e.x -= 1
        if target.y <= e.y:
            e.y -= 1
        if target.x >= e.x:
            e.x += 1
        if target.y >= e.y:
            e.y += 1
        print "bear movin'"
        if abs(e.x - target.x) <= 1 and abs(e.y - target.y) <= 1:
            message("I am presently standing here eating you",libtcod.red)
    return e

def bumperMotion(e,area):
    e = copy.deepcopy(e)
    movements = [[0,1],
                [0,-1],
                [-1,0],
                [1,0]]
    currentMovement = movements[e.direction]
    yMove = currentMovement[0]
    xMove = currentMovement[1]
    e.x += xMove
    e.y += yMove
    if bump(e.x,e.y,e.id,area):
        e.direction += 1
        if e.direction == 4:
            e.direction = 0

    return e

def makeSquirrel(x,y,id):
    global entities
    s = Entity()
    s.x = x
    s.y = y
    s.direction = 0
    s.c = "S"
    s.id = id
    s.movementType = "bumper"
    s.kind = "creature"
    s.blockMove = True
    s.hp = 5
    return s

def makeBear(x,y,id):
    global entities
    b = Entity()
    b.x = x
    b.y = y
    b.c = "B"
    b.id = id
    b.movementType = "bear"
    b.kind = "creature"
    b.blockMove = True
    b.target = None
    b.hp = 20
    return b

def moveEntity(e,area):
    e = copy.deepcopy(e)

    oldX = e.x
    oldY = e.y
    if e.movementType == "bumper":
        e = bumperMotion(e,area)
    elif e.movementType == "bear":
        e = bearMotion(e,area)

    if bump(e.x,e.y,e.id,area):
        e.x = oldX
        e.y = oldY
    return e