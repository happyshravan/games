#GSLevels
#Michael Choquette, mchoquet
#This file contains the code required to run the levels and menu screen

import GSclasses
import GSscores

def doLevel(canvas,useSavedTileSpots):
    if (canvas.data["level"]==0):
        doMenu(canvas)
    else:
        makeItems(canvas,useSavedTileSpots)
        drawGame(canvas)
        drawSidebar(canvas)
        drawBalls(canvas)


##### makeItems #####
       
def makeItems(canvas,useSavedTileSpots): 
    makeBalls(canvas)
    GSscores.loadTiles(canvas,useSavedTileSpots)
    makeGoals(canvas)

def makeBalls(canvas):#w and h refer to the game, not the canvas
    h=canvas.data["canvasHeight"]
    w=canvas.data["gameWidth"]
    level=canvas.data["level"]
    r1=h/60
    balls=[]
    if (level==1):
        balls.append(GSclasses.Ball(canvas,w/8,h/2,r1))
    elif(level==2):
        balls.append(GSclasses.Ball(canvas,w/2,h*5/12,r1))
    elif(level==3):
        balls.append(GSclasses.Ball(canvas,w/7,h/6,r1))
    elif(level==4):
        balls.append(GSclasses.Ball(canvas,w/7,h/6,r1))
        balls[0].vx = 1000*1000*1000
        balls[0].vy = 1000*1000*2000
    elif(level==5):
        balls.append(GSclasses.Ball(canvas,w/4,h/3,r1))
    elif(level==6):
        balls.append(GSclasses.Ball(canvas,w*13/14,h/3-r1,r1))
    elif(level==7):
        balls.append(GSclasses.Ball(canvas,w/7,h/6+7,r1))
    elif(level==8):
        balls.append(GSclasses.Ball(canvas,w/2,h/2,r1))
    elif(level==9):
        balls.append(GSclasses.Ball(canvas,w/7,h*5/6,r1))
        balls.append(GSclasses.Ball(canvas,w*3/4,h*5/6,r1,"red"))
    elif(level==10):
        balls.append(GSclasses.Ball(canvas,w*2/5,h/2,r1))
    elif(level==11):
        balls.append(GSclasses.Ball(canvas,w/3-r1/2,h/3,r1))
        balls.append(GSclasses.Ball(canvas,w*11/16,h/2,r1,"red"))
    elif(level==12):
        balls.append(GSclasses.Ball(canvas,w/7,h/6,r1))        
    canvas.data["balls"]=balls

def makeTiles(canvas):#w and h refer to the game, not the canvas
    level=canvas.data["level"]
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    tW=w/12
    tH=tW
    tiles=[]
    if (level==1): 
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*5/12, tW, tH, "right"))
    elif (level==2):
        tiles.append(GSclasses.Tile(canvas, w*5/6,h*5/12,tW,tH,"up"))
        tiles.append(GSclasses.Tile(canvas, w*17/18,h*5/12,tW,tH,"up"))
    elif (level==3):
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*5/12, tW, tH, "up"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*5/12, tW, tH, "right"))
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*7/12, tW, tH, "left"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*7/12, tW, tH, "down"))
    elif ((level>3)and(level<=12)):
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*5/12, tW, tH, "up"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*5/12, tW, tH, "up"))
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*7/12, tW, tH, "right"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*7/12, tW, tH, "right"))
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*9/12, tW, tH, "left"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*9/12, tW, tH, "left"))
        tiles.append(GSclasses.Tile(canvas, w*5/6, h*11/12, tW, tH, "down"))
        tiles.append(GSclasses.Tile(canvas, w*17/18, h*11/12, tW, tH, "down"))
    canvas.data["tiles"]=tiles

