from collections import namedtuple
from functools import partial

import copy

Entity = namedtuple('Entity',['x','y','c','id','kind','blockMove'])

Creature = namedtuple('Creature',Entity._fields + 
    ('direction','movementFunc','target','hp'))

Stairs = namedtuple('Stairs',Entity._fields +
    ('destArea','destX','destY'))

def chain(fs,v):
    return reduce((lambda x,y: y(x)),fs,v)

def contains(f,l):
    return len(filter(f,l)) > 0

def within(lower,upper,v):
    if v >= upper:
        return upper
    elif v <= lower:
        return lower
    else:
        return v

colorLimit = partial(within,0,255)

def first(f,l):
    r = filter(f,l)
    if len(r) > 0:
        return r[0]
    else:
        return None

def compose(f,g):
    return lambda x: f(g(x))

def zipWith(f,l,l2):
    z = zip(l,l2)
    return map(lambda e: f(e[0],e[1]),z)

def map2d(f,l):
    l = copy.deepcopy(l)
    for y in range(len(l)):
        for x in range(len(l[0])):
            l[y][x] = f(l[y][x])
    return l