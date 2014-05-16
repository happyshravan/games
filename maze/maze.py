from Tkinter import *
import MakeMaze
import DrawMaze
import SolveMaze

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if event.char=="r":
        rows,cols = len(canvas.data.maze),len(canvas.data.maze[0])
        canvas.data.maze = MakeMaze.blankMaze(rows,cols)
        MakeMaze.connectIslands(canvas.data.maze)
        canvas.data.solution=None
    elif event.char=="c":
        canvas.data.isPolar = not canvas.data.isPolar
    elif event.char=="s":
        if canvas.data.solution!=None: canvas.data.solution=None
        else: canvas.data.solution = SolveMaze.solve(canvas.data.maze)
    redrawAll()

########### draw ###########

def redrawAll():
    canvas.delete(ALL)
    canvas.create_rectangle(0,0,canvas.data.w,canvas.data.h,fill = "black")
    DrawMaze.drawBridges(canvas)
    DrawMaze.drawIslands(canvas)
    if canvas.data.solution!=None:
        DrawMaze.drawSolution(canvas,0,0,canvas.data.solution)

########### init ###########

def init(rows,cols):
    canvas.data.islandColor = "dark green"
    canvas.data.bridgeColor = "white"
    canvas.data.pathColor = "red"
    canvas.data.isPolar = False
    canvas.data.solution = None
    #make the islands
    canvas.data.maze = MakeMaze.blankMaze(rows,cols)
    #connect the islands
    MakeMaze.connectIslands(canvas.data.maze)
    redrawAll()


########### copy-paste below here ###########

def run(rows,cols):
    # create the root and the canvas
    global canvas
    root = Tk()
    cWidth,cHeight = 600,600
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.w,canvas.data.h = cWidth,cHeight
    margin = 5
    canvas.data.cW,canvas.data.cH = (cWidth-margin)/cols,(cHeight-margin)/rows
    canvas.data.margin = margin
    init(rows,cols)
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    # and launch the app
    root.mainloop()

#run(4,15)
#run(5,5)
#run(30,30)
run(50,50)
#run(100,100)
