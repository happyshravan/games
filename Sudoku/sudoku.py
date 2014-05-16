#suodku solver
#Michael Choquette
#this program provides a simple user interface,
#as well as a generalized solver

from Tkinter import *
import math
import copy
import time
import Solvers

###############User Interaction###############

def mousePressed(event):
    canvas=event.widget.canvas
    m,cS=canvas.data.margin,canvas.data.cellSize
    row,col=(event.y-m)/cS,(event.x-m)/cS
    if (row>=0 and row<canvas.data.rows and
        col>=0 and col<canvas.data.cols and
        canvas.data.startingBoard[row][col]==0):
        board,numbers=canvas.data.board,canvas.data.numbers
        number=int(board[row][col])+1
        text=str(number) if number<=canvas.data.rows else ""
        canvas.itemconfig(numbers[row][col],text=text)
        board[row][col]=number if number<=canvas.data.rows else 0

def rightMousePressed(event):
    canvas=event.widget.canvas
    m,cS=canvas.data.margin,canvas.data.cellSize
    row,col=(event.y-m)/cS,(event.x-m)/cS
    if (row>=0 and row<canvas.data.rows and
        col>=0 and col<canvas.data.cols and
        canvas.data.startingBoard[row][col]==0):
        board,numbers=canvas.data.board,canvas.data.numbers
        number=int(board[row][col])-1
        text=str(number) if number>0 else ""
        canvas.itemconfig(numbers[row][col],text=text)
        board[row][col]=max(number,0)

def keyPressed(event):
    canvas=event.widget.canvas
    if event.char=="r": init(canvas)
    elif event.char=="s":
        solveTime=solveIt(canvas)
        assert(Solvers.isFull(canvas.data.board) and
               not Solvers.hasContradiction(canvas.data.board))
        numbers,board=canvas.data.numbers,canvas.data.board
        for row in xrange(canvas.data.rows):
            for col in xrange(canvas.data.cols):
                text=str(board[row][col]) if board[row][col]>0 else ""
                canvas.itemconfig(numbers[row][col],text=text)
    elif event.char=="t": doTimeTest(canvas)

def solveIt(canvas):
    t0=time.clock()
    assert(Solvers.solve(canvas))
    return time.clock()-t0

def doTimeTest(canvas):
    print "starting time test..."
    maxTime=60 #1 minute
    timeSpent,solves=0,0
    lowTime,highTime=None,None
    while timeSpent<maxTime:
        solveTime=solveIt(canvas)
        assert type(solveTime)==float
        if lowTime==None or solveTime<lowTime: lowTime=solveTime
        if highTime==None or solveTime>highTime: highTime=solveTime
        timeSpent+=solveTime
        solves+=1
        canvas.data.board=copy.deepcopy(canvas.data.startingBoard)
    avgTime=timeSpent/solves
    print "RESULTS OF TRIAL:"
    print " SOLVES:",solves,"solves"
    print " TIME SPENT:",timeSpent,"seconds"
    print " AVERAGE SOLVE TIME:",avgTime,"seconds, or",avgTime/60,"minutes"
    print " VARIANCE:",highTime-lowTime,"seconds"
    print

#################init and draw###################

def cellCenter(canvas,row,col):
    m,cS=canvas.data.margin,canvas.data.cellSize
    return m+(col+0.5)*cS,m+(row+0.5)*cS

def drawBoard(canvas):
    rows,cols=canvas.data.rows,canvas.data.cols
    board=canvas.data.board
    cellSize=canvas.data.cellSize
    m=canvas.data.margin
    root=int(math.sqrt(rows))
    #draw gridlines
    x0,x1=m,m+cellSize*cols
    for row in xrange(rows+1):
        y=m+cellSize*row
        if row==0 or row==rows: thickness=5
        elif row%root==0: thickness=3
        else:
            thickness=1
        canvas.create_line(x0,y,x1,y,width=thickness)
    y0,y1=m,m+cellSize*rows
    for col in xrange(cols+1):
        x=m+cellSize*col
        if col==0 or col==cols: thickness=5
        elif col%root==0: thickness=3
        else:
            thickness=1
        canvas.create_line(x,y0,x,y1,width=thickness)
    #draw numbers
    numbers=[0]*rows
    startingBoard=canvas.data.startingBoard
    for row in xrange(rows):
        numbers[row]=[0]*cols
        for col in xrange(cols):
            number=board[row][col]
            text=str(number) if number>0 else ""
            font=("Helvetica",cellSize/2)
            fill="dark blue"if startingBoard[row][col]==0 else "black"
            cx,cy=cellCenter(canvas,row,col)
            numbers[row][col]=canvas.create_text(cx,cy,text=text,
                                                 font=font,fill=fill)
    canvas.data.numbers=numbers

