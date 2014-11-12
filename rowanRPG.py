import libtcodpy as libtcod
import random

class Entity:
    def __init__(self):
        return

starting_map = [[1 for x in range(100)] for x in range(100)]

player = Entity()
player.x = 50
player.y = 50
player.c = "@"
player.id = 0

squirrel = Entity()
squirrel.x = 51
squirrel.y = 51
squirrel.direction = 0
squirrel.c = "S"
squirrel.id = 1

entities = [player,squirrel]

#actual size of the window
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100

#size of the game_map
game_map_WIDTH = 100
game_map_HEIGHT = 100

color_dark_wall = libtcod.Color(50, 50, 0)
color_dark_ground = libtcod.Color(100, 100, 50)
color_grass = libtcod.Color(0, 150, 0)
color_light_green = libtcod.Color(0,250,0);
color_tree = libtcod.Color(0, 100, 0)

def draw_character(x,y,c,color = libtcod.white,bg = libtcod.BKGND_NONE):
    libtcod.console_set_default_foreground(con,color)
    libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET )
    libtcod.console_put_char(con,x,y,c,bg)

def render_all(game_map):
    tiles = {
            0:[" ",libtcod.white,color_dark_ground],
            1:[" ",libtcod.white,color_dark_wall],
            2:["#",color_light_green,color_grass],
            3:["T",color_tree,color_grass],
            4:["S",libtcod.white,color_dark_ground]}
    #go through all tiles, and set their background color
    for y in range(game_map_HEIGHT):
        for x in range(game_map_WIDTH):
            tileNum = game_map[y][x]
            c = tiles[tileNum][0]
            fgColor = tiles[tileNum][1]
            bgColor = tiles[tileNum][2]
            draw_character(x,y,c, fgColor, bgColor)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def generateCave(startingMap):
    spawn_rate = 5
    MAX_DIGGERS = 2000
    diggers = [[50,50,100]]
    i = 0
    while sum(map(sum,startingMap)) > 8000:
        i += 1
        availableDiggers = filter(lambda x: x[2] != 0,diggers)
        for digger in availableDiggers:
            dx = digger[0]
            dy = digger[1]
            energy = digger[2]
            if energy > 0:
                startingMap[dy][dx] = 0
                atTop = dy == 0
                atBottom = dy == 99
                atLeft = dx == 0
                atRight = dx == 99
                possibleMoves = []
                if not atTop: possibleMoves += [[1,startingMap[dy - 1]]]
                if not atBottom: possibleMoves += [[2,startingMap[dy + 1]]]
                if not atLeft: possibleMoves += [[4,startingMap[dx - 1]]]
                if not atRight: possibleMoves += [[3,startingMap[dx + 1]]]
                possibleMoves = filter(lambda m: m[1] != 0,possibleMoves)

                if len(possibleMoves) == 0:
                    if(len(availableDiggers) == 1):
                        direction = random.randint(1,4)
                        oldX = dx
                        oldY = dx
                        if direction == 1: dx -= 1
                        if direction == 2: dx += 1
                        if direction == 3: dy -= 1
                        if direction == 4: dy += 1
                        if dx <= 1 or dx >= len(startingMap) - 1 or dy <= 1 or dy >= len(startingMap) - 1:
                            dx = oldX
                            dy = oldY
                        digger[0] = dx
                        digger[1] = dy
                    else:
                        digger[2] = 0
                else:
                    direction = possibleMoves[random.randint(0,len(possibleMoves) - 1)][0]
                    oldX = dx
                    oldY = dy
                    if direction == 1: dy -= 1
                    if direction == 2: dy += 1
                    if direction == 3: dx += 1
                    if direction == 4: dx -= 1
                    if dx <= 1 or dx >= len(startingMap) - 1 or dy <= 1 or dy >= len(startingMap) - 1:
                        dx = oldX
                        dy = oldY
                    digger[0] = dx
                    digger[1] = dy
                    if random.randint(0,1000) < spawn_rate:
                        if len(diggers) > MAX_DIGGERS:
                            print "MAX"
                        diggers += [[dx,dy,random.randint(200,400)]]

    return startingMap

game_map = generateCave(starting_map)
def handle_keys():
    global player
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

    if game_map[newY][newX] == 0:
        player.x = newX
        player.y = newY

def thingInTheWay(entities,x,y,eid):
    return len(filter(lambda e: e.x == x and e.y == y and e.id != eid,entities)) > 0

def moveSquirrel():
    global game_map
    global squirrel
    movements = [[0,1],
                [0,-1],
                [-1,0],
                [0,1]]
    currentMovement = movements[squirrel.direction]
    yMove = currentMovement[0]
    xMove = currentMovement[1]
    oldX = squirrel.x
    oldY = squirrel.y
    squirrel.x += xMove
    squirrel.y += yMove

    if(game_map[squirrel.y][squirrel.x] != 0 or thingInTheWay(entities,squirrel.x,squirrel.y,squirrel.id)):
        squirrel.x = oldX
        squirrel.y = oldY
        squirrel.direction += 1
        if squirrel.direction == 4:
            squirrel.direction = 0


#############################################
# Initialization & Main Loop
#############################################



libtcod.console_disable_keyboard_repeat()

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

libtcod.console_disable_keyboard_repeat()

while not libtcod.console_is_window_closed():
    #render the screen
    moveSquirrel()
    render_all(game_map)    

    for entity in entities:
        draw_character(entity.x,entity.y,entity.c)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    #handle keys and exit game if needed
    oldX = player.x
    oldY = player.y
    exit = handle_keys()
    if exit:
        break
    draw_character(oldX, oldY, " ")