def doObstacles(canvas):#w and h refer to the game, not the canvas
    w=canvas.data["gameWidth"]
    h=canvas.data["canvasHeight"]
    level=canvas.data["level"]
    obstacles=[]
    leftWall=GSclasses.Obstacle(canvas,-2000,-2000,0,h+2000)
    obstacles.append(leftWall)
    topWall=GSclasses.Obstacle(canvas,-2000,-2000,w+2000,0)
    obstacles.append(topWall)
    rightWall=GSclasses.Obstacle(canvas,w,-2000,w+2000,h+2000)
    obstacles.append(rightWall)
    bottomWall=GSclasses.Obstacle(canvas,-2000,h,w+2000,h+2000)
    obstacles.append(bottomWall)
    if (level==1):
        obstacles.append(GSclasses.Obstacle(canvas,0,h*2/3,w*2/3,h))
        obstacles.append(GSclasses.Obstacle(canvas,w*5/6,h*1/3,w,h))
    elif (level==2):
        obstacles.append(GSclasses.Obstacle(canvas,w/2+3,h*2/3,w,h))
    elif (level==3):
        obstacles.append(GSclasses.Obstacle(canvas,0,h/3,w*2/3,h/2))
        obstacles.append(GSclasses.Obstacle(canvas,0,h*3/4,w/4,h))  
    elif (level==4):
        obstacles.append(GSclasses.Obstacle(canvas,w*3/7,h*5/12,w*4/7,h*7/12))
    elif (level==5):
        obstacles.append(GSclasses.Obstacle(canvas,w*69/140,h*2/3,w*71/140,h))
    elif (level==6):
        obstacles.append(GSclasses.Obstacle(canvas,0,h/3,w/7,h))
        obstacles.append(GSclasses.Obstacle(canvas,w/7,h*4/9,w*2/7,h))
        obstacles.append(GSclasses.Obstacle(canvas,w*2/7,h*5/9,w*3/7,h))
        obstacles.append(GSclasses.Obstacle(canvas,w*3/7,h*6/9,w*4/7,h))
        obstacles.append(GSclasses.Obstacle(canvas,w*4/7,h*7/9,w*5/7,h))
        obstacles.append(GSclasses.Obstacle(canvas,w*5/7,h*8/9,w*6/7,h))
    elif (level==7):
        obstacles.append(GSclasses.Obstacle(canvas,w*4/7,h/3,w,h/2))
        obstacles.append(GSclasses.Obstacle(canvas,w*4/7,h/2,w*5/7,h*7/12))
        obstacles.append(GSclasses.Obstacle(canvas,w*6/7,h/2,w,h*7/12))
    elif (level==8):
        pass
    elif (level==9):
        obstacles.append(GSclasses.Obstacle(canvas,w*67/140,h/2,w*73/140,h))
        obstacles.append(GSclasses.Obstacle(canvas,0,h*32/70,w*73/140,h/2))
    elif (level==10):
        pass
    elif (level==11):
        obstacles.append(GSclasses.Obstacle(canvas,w*2/3-2,h/3-2,w*2/3+2,h/3+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/2-2,h*2/3-2,w/2+2,h*2/3+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*3/8-2,h/2-2,w*3/8+2,h/2+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/7-2,h*5/12-2,w/7+2,h*5/12+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/12-2,h/5-2,w/12+2,h/5+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*6/11-2,h*7/10-2,w*6/11+2,h*7/10+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*3/4-2,h/15-2,w*3/4+2,h/15+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*4/5-2,h*7/12-2,w*4/5+2,h*7/12+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/3-2,h*4/5-2,w/3+2,h*4/5+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/8-2,h*5/7-2,w/8+2,h*5/7+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*11/26-2,h*9/10-2,w*11/26+2,h*9/10+2))
        obstacles.append(GSclasses.Obstacle(canvas,w/4-2,h/10-2,w/4+2,h/10+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*3/5-2,h/6-2,w*3/5+2,h/6+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*11/16-2,h*5/6-2,w*11/16+2,h*5/6+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*4/7-2,h*29/30-2,w*4/7+2,h*29/30+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*5/12-2,h*7/24-2,w*5/12+2,h*7/24+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*6/7-2,h*6/17-2,w*6/7+2,h*6/17+2))
        obstacles.append(GSclasses.Obstacle(canvas,w*7/15-2,h/55-2,w*7/15+2,h/55+2))
    elif (level==12):
        obstacles.append(GSclasses.Obstacle(canvas,0,h*67/140,w*2/3,h*73/140))
        obstacles.append(GSclasses.Obstacle(canvas,w*67/140,h/8,w*73/140,h/2))
        obstacles.append(GSclasses.Obstacle(canvas,w*57/140,h/2,w*63/140,h*9/10))
        obstacles.append(GSclasses.Obstacle(canvas,w*11/15,h*67/140,w,h*73/140))

    canvas.data["obstacles"]=obstacles 

