from Tkinter import *
import DTImages

#to do:
#BUG: when a cell has a waterLevel higher than 1, but neighbors of 0, it
    #looks ugly. I'll leave this for now, then fix it in Java

#reorganize functions -> split into files?

#gameplay:
#make "water" spawners (don't add water, change the amount above to that value)
#make a level saving/loading system (good luck future me!) -> stage editor
#start on the turrets...
    #think
    #do
    #do betterish
    #repeat

#any optimizations I can think of

def mousePressed(event):
    #gather variables
    canvas=event.widget.canvas
    width,height=canvas.data.width,canvas.data.height
    cellSize=canvas.data.cellSize
    waterLevels,workStation=canvas.data.waterLevels,canvas.data.workStation
    maxCliffs,cliffHeight=canvas.data.maxCliffs,canvas.data.cliffHeight
    terrainHeights=canvas.data.terrainHeights
    numbers=canvas.data.numbers
    #find row and col
    x=max(min(event.x,width),0)
    y=max(min(event.y,height),0)
    row,col=y/cellSize,x/cellSize
    #add water and update cell display
    maxWaterHeight=(maxCliffs+1)*cliffHeight
    localHMax=maxWaterHeight-terrainHeights[row][col]
    waterLevels[row][col]=min(waterLevels[row][col]+10,localHMax)
    workStation[row][col]=min(workStation[row][col]+10,localHMax)
    updateScreen(canvas)
    #update text(if applicable)
    if canvas.data.showNumbers:
        text=str(round(waterLevels[row][col],3))
        font=("times",cellSize/4)
        x,y=(col+0.5)*cellSize,(row+0.5)*cellSize
        canvas.delete(numbers[row][col])
        numbers[row][col]=canvas.create_text(x,y,text=text,font=font)

def rightMousePressed(event):
    #gather variables
    canvas=event.widget.canvas
    width,height=canvas.data.width,canvas.data.height
    cellSize=canvas.data.cellSize
    waterLevels,workStation=canvas.data.waterLevels,canvas.data.workStation
    numbers=canvas.data.numbers
    #find row and col
    x=max(min(event.x,width),0)
    y=max(min(event.y,height),0)
    row,col=y/cellSize,x/cellSize
    #remove water and update cell display
    waterLevels[row][col]=max(waterLevels[row][col]-10,0.0)
    workStation[row][col]=max(workStation[row][col]-10,0.0)
    updateScreen(canvas)
    #update text (if applicable)
    if canvas.data.showNumbers:
        text,font=str(round(waterLevels[row][col],3)),("times",cellSize/4)
        x,y=(col+0.5)*cellSize,(row+0.5)*cellSize
        hasWater=(waterLevels[row][col]>0)
        canvas.delete(numbers[row][col])
        numbers[row][col]=canvas.create_text(x,y,text=text,font=font)

def keyPressed(event):
    canvas=event.widget.canvas
    if event.char=="s": doFullStep(canvas)
    elif event.char=="c": init(canvas)
    elif event.char in "12345": #HARDCODING: the maxHeight is hardcoded
        width,height=canvas.data.width,canvas.data.height
        cellSize,cliffHeight=canvas.data.cellSize,canvas.data.cliffHeight
        x=max(min(event.x,width-1),0) #the edge goes right b/c of integer div
        y=max(min(event.y,height-1),0) #so I -1 to prevent an index error
        row,col=y/cellSize,x/cellSize
        canvas.data.terrainHeights[row][col]=(int(event.char)-1)*cliffHeight
        updateScreen(canvas)

def ceil(n):
    if n==int(n): return int(n)
    return int(n+1)

