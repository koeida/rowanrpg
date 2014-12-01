class Entity:
    def __init__(self):
        return

def chain(fs,v):
    return reduce((lambda x,y: y(x)),fs,v)

def contains(f,l):
    return len(filter(f,l)) > 0

def within(v,lower,upper):
    if v >= upper:
        return upper
    elif v <= lower:
        return lower
    else:
        return v

def first(f,l):
    r = filter(f,l)
    if len(r) > 0:
        return r[0]
    else:
        return None