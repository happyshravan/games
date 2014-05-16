#GraviShift
#Michael Choquette, mchoquet
#This is a gravity shifting puzzle game.

###############
#post-submission
    #more levels?

from Tkinter import *
import GSclasses ### making the items
import GSlevels ### drawing the game
import GSscores ### preserving information between plays
import math


####################
### ball motion ####
####################

def checkGoals(canvas,ball,x,y,endX,endY):
    noGoalsLeft=True
    for goal in canvas.data["goals"]:
        if (not goal.achieved):
            if goal.intersection(ball,x,y,endX,endY):
                goal.achieve()
            else:
                noGoalsLeft=False
    if noGoalsLeft: canvas.data["won"]=True

def firstCollisionPoint(collPoints):
    minTime=1
    minIndex=0
    i=0
    for (collx,colly,theta,time) in collPoints:
        if time<minTime:
            minTime=time
            minIndex=i
        i+=1
    (collx,colly,theta,time)=collPoints[minIndex]
    return (collx,colly,theta,time)

def postCollisionPosition(canvas,ball,x,y,timeLeft=1.0):
    vx=ball.vx
    vy=ball.vy
    (endX,endY)=(x+vx*timeLeft,y+vy*timeLeft)
    if ((timeLeft==0)or(vx==vy==0)): return (endX,endY)
    collisionPoints=[]
    for obstacle in canvas.data["obstacles"]: #finds all collisions on the line
        intersectionStats=obstacle.firstIntersection(x,y,endX,endY,ball.radius)
        if intersectionStats!=None:collisionPoints.append(intersectionStats)
    if (len(collisionPoints)==0): #base case: no more collisions on this path
        ball.drawPath(x,y,endX,endY)
        checkGoals(canvas,ball,x,y,endX,endY)
        return (endX,endY)
    else: #recursive case
        (collX,collY,theta,time)=firstCollisionPoint(collisionPoints)       
        ball.drawPath(x,y,collX,collY)
        checkGoals(canvas,ball,x,y,collX,collY)
        if (vx==0):timeLeft*=((endY-collY)/(endY-y))
        else:
            timeLeft*=((endX-collX)/(endX-x))
        #modify vx and vy based on theta
        if (theta==0): #otherwise trig will cause a rounding error
            ball.vx=vx
            ball.vy=vy*-0.85
        elif (theta==math.pi/2):
            ball.vx=vx*-0.85
            ball.vy=vy
        else:
            v=(vx,vy)
            vMag=math.sqrt(vx**2+vy**2)
            try:
                alpha=math.atan(vy/vx)+theta
            except:
                alpha=math.pi/2
            beta=math.pi/2-alpha
            reflectionVector=(math.cos(math.pi/2-theta),math.sin(math.pi/2-theta))
            #to get vPerp, dot project v onto the reflection vector (it's a unit vector)
            dotProduct=v[0]*reflectionVector[0]+v[1]*reflectionVector[1]
            vPerp=(reflectionVector[0]*dotProduct,reflectionVector[1]*dotProduct)
            vTan=(v[0]-vPerp[0],v[1]-vPerp[1])
            ball.vx=vTan[0]-0.85*vPerp[0]
            ball.vy=vTan[1]-0.85*vPerp[1]
        return postCollisionPosition(canvas,ball,collX,collY,timeLeft)

def moveBall(canvas,ball):
    #calculates the velocity based on forces and whether or not its rolling
    (xForce,yForce)=findForces(canvas,ball)
    vx=ball.vx+xForce
    vy=ball.vy+yForce
    if (ball.rolling[0]==True):
        vx*=0.985
        vy=0
        if (abs(vx)<0.2):
            vx=0
            ball.atRest=True
        if stoppedRolling(canvas,ball):
            ball.rolling=(False,None)
    if (ball.rolling==(False,None)):
        (floor,rolling,obstacle)=startedRolling(canvas,ball,vx,vy)
        if rolling:
            y=ball.location()[1]
            ball.move(0,floor-y)
            ball.drawPath()
            vy=0
            ball.rolling=(True,obstacle)
    ball.vx=vx
    ball.vy=vy

    #move the ball
    (x,y)=ball.location()
    (endX,endY)=postCollisionPosition(canvas,ball,x,y)
    ball.move(endX-x,endY-y)