#at some point, make a groundLevel function for efficiency? Nah.
#note: this uses workStation instead of waterLevels (for updateValues; may bug)
def updateCellDisplay(canvas,row,col):
    terrainHeights=canvas.data.terrainHeights
    waterLevels=canvas.data.waterLevels
    rows,cols=canvas.data.rows,canvas.data.cols
    cliffHeight=canvas.data.cliffHeight
    groundLevel=terrainHeights[row][col]/cliffHeight
    #MAGIC: a step every h/5
    waterLevel=ceil(waterLevels[row][col]*5/cliffHeight)

    up=1
    if row-1>=0 and row-1<rows and col>=0 and col<cols:
        
        localGround=terrainHeights[row-1][col]/cliffHeight
        localWater=ceil(waterLevels[row-1][col]*5/cliffHeight)
        if localGround+localWater<groundLevel+waterLevel: up=0

    right=1
    if row>=0 and row<rows and col+1>=0 and col+1<cols:
        localGround=terrainHeights[row][col+1]/cliffHeight
        localWater=ceil(waterLevels[row][col+1]*5/cliffHeight)
        if localGround+localWater<groundLevel+waterLevel: right=0

    down=1
    if row+1>=0 and row+1<rows and col>=0 and col<cols:
        localGround=terrainHeights[row+1][col]/cliffHeight
        localWater=ceil(waterLevels[row+1][col]*5/cliffHeight)
        if localGround+localWater<groundLevel+waterLevel: down=0

    left=1
    if row>=0 and row<rows and col-1>=0 and col-1<cols:

        localGround=terrainHeights[row][col-1]/cliffHeight
        localWater=ceil(waterLevels[row][col-1]*5/cliffHeight)
        if localGround+localWater<groundLevel+waterLevel: left=0
    i=8*up+4*right+2*down+left
    image=canvas.data.surfaceImages[groundLevel][waterLevel][i]
    canvas.itemconfig(canvas.data.cells[row][col],image=image)

#This moves the water for one round
def doFullStep(canvas):
    moveWater(canvas)
    updateValues(canvas)
    updateScreen(canvas)

#This handles the flow of the fluid on screen
#currently: model like heat transfer:
#get "heat" from surrounding sources
#lose "heat" to natural cooling
#it now works (YAY!), but the code could/should be simplified/clarified
def moveWater(canvas):
    waterLevels,workStation=canvas.data.waterLevels,canvas.data.workStation
    terrainHeights=canvas.data.terrainHeights
    maxHeight=canvas.data.cliffHeight*(canvas.data.maxCliffs+1)
    rows,cols=canvas.data.rows,canvas.data.cols
    directions=((-1,0),(0,-1),(1,0),(0,1)) #top,left,bottom,right
    for row in xrange(rows):
        for col in xrange(cols):
            newHeat=waterLevels[row][col] #new heat starts as the current heat
            centerHeat=waterLevels[row][col]
            centerHeight=terrainHeights[row][col]
            #finds neighbor's contributions to newHeat
            for drow,dcol in directions:
                #defining variables (including edge cases)
                tRow,tCol=row+drow,col+dcol
                if tRow<0 or tRow>=rows or tCol<0 or tCol>=cols:
                    neighborHeight=maxHeight #invisible off-screen cliffs
                    neighborHeat=0 #these border cliffs have no water on them
                else:
                    neighborHeight=terrainHeights[tRow][tCol]
                    neighborHeat=waterLevels[tRow][tCol]
                #adding appropriate heat value
                if neighborHeight>centerHeight:
                    newHeat+=min((neighborHeight-centerHeight+neighborHeat),
                                 (centerHeat+neighborHeat))/4
                else:
                    newHeat+=max((neighborHeight-centerHeight+neighborHeat),0)/4
            #decreasing newHeat because of heat loss
            workStation[row][col]=newHeat/2

#a hopefully-less-crazy version of the compressed heat transfer code above
"""
if neighborHeight>centerHeight:
    #the wall radiates heat, based on what's already in the cell
    newHeat+=centerHeat/4
    #the neighbor radiates heat
    newHeat+=neighborHeat/4
    #the center loses heat if it has too much
    dh=centerHeight+centerHeat-neighborHeight
    newHeat-=max(dh/4,0)
    
elif neighborHeight<centerHeight:
    #the center gets heat if a neighbor is overflowing
    dh=(neighborHeight+neighborHeat-centerHeight)
    newHeat+=max(dh/4,0)
else:
    #if the terrian is flat, it just gets some heat
    newHeat+=neighborHeat/4
"""   

