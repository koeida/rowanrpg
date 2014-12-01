from libtcodpy import *
from globals import *
from map import *

#LIBTCOD INIT
def initDisplay():
    global GameGlobals
    sys_set_fps(60)
    console_set_custom_font('arial10x10.png', FONT_TYPE_GREYSCALE | FONT_LAYOUT_TCOD)
    console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    GameGlobals.con = console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    console_disable_keyboard_repeat()
    GameGlobals.panel = console_new(SCREEN_WIDTH,PANEL_HEIGHT)

def clearPanel(panel,w,h):
    for y in range(h):
        for x in range(w):
            console_set_default_foreground(panel,black)
            console_set_char_background(panel, x, y, black, BKGND_SET )
            console_put_char(panel,x,y," ",black)

def renderEntities(currentArea):
    for entity in currentArea.entities:
        draw_character(entity.x,entity.y,entity.c,
                       white,currentArea.map[entity.y][entity.x].bg)


def display(currentArea):
    renderMap(currentArea.map)
    renderEntities(currentArea)
    console_blit(GameGlobals.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    renderPanel(GameGlobals.panel,GameGlobals.statusMessages[-4:])
    console_blit(GameGlobals.panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
    console_flush()

def draw_character(x,y,c,color = white,bg = BKGND_NONE):
    console_set_default_foreground(GameGlobals.con,color)
    console_set_char_background(GameGlobals.con, x, y, bg, BKGND_SET )
    console_put_char(GameGlobals.con,x,y,c,bg)

def message(s,c):
    global GameGlobals
    GameGlobals.statusMessages += [(s,c)]
    clearPanel(GameGlobals.panel,SCREEN_WIDTH,PANEL_HEIGHT)

def renderMap(game_map):
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            tile = game_map[y][x]            
            tile = tickTile(tile,GameGlobals.ticks)
            c = tile.c
            fgColor = tile.fg 
            bgColor = tile.bg
            if(tile.changed):
                draw_character(x,y,c, fgColor, bgColor)
                game_map[y][x] = tile._replace(changed = False)

def renderPanel(panel,msgs):
    console_set_default_foreground(panel,white)
    console_print_ex(panel,1,0,BKGND_NONE,LEFT,str(sys_get_fps()))
    y = 1
    for (line,color) in msgs:
        console_set_default_foreground(panel,color)
        console_print_ex(panel,1,y,BKGND_NONE,LEFT,line)
        y += 1