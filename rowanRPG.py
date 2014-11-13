import libtcodpy as libtcod
import random
import copy
from sets import Set

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
game_map_WIDTH = 80
game_map_HEIGHT = 80

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
            0:[".",libtcod.white,color_dark_ground],
            1:["#",libtcod.white,color_dark_wall],
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

def carveRoom(m,x,y,width,height,carveWith):   
    result = copy.deepcopy(m)
    for cy in range(height):
        for cx in range(width):
            yi = y + cy
            xi = x + cx
            result[yi][xi] = carveWith
    return result

def multiListCopy(source,dest,startX,startY):
    result = copy.deepcopy(dest)
    for y in range(len(source)):
        for x in range(len(source[0])):
            result[y + startY][x + startX] = source[y][x]            
    return result

class Split:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Tree:
    def __init__(self,leaf,l,r):
        self.leaf = leaf
        self.l = l
        self.r = r
    def display(self):
        #if self.l == None and self.r == None:
        print str(self.leaf.x) + "," + str(self.leaf.y) + " w:" + str(self.leaf.w) + " h:" + str(self.leaf.h)
        if(self.l != None):
            self.l.display()
        if(self.r != None):
            self.r.display()
    def displayG(self,m):        
        drawRect(m,self.leaf.x,self.leaf.y,self.leaf.w,self.leaf.h)
        if(self.l != None):
            self.l.displayG(m)
        if(self.r != None):
            self.r.displayG(m)

def drawRect(m,x,y,w,h):
    for row in range(h):
        for column in range(w):
            if row == 0 or column == 0 or row == (h - 1) or column == (w - 1): 
                m[row + y][column + x] = 0
    

def filterTree(f,t):
    if t == None: return None
    if f(t.leaf):
        return Tree(t.leaf,filterTree(f,t.l),filterTree(f,t.r))
    else:
        return None

def mapTree(f,t):
    if t == None: return None
    res = f(t)
    return Tree(res.leaf,mapTree(f,t.l),mapTree(f,t.r))

m = [[1 for x in range(100)] for y in range(100)]

def treeDebug(t):
    global m
    t.displayG(m)
    render_all(m)    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

def generateSplit(t):
    global m
    x = t.leaf.x
    y = t.leaf.y
    w = t.leaf.w
    h = t.leaf.h
    MIN_ROOM_SIZE = 20
    if w < MIN_ROOM_SIZE or h < MIN_ROOM_SIZE:
        return None

    roomBuffer = MIN_ROOM_SIZE / 2
    vertical = random.randint(0,1)
    if(vertical):
        minSplit = roomBuffer
        maxSplit = h - roomBuffer        
        splitY = random.randint(minSplit,maxSplit)
        l = Split(x,y,w,splitY)
        r = Split(x,splitY + y,w,h - splitY)
        t = Tree(Split(x,y,w,h),Tree(l,None,None),Tree(r,None,None))           
        treeDebug(t)
        return Tree(Split(x,y,w,h),generateSplit(Tree(l,None,None)),generateSplit(Tree(r,None,None)))
    else:
        minSplit = roomBuffer
        maxSplit = w - roomBuffer
        splitX = random.randint(minSplit,maxSplit)        
        l = Split(x,y,splitX ,h)
        r = Split(splitX + x,y,w - splitX,h)
        t = Tree(Split(x,y,w,h),Tree(l,None,None),Tree(r,None,None))
        treeDebug(t)
        return Tree(Split(x,y,w,h),generateSplit(Tree(l,None,None)),generateSplit(Tree(r,None,None)))
        

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


t = generateSplit(Tree(Split(0,0,80,80),None,None))
t.displayG(m)
render_all(m)    
libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
libtcod.console_flush()
print "done"
key = libtcod.console_wait_for_keypress(True)
exit()


while not libtcod.console_is_window_closed():
    #render the screen
    #moveSquirrel()
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