def makeGoals(canvas):#w and h refer to the game, not the canvas
    h=canvas.data["canvasHeight"]
    w=canvas.data["gameWidth"]
    level=canvas.data["level"]
    goals=[]
    if(level==1):
        goals.append(GSclasses.Goal(canvas,w*2/3,h*5/6,w*5/6,h))
    elif(level==2):
        goals.append(GSclasses.Goal(canvas,0,0,w,h/48))
    elif(level==3):
        goals.append(GSclasses.Goal(canvas,0,h/2,w/6,h*3/4))
        goals.append(GSclasses.Goal(canvas,w*7/8,h*7/8,w,h))
    elif(level==4):
        goals.append(GSclasses.Goal(canvas,0,h*5/6,w/7,h))
        goals.append(GSclasses.Goal(canvas,w*6/7,0,w,h/6))
    elif(level==5):
        goals.append(GSclasses.Goal(canvas,0,h*5/6,w/7,h))
        goals.append(GSclasses.Goal(canvas,w*6/7,0,w,h/6))
        goals.append(GSclasses.Goal(canvas,w*6/7,h*5/6,w,h))
    elif(level==6):
        goals.append(GSclasses.Goal(canvas,0,0,w/7,h/3))
        goals.append(GSclasses.Goal(canvas,w*2/7,h*4/9,w*3/7,h*5/9))
        goals.append(GSclasses.Goal(canvas,w*4/7,h*6/9,w*5/7,h*7/9))
    elif(level==7):
        goals.append(GSclasses.Goal(canvas,w*6/7,0,w,h/6))
        goals.append(GSclasses.Goal(canvas,w*5/7,h/2,w*6/7,h*13/24))
    elif(level==8):
        goals.append(GSclasses.Goal(canvas,0,0,w/5,h/5))
        goals.append(GSclasses.Goal(canvas,w/5,0,w*2/5,h/5))
        goals.append(GSclasses.Goal(canvas,w*2/5,0,w*3/5,h/5))
        goals.append(GSclasses.Goal(canvas,w*3/5,0,w*4/5,h/5))
        goals.append(GSclasses.Goal(canvas,w*4/5,0,w,h/5))
        goals.append(GSclasses.Goal(canvas,w*4/5,h/5,w,h*2/5))
        goals.append(GSclasses.Goal(canvas,w*4/5,h*2/5,w,h*3/5))
        goals.append(GSclasses.Goal(canvas,w*4/5,h*3/5,w,h*4/5))
        goals.append(GSclasses.Goal(canvas,w*4/5,h*4/5,w,h))
        goals.append(GSclasses.Goal(canvas,w*3/5,h*4/5,w*4/5,h))
        goals.append(GSclasses.Goal(canvas,w*2/5,h*4/5,w*3/5,h))
        goals.append(GSclasses.Goal(canvas,w*1/5,h*4/5,w*2/5,h))
        goals.append(GSclasses.Goal(canvas,0,h*4/5,w/5,h))
        goals.append(GSclasses.Goal(canvas,0,h*3/5,w/5,h*4/5))
        goals.append(GSclasses.Goal(canvas,0,h*2/5,w/5,h*3/5))
        goals.append(GSclasses.Goal(canvas,0,h/5,w/5,h*2/5))
    elif(level==9):
        goals.append(GSclasses.Goal(canvas,w*57/140,h/2,w*67/140,h*3/5))
        goals.append(GSclasses.Goal(canvas,0,h/3,w/7,h*32/70))
    elif(level==10):
        goals.append(GSclasses.Goal(canvas,w/10,h/10,w*3/20,h*3/20))
        goals.append(GSclasses.Goal(canvas,w*19/40,h*3/20,w*21/40,h/5))
        goals.append(GSclasses.Goal(canvas,w*17/20,h/10,w*9/10,h*3/20))
        goals.append(GSclasses.Goal(canvas,w*17/20,h*17/20,w*9/10,h*9/10))
        goals.append(GSclasses.Goal(canvas,w*19/40,h*4/5,w*21/40,h*17/20))
        goals.append(GSclasses.Goal(canvas,w/10,h*17/20,w*3/20,h*9/10))
    elif(level==11):
        goals.append(GSclasses.Goal(canvas,0,0,w/7,h/6))
        goals.append(GSclasses.Goal(canvas,w*6/7,0,w,h/6))
        goals.append(GSclasses.Goal(canvas,w*6/7,h*5/6,w,h))
        goals.append(GSclasses.Goal(canvas,0,h*5/6,w/7,h))
    elif(level==12):
        goals.append(GSclasses.Goal(canvas,w/4,h*67/140-h/15,w*19/60,h*67/140))
        goals.append(GSclasses.Goal(canvas,w*67/140-w/15,h/8,w*67/140,h*23/120))
        goals.append(GSclasses.Goal(canvas,w*73/140,h*67/140-h/15,w*73/140+w/15,h*67/140))
        goals.append(GSclasses.Goal(canvas,w*14/15,h*67/140-h/15,w,h*67/140))
        goals.append(GSclasses.Goal(canvas,w/2,h*2/3,w*17/30,h*11/15))
        goals.append(GSclasses.Goal(canvas,w*5/6,h*3/4,w*9/10,h*49/60))
        goals.append(GSclasses.Goal(canvas,0,h*14/15,w/15,h))
        goals.append(GSclasses.Goal(canvas,w*57/140-w/15,h*73/140,w*57/140,h*73/140+h/15))
    canvas.data["goals"]=goals