def initBoard(canvas,n):
    assert n>0 and math.sqrt(n)==int(math.sqrt(n))
    if n==1: canvas.data.board=[[1]]
    elif n==4: canvas.data.board=[[2,0,0,1],
                                  [0,4,3,0],
                                  [0,2,1,0],
                                  [3,0,0,4]]
    elif n==9: canvas.data.board=[[7,0,6,0,5,0,3,0,8],
                                  [0,0,3,0,0,0,2,0,0],
                                  [0,1,0,0,9,0,0,4,0],
                                  [6,0,0,3,0,1,0,0,4],
                                  [0,0,1,0,0,0,5,0,0],
                                  [3,0,0,4,0,5,0,0,9],
                                  [0,6,0,0,8,0,0,1,0],
                                  [0,0,7,0,0,0,9,0,0],
                                  [2,0,4,0,1,0,8,0,6]]
    elif n==16: canvas.data.board=[[1,0,0,2,3,4,0,0,12,0,6,0,0,0,7,0],
                                   [0,0,8,0,0,0,7,0,0,3,0,0,9,10,6,11],
                                   [0,12,0,0,10,0,0,1,0,13,0,11,0,0,14,0],
                                   [3,0,0,15,2,0,0,14,0,0,0,9,0,0,12,0],
                                   [13,0,0,0,8,0,0,10,0,12,2,0,1,15,0,0],
                                   [0,11,7,6,0,0,0,16,0,0,0,15,0,0,5,13],
                                   [0,0,0,10,0,5,15,0,0,4,0,8,0,0,11,0],
                                   [16,0,0,5,9,12,0,0,1,0,0,0,0,0,8,0],
                                   [0,2,0,0,0,0,0,13,0,0,12,5,8,0,0,3],
                                   [0,13,0,0,15,0,3,0,0,14,8,0,16,0,0,0],
                                   [5,8,0,0,1,0,0,0,2,0,0,0,13,9,15,0],
                                   [0,0,12,4,0,6,16,0,13,0,0,7,0,0,0,5],
                                   [0,3,0,0,12,0,0,0,6,0,0,4,11,0,0,16],
                                   [0,7,0,0,16,0,5,0,14,0,0,1,0,0,2,0],
                                   [11,1,15,9,0,0,13,0,0,2,0,0,0,14,0,0],
                                   [0,14,0,0,0,11,0,2,0,0,13,3,5,0,0,12]]
    canvas.data.startingBoard=copy.deepcopy(canvas.data.board)

def init(canvas):
    canvas.delete(ALL)
    canvas.data.isSolved=False
    rows,cols=canvas.data.rows,canvas.data.cols
    canvas.data.cellSize=canvas.data.boardSize/rows
    canvas.data.mouseRow,canvas.data.mouseCol=rows/2,cols/2
    initBoard(canvas,rows)
    drawBoard(canvas)

def run(n):
    assert(math.sqrt(n)==int(math.sqrt(n)) and type(n)==int)
    boardSize,margin=600,25
    root=Tk()
    canvas=Canvas(root,width=boardSize+2*margin,height=boardSize+2*margin)
    canvas.pack()
    canvas.canvas=root.canvas=canvas
    class Struct: pass
    canvas.data=Struct()
    canvas.data.boardSize=boardSize
    canvas.data.margin=margin
    canvas.data.rows,canvas.data.cols=n,n
    init(canvas)
    root.bind("<Button-1>",mousePressed)
    root.bind("<Button-3>",rightMousePressed)
    root.bind("<Key>",keyPressed)
    root.mainloop()

run(9)
