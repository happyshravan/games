#DrawMaze.py
#contains the maze-drawing code
#Michael Choquette
import math


def drawIslands(canvas):
    islands = canvas.data.maze
    rows,cols = len(islands),len(islands[0])
    color = canvas.data.islandColor
    r = min(canvas.data.cW,canvas.data.cH)/6
    for row in xrange(rows):
        for col in xrange(cols):
            drawCircle(canvas,islandCenter(canvas,row,col),r,color)

def drawCircle(canvas,(cx,cy),r,color):
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)

def islandCenter(canvas,row,col):
    if canvas.data.isPolar:
        cx,cy = canvas.data.w/2,canvas.data.h/2
        rows,cols = len(canvas.data.maze),len(canvas.data.maze[0])
        maxR = min(cx,cy)
        r = maxR*(row+1)/(rows+1)
        theta = 2*math.pi*col/cols
        return cx+r*math.cos(theta), cy-r*math.sin(theta)
    else:
        cellWidth,cellHeight = canvas.data.cW,canvas.data.cH
        return (col+0.5)*cellWidth,(row+0.5)*cellHeight

def drawBridges(canvas):
    islands = canvas.data.maze
    rows,cols = len(islands),len(islands[0])
    color = canvas.data.bridgeColor
    width = min(canvas.data.cW,canvas.data.cH)/15
    for r in xrange(rows):
        for c in xrange(cols):
            island = islands[r][c]
            if (island.east):
                canvas.create_line(islandCenter(canvas,r,c),
                                   islandCenter(canvas,r,c+1),
                                   fill=color, width=width)
            if (island.south):
                canvas.create_line(islandCenter(canvas,r,c),
                                   islandCenter(canvas,r+1,c),
                                   fill=color, width=width)

def drawSolution(canvas,startRow,startCol,path):
    row,col = startRow,startCol
    color = canvas.data.pathColor
    r = min(canvas.data.cW,canvas.data.cH)/6
    w = r*2/5
    drawCircle(canvas,islandCenter(canvas,row,col),r,color)
    for drow,dcol in path:
        canvas.create_line(islandCenter(canvas,row,col),
                           islandCenter(canvas,row+drow,col+dcol),
                           fill=color, width=w)
        row,col = row+drow,col+dcol
        drawCircle(canvas,islandCenter(canvas,row,col),r,color)