def stoppedRolling(canvas,ball):
    (xForce,yForce)=findForces(canvas,ball)
    obstacle=ball.rolling[1]
    (x,y)=ball.location()
    (left,top,right,bottom)=obstacle.coords
    if (((x)<left)or((x)>right)or(yForce!=canvas.data["gravity"])): return True
    return False

def startedRolling(canvas,ball,vx,vy):
    (x,y)=ball.location()
    r=ball.radius
    for obstacle in canvas.data["obstacles"]:
        if (not obstacle.complex):
            (left,top,right,bottom)=obstacle.coords
            if ((x>=left)and(x<=right)and((x+vx)>=left)and((x+vx)<=right)
                and ((y+r)>(top-2)) and((y+r)<=top)and(vy<=3.5)and(vy>0)):
                return (top-r-1,True,obstacle)
    return (1,False,None)


######################
##### animation ######
######################

def inRect(x,y,left,top,right,bottom):
    return ((x>left)and(x<right)and(y>top)and(y<bottom))

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def inCircle(x,y,cx,cy,r):
    return (distance(x,y,cx,cy)<r)

def ballInRegion(region,x,y,r):
    (left,top,right,bottom)=region.coords
    return(inRect(x,y,left-r,top,right+r,bottom) or
           inRect(x,y,left,top-r,right,bottom+r) or
           inCircle(x,y,left,top,r) or inCircle(x,y,right,top,r) or
           inCircle(x,y,left,bottom,r) or inCircle(x,y,right,bottom,r))

def findForces(canvas,ball):
    fX=0
    fY=canvas.data["gravity"]
    (x,y)=ball.location()
    r=ball.radius
    for tile in canvas.data["tiles"]:
        if ballInRegion(tile,x,y,r):
            (pushX,pushY)=tile.force
            fX+=pushX
            fY+=pushY
    return (fX,fY)

def timerFired(canvas):
    balls=canvas.data["balls"]
    #if they haven't already won, check to see if it's hit any new goals
    if ((canvas.data["won"])and(canvas.data["victoryText1"]==None)):
        width=canvas.data["gameWidth"]
        height=canvas.data["canvasHeight"]
        text1="You Won!"
        font1=("Helvetica",height/5)
        canvas.data["victoryText1"]=canvas.create_text(width/2,height/2,
                                                      text=text1,font=font1,
                                                      fill="green")
        text2="""n for next level
p for previous
m for menu"""
        font2=("Helvetica",height/24)
        canvas.data["victoryText2"]=canvas.create_text(width/2,height*17/24,
                                                       text=text2,font=font2,
                                                       fill="red")
        GSscores.checkScore(canvas)
    #note: the game keeps playing if you've won
    if canvas.data["GAMEON"]:
        delay=20
        #find the ball speed
        for ball in balls:
            if not ball.atRest:
                moveBall(canvas,ball)
            
            #move the ball
            
        #note: if the game is not on, THE TIMER STOPS
        canvas.after(delay,timerFired,canvas)

def animateTiles(canvas):
    for tile in canvas.data["tiles"]:
        if tile.inPlay: tile.animate()
    delay=100
    canvas.after(delay,animateTiles,canvas)

def resetGoals(canvas):
    for goal in canvas.data["goals"]:
        if goal.achieved:goal.unachieve()
        canvas.lift(goal.goal)
    canvas.data["won"]=False


######################
## user interaction ##
######################

def doButtonAction(canvas,button):
    if (button.type=="startStop"):
        if canvas.data["GAMEON"]:doStop(canvas)
        else:
            doStart(canvas)
    elif (button.type=="restart"):
          useSavedTileSpots=False
          init(canvas,useSavedTileSpots)
    elif (button.type=="level"):
        canvas.data["level"]=button.level
        init(canvas)