#copies the information in workStation back into waterLevels,
#does evaporation, and changes the colors of cells that changed
def updateValues(canvas):
    waterLevels,workStation=canvas.data.waterLevels, canvas.data.workStation
    cellSize,stepHeight=canvas.data.cellSize,canvas.data.cliffHeight/5
    numbers=canvas.data.numbers
    font=("times",cellSize/4)
    totalWater=0
    for row in xrange(canvas.data.rows):
        y=(row+0.5)*cellSize
        for col in xrange(canvas.data.cols):
            if workStation[row][col]<0.001:
                workStation[row][col]=0.0
            waterLevels[row][col]=workStation[row][col]
            #draw helper text (again, only if applicable)
            if canvas.data.showNumbers:
                x=(col+0.5)*cellSize
                canvas.delete(numbers[row][col])
                text=str(round(waterLevels[row][col],3))
                numbers[row][col]=canvas.create_text(x,y,text=text,font=font)
            totalWater+=waterLevels[row][col]

def updateScreen(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            updateCellDisplay(canvas,row,col)
           
def initBoards(canvas):
    canvas.delete(ALL)
    rows,cols=canvas.data.rows,canvas.data.cols
    waterLevels,workStation,terrainHeights=[],[],[]
    numbers=[]
    cellSize=canvas.data.cellSize
    font=("times",cellSize/4)
    for row in xrange(rows):
        waterLevels.append([0.0]*cols)
        workStation.append([0.0]*cols)
        terrainHeights.append([0]*cols)
        numbers.append([0]*cols)
        if canvas.data.showNumbers:
            y=(row+0.5)*cellSize
            for col in xrange(cols):
                x=(col+0.5)*cellSize
                numbers[row][col]=canvas.create_text(x,y,text="0.0",font=font)
    canvas.data.waterLevels=waterLevels
    canvas.data.workStation=workStation
    canvas.data.numbers=numbers
    canvas.data.terrainHeights=terrainHeights

def initCells(canvas):
    cells=[]
    images=canvas.data.surfaceImages
    rows,cols=canvas.data.rows,canvas.data.cols
    cellSize=canvas.data.cellSize
    terrainHeights=canvas.data.terrainHeights
    cliffHeight=canvas.data.cliffHeight
    for row in xrange(rows):
        y=cellSize*(row+0.5)
        cells.append([0]*cols)
        for col in xrange(cols):
            x=cellSize*(col+0.5)
            height=int(terrainHeights[row][col]/cliffHeight)
            image=images[height][0][0]#no creeper initially, and no neighbors
            cells[row][col]=canvas.create_image(x,y,image=image)
    canvas.data.cells=cells

def init(canvas):
    w,h=canvas.data.width,canvas.data.height
    cellSize=canvas.data.cellSize
    rows,cols=h/cellSize,w/cellSize
    canvas.data.rows,canvas.data.cols=rows,cols
    canvas.data.showNumbers=True
    initBoards(canvas)
    initCells(canvas)

#actual dimensions: cellSize=10, width=800, height=600
#good for testing: cellSize=30, width=height=690

def run(width=690,height=690):
    root=Tk()
    canvas=Canvas(root,width=width,height=height)
    root.canvas=canvas.canvas=canvas
    canvas.pack()
    class Struct: pass
    canvas.data=Struct()
    canvas.data.width=width
    canvas.data.height=height
    canvas.data.cliffHeight=10
    canvas.data.cellSize=30
    canvas.data.maxCliffs=4 #4 cliffs
    DTImages.makeSurfaceImages(canvas)
    init(canvas)
    root.bind("<Button-1>",mousePressed)
    root.bind("<Button-3>",rightMousePressed)
    root.bind("<Key>",keyPressed)
    root.mainloop()
    
run()