##### drawGame #####

def drawGame(canvas):
    drawBackground(canvas)
    doObstacles(canvas)
    drawHelpText(canvas)
    drawGoals(canvas)

def drawBackground(canvas):
    w=canvas.data["gameWidth"]
    h=canvas.data["canvasHeight"]
    canvas.data["background"]=canvas.create_rectangle(0,0,w,h,
                                                      fill="black",width=0)


def drawHelpText(canvas):
    level=canvas.data["level"]
    w=canvas.data["gameWidth"]
    h=canvas.data["canvasHeight"]
    if (level<4):
        font=("Calibri",h/40)
        if (level==1):
            x=w/8
            y=h/8
            fill="light green"
            msg="""Gravitiles push things that are touching them. Click and
drag them into play to direct the ball into the goal.
Press s to run and reset the simulation, and r to restart the level.
Note: you cannot move tiles while the game is playing."""
        elif (level==2):
            x=w*7/12
            y=h*3/4
            fill="dark blue"
            msg="""The purple tiles over there are
stronger than gravity, especially
when they work as a team..."""
        else: #level==3
            x=w/16
            y=h*11/30
            fill="dark blue"
            msg="""To return to the menu, press m. To remove
a tile from play, right click on it. Good Luck!"""
        canvas.create_text(x,y,text=msg,font=font,fill=fill,anchor="nw")

def drawGoals(canvas):
    for goal in canvas.data["goals"]:
        goal.draw()

def drawBalls(canvas):
    for ball in canvas.data["balls"]:
        ball.draw()

##### drawSidebar #####

def drawSidebar(canvas):
    drawSidebarBackground(canvas)
    drawButtons(canvas)
    drawTiles(canvas)

def drawSidebarBackground(canvas):
    gW=canvas.data["gameWidth"]
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    #background
    canvas.create_rectangle(gW,0,w,h,width=0,fill="midnight blue")
    #title
    text="Gravishift"
    fill="white"
    font=("Courier",h/25,"italic")
    canvas.create_text(w*8/9,h/25,text=text,fill=fill,font=font)
    #your score
    text="score:"+str(canvas.data["score"])
    font=("Calibri",h/50)
    canvas.data["scoreText"]=canvas.create_text(w*15/18,h*2/25,text=text,
                                                fill=fill,font=font)
    #my score
    text="pro score:"+str(canvas.data["proScores"][canvas.data["level"]])
    canvas.create_text(w*17/18,h*2/25,text=text,fill=fill,font=font)

def drawButtons(canvas):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    buttons=[]
    restartButton=GSclasses.Button(canvas,w*8/9,h*3/20,w/5,h/12,"restart",-1)
    restartButton.usable=True
    restartButton.draw()
    buttons.append(restartButton)
    startStopButton=GSclasses.Button(canvas,w*8/9,h*4/15,
                                     w/5,h/12,"startStop",-1)
    startStopButton.usable=True
    startStopButton.draw()
    buttons.append(startStopButton)
    canvas.data["buttons"]=buttons