def mousePressed(event):
    canvas=event.widget.canvas
    x=event.x
    y=event.y
    canvas.data["lastMouse"]=(x,y)
    if canvas.data["level"]!=0:
        if (not canvas.data["GAMEON"]):
            for tile in reversed(canvas.data["tiles"]): #reversed so it picks the top tile
                (left,top,right,bottom)=tile.coords
                if inRect(x,y,left,top,right,bottom):
                    canvas.data["chosenTile"]=tile
                    canvas.data["xDisp"]=tile.x-x
                    canvas.data["yDisp"]=tile.y-y
                    break
    for button in canvas.data["buttons"]:
        (left,top,right,bottom)=button.coords
        if (inRect(x,y,left,top,right,bottom)and(button.usable)):
            doButtonAction(canvas,button)
            break

def mouseMoved(event):
    canvas=event.widget.canvas
    tile=canvas.data["chosenTile"]
    if tile!=None:
        (newX,newY)=(event.x,event.y)
        (lastX,lastY)=(tile.x,tile.y)
        xDisp=canvas.data["xDisp"]
        yDisp=canvas.data["yDisp"]
        newX+=xDisp
        newY+=yDisp
        tileWidth=tile.width
        tileHeight=tile.height
        if tile.inPlay: # it's still O(n), however ugly this is...
            for obstacle in canvas.data["obstacles"]:
                if (not obstacle.complex):
                    (left,top,right,bottom)=obstacle.coords
                    left-=tileWidth/2
                    right+=tileWidth/2
                    top-=tileHeight/2
                    bottom+=tileHeight/2
                    if (inRect(newX,newY,left,top,right,bottom)):
                        if(lastX<=left): newX=left
                        elif(lastX>=right): newX=right
                        if(lastY<=top): newY=top
                        elif(lastY>=bottom): newY=bottom
            goodSpot=True
            for obstacle in canvas.data["obstacles"]:
                if (not obstacle.complex):
                    (left,top,right,bottom)=obstacle.coords
                    left-=tileWidth/2
                    right+=tileWidth/2
                    top-=tileHeight/2
                    bottom+=tileHeight/2
                    if (inRect(newX,newY,left,top,right,bottom)):
                        goodSpot=False
                        break
            if goodSpot:tile.moveTo(newX,newY)
        else: #it doesn't recognise the obstacles if the tile isn't in play
            newX=max(newX,tileWidth/2)#left bound
            newY=max(newY,tileHeight/2)#top bound
            newY=min(newY,canvas.data["canvasHeight"]-tileHeight/2)#bottom bound
            newX=min(newX,canvas.data["canvasWidth"]-tileWidth/2)#right bound
            tile.moveTo(newX,newY)

def mouseReleased(event):
    canvas=event.widget.canvas
    tile=canvas.data["chosenTile"]
    if tile!=None:
        if(not tile.inPlay):
            x=tile.x
            y=tile.y
            tWidth=tile.width
            tHeight=tile.height
            badMove=False
            for obstacle in canvas.data["obstacles"]:
                if (not obstacle.complex):
                    (left,top,right,bottom)=obstacle.coords
                    left-=tWidth/2
                    right+=tWidth/2
                    top-=tHeight/2
                    bottom+=tHeight/2
                    if inRect(x,y,left,top,right,bottom):
                        tile.moveTo(tile.homeX,tile.homeY)
                        badMove=True
                        break
            if (not badMove):
                tile.inPlay=True
                canvas.data["score"]+=1
                text="score:"+str(canvas.data["score"])
                scoreText=canvas.data["scoreText"]
                canvas.itemconfig(scoreText,text=text)
        GSscores.saveTiles(canvas)
    canvas.data["chosenTile"]=None
    canvas.data["lastMouse"]=(None,None)

