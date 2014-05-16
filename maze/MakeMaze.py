#MakeMaze.py
#Michael Choquette
#contains the code for making a maze
import random
import time #for testing

############################### Simple method ################################
#each island has a number; the whole board is updated when islands are joined
class Struct: pass
def makeIsland(number):
    island = Struct()
    island.east = island.south = False
    island.number = number
    return island

def blankMaze(rows,cols):
    class Struct: pass
    islands = [[0]*cols for row in xrange(rows)]
    counter = 0
    for row in xrange(rows):
        for col in xrange(cols):
            islands[row][col] = makeIsland(counter)
            counter+=1
    return islands

def connectIslands(islands):
    rows,cols = len(islands),len(islands[0])
    for i in xrange(rows*cols-1):
        makeBridge(islands)

def makeBridge(islands):
    rows,cols = len(islands),len(islands[0])
    while True:
        row,col = random.randint(0,rows-1),random.randint(0,cols-1)
        start = islands[row][col]
        if flipCoin()=="h": #try to go east
            if col==cols-1: continue
            target = islands[row][col+1]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.east = True
            renameIslands(start,target,islands)
        else: #try to go south
            if row==rows-1: continue
            target = islands[row+1][col]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.south = True
            renameIslands(start,target,islands)
        #only got here if a bridge was made
        return

def renameIslands(i1,i2,islands):
    n1,n2 = i1.number,i2.number
    lo,hi = min(n1,n2),max(n1,n2)
    for row in islands:
        for island in row:
            if island.number==hi: island.number=lo

def flipCoin():
    return random.choice("ht")

##t0 = time.clock()
##maze = blankMaze(100,100) #.025 seconds
##t1 = time.clock()
##print t1-t0
##t2 = time.clock()
##connectIslands(maze) #10 seconds
##t3 = time.clock()
##print t3-t2

################################# fast method #################################
#uses union-find to efficiently union everything together
#current state: unfinished
class Island:
    def __init__(this,number):
        this.east = this.south = False
        this.node = Node()

    def connectIslands(this,island2):
        r1,r2 = this.node.getRoot(),island2.node.getRoot()
        if r1==r2: return
        if r1.rank<r2.rank:
            r1.isRoot = False
            r1.parent = r2
        elif r2.rank<r1.rank:
            r2.isRoot = False
            r2.parent = r1
        else: #only increase rank when merging trees of equal height
            r1.isRoot = False
            r1.parent = r2
            r2.rank+=1

    def connectedTo(this,island2):
        return this.node.getRoot() == island2.node.getRoot()

class Node:
    def __init__(this):
        this.parent=None
        this.isRoot=True
        this.rank = 0

    def getRoot(this):
        def get(node):
            if node.isRoot: return node
            node.parent = get(node.parent)
            return node.parent
        return get(this)

def blankMaze(rows,cols):
    islands = [[0]*cols for row in xrange(rows)]
    counter = 0
    for row in xrange(rows):
        for col in xrange(cols):
            islands[row][col] = Island(counter)
            counter+=1
    return islands

def getAllMoves(rows,cols):
    options = [0]*(rows*cols*2-rows-cols)
    i=0
    for j in xrange(rows-1):
        options[i] = (j,cols-1,"s")
        i+=1
    for j in xrange(cols-1):
        options[i] = (rows-1,j,"e")
        i+=1
    for row in xrange(rows-1):
        for col in xrange(cols-1):
            options[i] = (row,col,"e")
            options[i+1] = (row,col,"s")
            i+=2
    random.shuffle(options)
    return (a for a in options)

def connectIslands(islands):
    rows,cols = len(islands),len(islands[0])
    options = getAllMoves(rows,cols)
    for i in xrange(rows*cols-1):
        makeBridge(islands,options)

#to do: take in options as a randomized stack, and keep taking/using values
#if a value is invalid, it will never be valid again,
        #so you don't have to add anything back in
def makeBridge(islands,options):
    rows,cols = len(islands),len(islands[0])
    while True:
        row,col,direction = options.next()
        start = islands[row][col]
        if direction=="e": #try to go east
            target = islands[row][col+1]
            if start.connectedTo(target): continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.east = True
        else: #try to go south
            target = islands[row+1][col]
            if start.connectedTo(target): continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.south = True
        #only got here if a bridge was made
        start.connectIslands(target)
        return

def flipCoin():
    return random.choice("ht")

##t0 = time.clock()
##maze = blankMaze(1000,1000)
##t1 = time.clock()
##print t1-t0
##t2 = time.clock()
##connectIslands(maze)
##t3 = time.clock()
##print t3-t2