def drawTiles(canvas):
    for tile in canvas.data["tiles"]:
        tile.draw()        

#################################################

def doMenu(canvas):
    drawMenuBackground(canvas)
    makeTitle(canvas)
    makeMenuHelpText(canvas)
    makeMenuTiles(canvas)
    (rows,cols)=(4,3)
    makeLevelSelectionButtons(canvas,rows,cols)

def drawMenuBackground(canvas):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    canvas.create_rectangle(0,0,w,h,fill="black",width=0)
    canvas.create_rectangle(w/24,h/4,w*11/24,h*15/16,fill="midnight blue")
    canvas.create_rectangle(w/2,h/4,w*23/24,h*3/4,fill="midnight blue")

def makeTitle(canvas):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    text="Gravishift"
    font=("Courier",w/8,"italic")
    canvas.create_text(w/2,h/8,text=text,fill="grey",font=font)

def makeMenuHelpText(canvas):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    font=("Sans",w/60)
    msg1="""Welcome to Gravishift, a game of precision
and inspiration! Place Gravitiles like the
ones shown below to launch the ball through
the targets. How few do you need to win?"""
    canvas.create_text(w*49/96,h*25/96,text=msg1,fill="white",font=font,anchor="nw")
    msg2="""When in-game, navigate between levels by
pressing n(ext) and p(revious). To return to
this screen, press m."""
    canvas.create_text(w*49/96,h*45/96,text=msg2,fill="white",font=font,anchor="nw")
    msg3="""Unlocked levels are grey, and turn gold if you
match or beat my high score. Well don't just
sit there: pick one and get started!"""
    canvas.create_text(w*49/96,h*61/96,text=msg3,fill="white",font=font,anchor="nw")

def makeMenuTiles(canvas):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    tWidth=w/12
    tHeight=tWidth
    x=(w+tWidth)/2
    margin=tWidth/2
    y=h*3/4+margin+tWidth/2
    tile0=GSclasses.Tile(canvas,x,y,tWidth,tHeight,"up")
    tile1=GSclasses.Tile(canvas,x+1*(tWidth+margin),y,tWidth,tHeight,"right")
    tile2=GSclasses.Tile(canvas,x+2*(tWidth+margin),y,tWidth,tHeight,"down")
    tile3=GSclasses.Tile(canvas,x+3*(tWidth+margin),y,tWidth,tHeight,"left")
    tile0.draw()
    tile1.draw()
    tile2.draw()
    tile3.draw()
    tiles=[]
    canvas.data["tiles"]=[tile0,tile1,tile2,tile3]

def makeLevelSelectionButtons(canvas,rows,cols):
    w=canvas.data["canvasWidth"]
    h=canvas.data["canvasHeight"]
    buttons=canvas.data["buttons"]
    highScores=canvas.data["highScores"]
    proScores=canvas.data["proScores"]
    lastBeatenLevelNotSeen=True
    i=1
    left=w/24
    top=h/4
    right=w*11/24
    botom=h*15/16
    deltaX=w*5/12
    deltaY=h*11/16
    xMargin=deltaX/75
    width=(deltaX-(xMargin*(cols+1)))/cols#width*(cols)+xMargin*(cols+1)=deltaX
    height=width/3
    yMargin=(deltaY-(height*rows))/(rows+1)#similar to above equation
    for row in xrange(rows):
        for col in xrange(cols):
            x=left+xMargin+width/2+(width+xMargin)*col
            y=top+yMargin+height/2+(height+yMargin)*row
            ithLevelButton=GSclasses.Button(canvas,x,y,width,height,"level",i)
            if lastBeatenLevelNotSeen:
                ithLevelButton.usable=True
                if (highScores[i]>8):lastBeatenLevelNotSeen=False
            else: ithLevelButton.usable=False
            if (highScores[i]<=proScores[i]):ithLevelButton.proScore=True
            ithLevelButton.draw()
            buttons.append(ithLevelButton)
            i+=1
    canvas.data["buttons"]=buttons