def rightMousePressed(event):
    canvas=event.widget.canvas
    if ((canvas.data["level"]!=0)and(not canvas.data["GAMEON"])):
        x=event.x
        y=event.y
        #finding the tile clicked on
        for tile in canvas.data["tiles"]:
            if tile.inPlay:
                (left,top,right,bottom)=tile.coords
                if inRect(x,y,left,top,right,bottom):
                    #reset the tile's position
                    homeX=tile.homeX
                    homeY=tile.homeY
                    tile.moveTo(homeX,homeY)
                    tile.inPlay=False
                    tile.resetChev()#so that the animation didn't freeze weirdly
                    #decrementing score as a result of tile removal
                    canvas.data["score"]-=1
                    text="score:"+str(canvas.data["score"])
                    scoreText=canvas.data["scoreText"]
                    canvas.itemconfig(scoreText,text=text)
                    #saving the new position
                    GSscores.saveTiles(canvas)
                    break

def doStart(canvas):
    canvas.data["GAMEON"]=True
    for pathLine in canvas.find_withtag("path"): #erase the path
        canvas.delete(pathLine)
    timerFired(canvas) #start the timer again

def doStop(canvas):
    #reset the balls
    for ball in canvas.data["balls"]:
        canvas.delete(ball.ball)
    GSlevels.makeBalls(canvas)
    GSlevels.drawBalls(canvas)
    canvas.data["GAMEON"]=False #ends the timerFired
    canvas.delete(canvas.data["victoryText1"])
    canvas.delete(canvas.data["victoryText2"])
    canvas.data["victoryText1"]=None
    canvas.data["victoryText2"]=None
    #change the path color
    for pathLine in canvas.find_withtag("path"): 
        canvas.itemconfig(pathLine,fill="dark grey")
    resetGoals(canvas)
    for tile in canvas.data["tiles"]:
        tile.resetChev()

def keyPressed(event):
    canvas=event.widget.canvas
    key=event.char
    level=canvas.data["level"]
    if ((key=="s")and(level>0)and(canvas.data["chosenTile"]==None)):
        if canvas.data["GAMEON"]:doStop(canvas)
        else:
            doStart(canvas)
    elif (key=="r"):
        useSavedTileSpots=False
        init(canvas,useSavedTileSpots)
    elif ((key=="m")and(level>0)):
        canvas.data["level"]=0
        init(canvas)
    elif ((key=="n")and(canvas.data["won"])and(level<12)):
        canvas.data["level"]+=1
        init(canvas)# GO TO NEXT LEVEL
    elif ((key=="p")and(canvas.data["won"])):
        canvas.data["level"]-=1
        init(canvas)# GO TO PREVIOUS LEVEL

######################
######## init ########
######################

def init(canvas,useSavedTileSpots=True):
    canvas.delete(ALL)
    canvas.data["gameWidth"]=canvas.data["canvasWidth"]*7/9
    canvas.data["gravity"]=1
    canvas.data["GAMEON"]=False
    canvas.data["won"]=False
    canvas.data["victoryText1"]=None
    canvas.data["victoryText2"]=None
    canvas.data["chosenTile"]=None
    canvas.data["xDisp"]=None
    canvas.data["yDisp"]=None
    canvas.data["buttons"]=[]
    canvas.data["score"]=0
    level=canvas.data["level"]
    GSlevels.doLevel(canvas,useSavedTileSpots)
        
def run():
    root=Tk()
    canvasWidth=900
    canvasHeight=canvasWidth*2/3
    canvas=Canvas(root,width=canvasWidth,height=canvasHeight)
    canvas.pack()
    canvas.canvas=root.canvas=canvas
    canvas.data={}
    canvas.data["canvasWidth"]=canvasWidth
    canvas.data["canvasHeight"]=canvasHeight
    canvas.data["level"]=0
    canvas.data["levels"]=12
    #gathering score info that lasts between games
    GSscores.loadHighScores(canvas)
    GSscores.setProScores(canvas)
    init(canvas)
    animateTiles(canvas)
    root.bind("<Button-1>", mousePressed)
    root.bind("<Button-3>", rightMousePressed)
    root.bind("<B1-Motion>", mouseMoved)
    root.bind("<ButtonRelease-1>", mouseReleased)
    root.bind("<Key>",keyPressed)
    root.mainloop()

run()
