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
    def displayF(self,m):
        if self.l == None and self.r == None:   
            fillRect(m,self.leaf.x,self.leaf.y,self.leaf.w,self.leaf.h)
        if(self.l != None):
            self.l.displayF(m)
        if(self.r != None):
            self.r.displayF(m)

def drawRect(m,x,y,w,h):
    for row in range(h):
        for column in range(w):
            if row == 0 or column == 0 or row == (h - 1) or column == (w - 1): 
                m[row + y][column + x] = 0

def fillRect(m,x,y,w,h):
    for row in range(h):
        for column in range(w):            
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

def mapTreeBottom(f,t):
    if t == None:
        return None
    if t.l == None and t.r == None:
        res = f(t)        
        return Tree(res.leaf,None,None)
    else:
        return Tree(t.leaf,mapTreeBottom(f,t.l),mapTreeBottom(f,t.r))

def filterTree(f,t):
    if t == None:
        return []    
    if f(t):
        return [t] + filterTree(f,t.l) + filterTree(f,t.r)
    else:
        return filterTree(f,t.l) + filterTree(f,t.r)


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
    MIN_ROOM_SIZE = 10
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
        return Tree(Split(x,y,w,h),generateSplit(Tree(l,None,None)),generateSplit(Tree(r,None,None)))
    else:
        minSplit = roomBuffer
        maxSplit = w - roomBuffer
        splitX = random.randint(minSplit,maxSplit)        
        l = Split(x,y,splitX ,h)
        r = Split(splitX + x,y,w - splitX,h)
        t = Tree(Split(x,y,w,h),Tree(l,None,None),Tree(r,None,None))
        return Tree(Split(x,y,w,h),generateSplit(Tree(l,None,None)),generateSplit(Tree(r,None,None)))

def makeRoom(t):
    MIN_SIZE = 8
    area = t.leaf
    minX = area.x
    minY = area.y
    maxX = area.x + area.w - MIN_SIZE - 1
    maxY = area.y + area.h - MIN_SIZE - 1
    
    newX = random.randint(minX,maxX)
    newY = random.randint(minY,maxY)
    newW = random.randint(MIN_SIZE,area.w - (newX - minX)) - 1
    newH = random.randint(MIN_SIZE,area.h - (newY - minY)) - 1
    return Tree(Split(newX,newY,newW,newH),t.l,t.r)

def randomFrom(l):
    return l[random.randint(0,len(l))]

def connectBranches(m,t):
    leftXs =  set(range(t.l.leaf.x,t.l.leaf.x + t.l.leaf.w))
    rightXs = set(range(t.r.leaf.x,t.r.leaf.x + t.r.leaf.w))
    commonXs = list(leftXs.intersection(rightXs))

    top,bottom = [t.l.leaf,t.r.leaf] if t.l.leaf.y < t.r.leaf.y else [t.r.leaf,t.l.leaf]
    if(len(commonXs)):
        joinX = randomFrom(commonXs)
        hallStartY = top.y + top.h
        endY = bottom.y        
        fillRect(m,joinX,hallStartY,1,endY - hallStartY)        

def isSecondToLastNode(t):
    if t.l == None or t.r == None:
        return False
    elif t.l.l == None and t.r.l == None:
        return True
    else:
        return False


def generateDungeon(w,h):
    m = [[1 for x in range(w)] for y in range(h)]
    t = generateSplit(Tree(Split(0,0,w - 1,h - 1),None,None))
    t = mapTreeBottom(makeRoom,t)
    rooms = filterTree(lambda t: t.l == None and t.r == None,t)
    for room in rooms:
        r = room.leaf
        fillRect(m,r.x,r.y,r.w,r.h)
    roomsToJoin = filterTree(isSecondToLastNode,t)
    for room in roomsToJoin:
        connectBranches(m,room)
    
    return m      