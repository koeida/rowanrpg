import libtcodpy as libtcod
import random
import copy
from sets import Set
import hm

class Entity:
    def __init__(self):
        return

class Area:
    def __init__(self,m,entities):
        self.map = m
        self.entities = entities
        return

player = Entity()
player.x = 1
player.y = 1
player.c = "@"
player.id = 0
player.kind = "player"
player.movementType = "player"
player.blockMove = True
player.hp = 50

entities = [player]

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 80

#size of the game_map
game_map_WIDTH = 10
game_map_HEIGHT = 10

def makeSquirrel(x,y):
    global entities
    s = Entity()
    s.x = x
    s.y = y
    s.direction = 0
    s.c = "S"
    s.id = len(entities) + 1
    s.movementType = "bumper"
    s.kind = "creature"
    s.blockMove = True
    return s

def makeBear(x,y):
    global entities
    b = Entity()
    b.x = x
    b.y = y
    b.c = "B"
    b.id = len(entities) + 1
    b.movementType = "bear"
    b.kind = "creature"
    b.blockMove = True
    b.target = None
    return b

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

def draw_character(x,y,c,color = libtcod.white,bg = libtcod.BKGND_NONE):
    libtcod.console_set_default_foreground(con,color)
    libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET )
    libtcod.console_put_char(con,x,y,c,bg)

def render_all(game_map):
    color_hill          = libtcod.Color(102,204,0)
    color_low_ground    = libtcod.Color(51,102,0)
    color_med_ground    = libtcod.Color(76,153,0)
    color_shore         = libtcod.Color(123,154,0)
    color_shallow_water = libtcod.Color(105, 161, 255)
    color_deep_water    = libtcod.Color(25,90,206);

    tiles = {
            5:[" ",libtcod.white,color_hill],
            4:[" ",libtcod.white,color_med_ground],
            3:[" ",libtcod.white,color_low_ground],
            2:[" ",libtcod.white,color_shore],
            1:[" ",libtcod.white,color_shallow_water],
            0:[" ",libtcod.white,color_deep_water]}
    #go through all tiles, and set their background color
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            tileNum = game_map[y][x]
            c = tiles[tileNum][0]
            fgColor = tiles[tileNum][1]
            bgColor = tiles[tileNum][2]
            draw_character(x,y,c, fgColor, bgColor)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def first(f,l):
    r = filter(f,l)
    if len(r) > 0:
        return r[0]
    else:
        return None

def handle_keys():
    global player
    global entities
    global currentArea
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

    newX = player.x
    newY = player.y
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
        if k == '>':
            stairs = first(lambda e: e.kind == 'stairs' and e.x == player.x and e.y == player.y,entities)
            if stairs != None:
                currentArea = stairs.destMap
                newY = stairs.destY
                newX = stairs.destX
                entities = currentArea.entities

    if currentArea.map[newY][newX] != 0 and not thingInTheWay(entities,newX,newY,player.id):
        player.x = newX
        player.y = newY

def thingInTheWay(entities,x,y,eid):
    return len(filter(lambda e: e.x == x and e.y == y and e.id != eid and e.blockMove,entities)) > 0

def moveEntity(e,area):
    if e.movementType == "bumper":
        bumperMotion(e,area)
    elif e.movementType == "bear":
        bearMotion(e,area)

def getEntitiesIn(cx,cy,ex,ey,a):
    results = []
    for y in range(cy,ey + 1):
        for x in range(cx,ex + 1):
            es = filter(lambda e: e.x == x and e.y == y,a.entities)
            results += es
    return results

def contains(f,l):
    return len(filter(f,l)) > 0

def first(f,l):
    r = filter(f,l)
    if len(r) == 0:
        return None
    else:
        return r[0]

def bearMotion(e,area):
    if e.target == None:
        #Is player around?
        lookCx = e.x - 2
        lookCy = e.y - 2
        lookEx = e.x + 2
        lookEy = e.y + 2
        nearbyEntities = getEntitiesIn(lookCx,lookCy,lookEx,lookEy,area)
        player = first(lambda e: e.kind == "player",nearbyEntities)
        if player != None:
            print "I eat you now."
            e.target = player
    else:        
        if abs(e.x - e.target.x) <= 1 and abs(e.y - e.target.y) <= 1:
            print "ROARRRRR"

def bumperMotion(e,area):
    movements = [[0,1],
                [0,-1],
                [-1,0],
                [1,0]]
    currentMovement = movements[e.direction]
    yMove = currentMovement[0]
    xMove = currentMovement[1]
    oldX = e.x
    oldY = e.y
    e.x += xMove
    e.y += yMove

    if(area.map[e.y][e.x] == 0 or thingInTheWay(entities,e.x,e.y,e.id)):
        e.x = oldX
        e.y = oldY
        e.direction += 1
        if e.direction == 4:
            e.direction = 0


#############################################
# Initialization & Main Loop
#############################################

libtcod.console_disable_keyboard_repeat()

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

libtcod.console_disable_keyboard_repeat()


game_map = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]]

game_map2 = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]]

outdoors = Area(hm.getHeightMap(),entities)


entities += [makeSquirrel(2,2)]
entities += [makeSquirrel(2,3)]
entities += [makeBear(3,3)]

entities2 = [player]
map1 = Area(game_map,entities)
map2 = Area(game_map2,entities2)

entities += [makeStairs(2,5,map2,3,5)]
entities2 += [makeStairs(3,5,map1,2,5)]
currentArea = outdoors

while not libtcod.console_is_window_closed():
    #render the screen
    render_all(currentArea.map)

    for entity in entities:
        draw_character(entity.x,entity.y,entity.c)
        moveEntity(entity,currentArea)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    #handle keys and exit game if needed
    oldX = player.x
    oldY = player.y
    exit = handle_keys()
    if exit:
        break
    draw_character(oldX, oldY, " ")

