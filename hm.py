#!/usr/bin/python
import math
import libtcodpy as libtcod
# size of the heightmap
HM_WIDTH=80
HM_HEIGHT=80
rnd=libtcod.random_new()
noise=libtcod.noise_new(2,libtcod.NOISE_DEFAULT_HURST,libtcod.NOISE_DEFAULT_LACUNARITY,rnd)
def addHill(hm,nbHill,baseRadius,radiusVar,height) :
    for i in range(nbHill) :
        hillMinRadius=baseRadius*(1.0-radiusVar)
        hillMaxRadius=baseRadius*(1.0+radiusVar)
        radius = libtcod.random_get_float(rnd,hillMinRadius, hillMaxRadius)
        theta = libtcod.random_get_float(rnd,0.0, 6.283185) # between 0 and 2Pi
        dist = libtcod.random_get_float(rnd,0.0, float(min(HM_WIDTH,HM_HEIGHT))/2 - radius)
        xh = int(HM_WIDTH/2 + math.cos(theta) * dist)
        yh = int(HM_HEIGHT/2 + math.sin(theta) * dist)
        libtcod.heightmap_add_hill(hm,float(xh),float(yh),radius,height)
# 3x3 kernel for smoothing operations
smoothKernelSize=9
smoothKernelDx=[-1,0,1,-1,0,1,-1,0,1]
smoothKernelDy=[-1,-1,-1,0,0,0,1,1,1]
smoothKernelWeight=[1.0,2.0,1.0,2.0,20.0,2.0,1.0,2.0,1.0]
# function building the heightmap
def buildMap(hm) :
    libtcod.heightmap_add_fbm(hm,noise,3.83,3.83,400,0,4.93,1,0.35)
    libtcod.heightmap_normalize(hm)

def head(l):
    if len(l) == 0:
        return None
    else:
        return l[0]

def tail(l):
    return l[1:]

def next(l):
    return head(head(l))

def takeWhile(f,l):
    results = []
    for e in l:
        if f(e):
            results += [e]
        else:
            break
    return results

def getHeightMap():
    # test code to print the heightmap
    hm=libtcod.heightmap_new(HM_WIDTH,HM_HEIGHT)
    buildMap(hm)
    result = [[0 for x in range(HM_WIDTH)] for y in range(HM_HEIGHT)]    
    for x in range(HM_WIDTH) :
       for y in range(HM_HEIGHT) :
            z = libtcod.heightmap_get_value(hm,x,y)
            val=int(z*255) & 0xFF            
            
            tileRanges = [
                [0,0],                
                [110,2],
                [140,3],
                [190,4],
                [240,5],
                [300,6]]
            
            tile = takeWhile(lambda e: val >= e[0],tileRanges)[-1][1]           
            result[y][x] = tile
    return result