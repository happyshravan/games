#Michael Choquette, mchoquet
#MissileCommand.py
#This file contains the Tkinter version of Missile Command

from Tkinter import *
import random

#Not counting comments, my solution to this assignment comes out to ~250 lines
#of code, none of which is particularly complicated. Given sufficiently
#comprehensive instructions, this should be completely achievable in a week.

#################################
####### user interaction ########
#################################

#1. If the game's over, ignore user interaction.
#2. If the game hasn't started, start it.
#3. If you're in between levels, go to the next one
def mousePressed(event): #click to launch missiles
    canvas=event.widget.canvas
    if canvas.data["gameOver"]: pass
    elif canvas.data["startedGame"]==False: #in pregame
        (canvas.data["startedGame"],canvas.data["inLevel"])=(True,True)
        canvas.data["level"]=1
        runLevel(canvas)
    elif canvas.data["inLevel"]==False: #between levels
        canvas.data["level"]+=1
        canvas.data["inLevel"]=True
        #restock the missiles before each level starts
        canvas.data["missilesLeft"]=[20]*3
        runLevel(canvas)


#r restarts outside of a level, and 1,2,3 shoot missiles in a level
def keyPressed(event):
    canvas=event.widget.canvas
    if event.char=="r" and not canvas.data["inLevel"]: init(canvas)
    elif event.char in "123" and canvas.data["inLevel"]:
        siloNum=int(event.char)-1
        missilesLeft=canvas.data["missilesLeft"]
        #if you have ammo and a reason, you may shoot :)
        if missilesLeft[siloNum]>0 and not gameLost(canvas): 
            (startX,startY)=canvas.data["missileTargets"][siloNum]            
            (endX,endY)=(canvas.data["mouseX"],canvas.data["mouseY"])
            missileSpeed=canvas.data["size"]*3/64 #default speed is 40
            launchMissile(canvas,(startX,startY),
                          (endX,endY),missileSpeed,"blue")
            #remove the launched missile from your stores
            missilesLeft[siloNum]-=1        

#moves your crosshairs, then redraws everything to show the change
def mouseMoved(event):
    canvas=event.widget.canvas
    canvas.data["mouseX"]=event.x
    canvas.data["mouseY"]=min(event.y,canvas.data["size"]*4/5)
    redrawAll(canvas)


#################################
########### runLevel ############
#################################

#Missile Command is inherently split into levels of indeterminate length, so
#I chose to to call timerFired (here runLevel) for every level separately, and
#not have one running the whole time in the background. My hunch is that this
#is the clearest way; at least, it's the best way I've found.

#To avoid infinite loops, it only fires missiles if a target exists. Then it
#moves existing missiles, modifies existing explosions, checks to see if any of
#your targets have been destroyed, and checks to see if the level is over yet
def runLevel(canvas,counter=0):
    if aTargetExists(canvas) and (counter in (50,150,250)):
        launchEnemyMissiles(canvas)
    moveMissiles(canvas)
    growExplosions(canvas)
    checkMissiles(canvas)
    checkTargets(canvas)
    redrawAll(canvas)
    if levelHasEnded(canvas,counter):
        canvas.data["inLevel"]=False
        if gameLost(canvas):canvas.data["gameOver"]=True
        else:
            updateScore(canvas)
        redrawAll(canvas) #so that the between-level text is drawn right away
    else:
        delay=20
        canvas.after(delay,runLevel,canvas,counter+1)

#returns True if a city stands or a silo has a missile in it
def aTargetExists(canvas):
    return (True in canvas.data["standingCities"] or
            canvas.data["missilesLeft"].count(0)<3)

#HARDCODING WARNING: the last missiles are spawned when counter==250
def levelHasEnded(canvas,counter):
    return (counter>250 and len(canvas.data["missiles"])==0 and
            len(canvas.data["explosions"])==0)

#The game is over of none of your cities are standing
def gameLost(canvas):
    return not True in canvas.data["standingCities"]

#The missiles come in 3 waves per level. The 3 waves in each level are the same,
#but all the waves get harder as the level increases. Note: the s/640 is just
#a scale factor: we want missiles to move slower on a smaller screen.
def launchEnemyMissiles(canvas):
    (s,level)=(canvas.data["size"],canvas.data["level"])
    missileSpeed=(level+1)/2*s/640
    missileCount=5+level/2
    missileTargets=canvas.data["missileTargets"]
    for i in xrange(missileCount):
        startX=random.randint(0,s)
        (endX,endY)=missileTargets[chooseTarget(canvas)]
        launchMissile(canvas,(startX,0),(endX,endY),missileSpeed,"red")

#Chooses a city/silo at random until it finds one that's standing
def chooseTarget(canvas):
    while True:
        target=random.randint(0,8)
        if target<3 and canvas.data["missilesLeft"][target]>0:return target
        elif target>=3 and canvas.data["standingCities"][target-3]:return target

#Initializes a missile, using unit vectors to get the right missile speed 
def launchMissile(canvas,(startX,startY),(endX,endY),missileSpeed,color):
    (dx,dy)=(endX-startX,endY-startY)
    distance=(dx**2+dy**2)**0.5
    (vx,vy)=(dx*missileSpeed/distance,dy*missileSpeed/distance)
    canvas.data["missiles"].append([startX,startY,startX,startY, #start,current
                                    endX,endY,vx,vy,color]) #end,speed,color

#Moves all the missiles
def moveMissiles(canvas):
    for missile in canvas.data["missiles"]:
        moveMissile(missile)

#Destructively modifies the missile's coordinates
def moveMissile(missile):
    missile[2]+=missile[6] #currentX += vX
    missile[3]+=missile[7] #currentY += vY        

#moves all the explosions one step forward: they start at 0, grow to 50,
#shrink to 0 again, and vanish. 
def growExplosions(canvas):
    explosions=canvas.data["explosions"]
    maxRadius=50*canvas.data["size"]/640 #default size: 50
    for i in xrange(len(explosions)-1,-1,-1): #so that I can remove as I go
        (cx,cy,r,isGrowing)=explosions[i]
        if isGrowing:
            r+=1.5
            if r>maxRadius: isGrowing=False #now it shrinks
        else:
            r-=1.5
        if r<=0: explosions.pop(i)
        else:
            explosions[i]=(cx,cy,r,isGrowing)

#This explodes any missiles that reach their targets or are hit on the way
def checkMissiles(canvas):
    missiles=canvas.data["missiles"]
    for i in xrange(len(missiles)-1,-1,-1): #so that I can remove as I go
        missile=missiles[i]
        (x,y)=(missile[2],missile[3])
        if inExplosion(canvas,x,y) or atTarget(missile):
            explode(canvas,x,y)
            missiles.pop(i)

#Finds if the point (here the coords of a missile or city) is in an explosion
def inExplosion(canvas,x,y):
    for (cx,cy,r,isGrowing) in canvas.data["explosions"]:
        if pointInCircle(cx,cy,r,x,y): return True
    return False

#Just the equation for a circle with a < tacked onto the =
def pointInCircle(cx,cy,r,x,y):
    return ((x-cx)**2+(y-cy)**2)<=r**2

#This determines whether or not a missile has reached its target (within error)
#This way works on the assumption that v is nonzero
def atTarget((startX,startY,currentX,currentY,endX,endY,vX,vY,color)):
    return (currentX-endX)*vX>=0 and (currentY-endY)*vY>=0

#This initializes an explosion at a certain point
def explode(canvas,cX,cY):
    canvas.data["explosions"].append([cX,cY,0,True]) #r=0, and it's growing

#This checks to see if any of the 9 targets have just been hit by a missile
def checkTargets(canvas):
    missileTargets=canvas.data["missileTargets"]
    missilesLeft=canvas.data["missilesLeft"]
    standingCities=canvas.data["standingCities"]
    #checkSilos
    for i in xrange(3):
        (x,y)=missileTargets[i]
        if inExplosion(canvas,x,y): missilesLeft[i]=0
    #checkCities
    for i in xrange(6):
        (x,y)=missileTargets[i+3]
        if inExplosion(canvas,x,y): standingCities[i]=False

#Finds the new player score given that the score only changes between levels
def updateScore(canvas):
    intactCities=canvas.data["standingCities"].count(True)
    totalMissilesLeft=sum(canvas.data["missilesLeft"])
    multiplier=canvas.data["level"]
    canvas.data["score"]+=multiplier*(100*intactCities+5*totalMissilesLeft)


#################################
########### redrawAll ###########
#################################

#deletes the old screen and draws an updated one over it
def redrawAll(canvas):
    canvas.delete(ALL)
    drawBackground(canvas)
    drawMissiles(canvas)
    drawExplosions(canvas)
    drawText(canvas)
    drawCrosshairs(canvas)

#each missile is a red or blue line going from its source to itc current spot
def drawMissiles(canvas):
    for missile in canvas.data["missiles"]:
        (sX,sY,x,y)=(missile[0],missile[1],missile[2],missile[3])
        color=missile[-1]
        canvas.create_line(sX,sY,x,y,fill=color)

#Each explosion is just a white circle
def drawExplosions(canvas):
    for (cx,cy,r,isGrowing) in canvas.data["explosions"]:
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,width=0,fill="white")

#Writes all the appropriate text to the game screen. Note: this has the same
#structure as mousePressed, and there can be drawing bugs if it's out of order
def drawText(canvas):
    s=int(canvas.data["size"])#create_text needs ints: may cause rounding errors
    if canvas.data["gameOver"]:
        drawGameOverText(canvas,s)
    elif canvas.data["startedGame"]==False:
        drawIntroText(canvas,s)
    elif canvas.data["inLevel"]==False:
        drawBetweenLevelText(canvas,s)
    else: #must be in a level
        drawAmmoText(canvas,s)

#Displays the game over message and your final score
def drawGameOverText(canvas,s):
    (gameOverMsg,gameOverFont)=("Game Over",("courier",s/12))
    summaryMsg=("You lost on level: "+str(canvas.data["level"])+
                "\nYour final score: "+str(canvas.data["score"]))
    summaryFont=("courier",s/40)
    canvas.create_text(s/2,s/3,text=gameOverMsg,font=gameOverFont,fill="white")
    canvas.create_text(s/2,s*2/3,text=summaryMsg,font=summaryFont,fill="white")

#Makes the splash screen and very limited instructions
def drawIntroText(canvas,s):
    name="MISSILE COMMAND"
    nameFont=("Courier",s/16)
    canvas.create_text(s/2,s/3,text=name,font=nameFont,fill="white")
    directions="""Use 1,2, and 3 to switch between your silos.
Between levels, you can restart with r.
Shoot the missiles down!"""
    directionsFont=("Courier",s/48)
    canvas.create_text(s/2,s*2/3,text=directions,
                       font=directionsFont,fill="white")

#draws the info the player gets between levels (level beaten,
#score earned in the last battle, next level number and multiplier)
def drawBetweenLevelText(canvas,s):
    text="Survived level "+str(canvas.data["level"])
    font = ("Courier",s/32)
    canvas.create_text(s/2,s/4,text=text,font=font,fill="white")
    citiesLeft=canvas.data["standingCities"].count(True)
    totalMissilesLeft=sum(canvas.data["missilesLeft"])
    multiplier=canvas.data["level"]
    scoreMsg1=("Saved "+str(citiesLeft)+" cities: +"
               +str(100*citiesLeft)+" (x"+str(multiplier)+") points.")
    scoreMsg2=("Saved "+str(totalMissilesLeft)+" missiles: +"
               +str(5*totalMissilesLeft)+" (x"+str(multiplier)+") points.")
    scoreMsg3="Total score: "+str(canvas.data["score"])+" points."
    scoreMsg=scoreMsg1+"\n"+scoreMsg2+"\n"+scoreMsg3
    scoreMsgFont=("Courier",s/48)
    canvas.create_text(s/2,s/2,text=scoreMsg,font=scoreMsgFont,fill="white")
    text=("Cl1ck to continue to level "+str(1+canvas.data["level"]))
    font=("Courier",s/48)
    canvas.create_text(s/2,s*2/3,text=text,font=font,fill="white")

#This function draws the messages that tell the player they're low/out of ammo.
#Remember: missile silo coordinates are 0-2 in our missileTargets list
def drawAmmoText(canvas,s):
    (lowText,lowFont)=("Low",("courier",s/32,"bold"))
    (outText,outFont)=("Out",("courier",s/32,"bold"))
    missilesLeft=canvas.data["missilesLeft"]
    targets=canvas.data["missileTargets"]
    for i in xrange(3): #3 silos
        if missilesLeft[i]==0:
            targetX=targets[i][0]
            canvas.create_text(targetX,s*35/36,text=outText,
                               font=outFont,fill="red")
        elif missilesLeft[i]<7:
            targetX=targets[i][0]
            canvas.create_text(targetX,s*35/36,text=lowText,
                               font=lowFont,fill="red")

#The crosshairs is a pair of interseting lines
def drawCrosshairs(canvas):
    w=canvas.data["size"]/80 #default: 8/640
    (mouseX,mouseY)=(canvas.data["mouseX"],canvas.data["mouseY"])
    canvas.create_line(mouseX-w,mouseY,mouseX+w,mouseY,fill="blue")
    canvas.create_line(mouseX,mouseY-w,mouseX,mouseY+w,fill="blue")

#15-110 students doing this homework assignment do not need to master
#the code below this line, EXCEPT FOR:
#1. canvas.data["missileTargets"]: the the coordinates of the 9 missile targets,
    #each coordinate pair stored in a tuple according to the following order:
    # the first 3 tuples are the silo coords (ordered left to right) and the
    # other 6 tuples are the city coords (also ordered left to right). 
#2. all of the canvas.data["whatever"]s in init(canvas)
################################################################################
############################## drawBackground ##################################
################################################################################

#see how much better this is because of all that yuck below! See!
def drawBackground(canvas):
    #sky
    canvas.create_rectangle(canvas.data["sky"],width=0,fill="black")
    #terrain
    canvas.create_polygon(canvas.data["terrain"],width=0,fill="yellow")
    #cities
    drawCities(canvas)
    #silos/stored missiles
    drawSilos(canvas)

#draws the standing cities, based on coordinates precalculated in placeCities
def drawCities(canvas):
    cities=canvas.data["cities"]
    standingCities=canvas.data["standingCities"]
    for i in xrange(len(cities)):
        if standingCities[i]: #if the ith city stands, draw it
            (back,mid,front)=cities[i]
            canvas.create_polygon(back,width=0,fill="royalblue")
            canvas.create_polygon(mid,width=0,fill="cyan")
            canvas.create_polygon(front,width=0,fill="lightblue2")

#Draws the remaining stored missiles, based on precalculated coordinates
def drawSilos(canvas):
    missilesLeft=canvas.data["missilesLeft"]
    silos=canvas.data["silos"]
    for siloNum in xrange(len(silos)):
        (silo,missilesInSilo)=(silos[siloNum],missilesLeft[siloNum])
        missilesToDraw=(missilesInSilo+1)/2
        for missileNum in xrange(missilesToDraw):
            canvas.create_polygon(silo[missileNum],width=0,fill="blue")

#####################################
####### precalculateLocations #######
#####################################

#This precalculates the coordinates of all the static objects in the game,
#and it makes the list of locations the enemy will be shooting missiles at.
#A lot of the effort that went here is pointless if you can use delta graphics,
# but it's not fair to ask that of everybody in the class. Oh well!
def precalculateLocations(canvas):
    s=canvas.data["size"]
    #the sky
    canvas.data["sky"]=(0,0,s,s)
    #the terrain
    ground=s*17/18
    (bigW,bigH,smallW,smallH)=placeTerrain(canvas,s,ground)
    #the missiles
    placeStoredMissiles(canvas,s,ground,bigW,bigH)
    #the cities are created every time, but their locations are calculated here
    roughlyPlaceCities(canvas,s,ground,bigW,smallW,smallH)
    #finding where the enemy missiles will be shooting at
    findMissileTargets(canvas)

#Merges the coordinates for the ground and all the mountains into one large
#polygon, and saves it for later use. It also returns some general information
#about the mountains and passes it back so the other helpers can use it.
def placeTerrain(canvas,s,ground):
    (bigH,smallH)=(s/30,s/90) #conveniently, s is already a float
    (bigW,smallW)=(2*s/15,4*s/45)
    terrain=[s,ground, s,s, 0,s, 0,ground]
    terrain.extend(mountainCoords(0,ground,bigW,bigH))
    terrain.extend(mountainCoords((s+bigW-2*smallW)/4,ground,smallW,smallH))
    terrain.extend(mountainCoords((s-bigW)/2,ground,bigW,bigH))
    terrain.extend(mountainCoords((3*s-bigW-2*smallW)/4,ground,smallW,smallH))
    terrain.extend(mountainCoords(s-bigW,ground,bigW,bigH))
    canvas.data["terrain"]=tuple(terrain)
    return (bigW,bigH,smallW,smallH)

#Finds the coordinates of a single mountain, given the box that contains it.
def mountainCoords(startX,startY,width,height): #anchor DL
    return[startX,startY,startX+height,startY-height,
           startX+height*6/5,startY-height*4/5,
           startX+width-height*6/5,startY-height*4/5,
           startX+width-height,startY-height,
           startX+width,startY]

#Calculates the coordinates of all the missile symbols for all 3 silos
#It also finds the exact location of the three silos, so your missiles know
#where to launch from, and their missiles know where to launch at.
def placeStoredMissiles(canvas,s,ground,bigW,bigH):#top-center anchored
    (dx,startY)=((s-bigW)/2,ground-bigH*4/5)
    silos=[]
    siloSpots=[] #where the missiles are launched from, and the count remaining
    for i in xrange(3): #3 silos
        startX=bigW/2+i*dx
        silos.append(placeOneSilo(startX,startY,bigW*3/4,bigH*5/4))
        siloSpots.append((startX,startY))
    canvas.data["silos"]=tuple(silos)
    canvas.data["siloSpots"]=tuple(siloSpots)

#Calculates the coordinates of the 10 missile symbols for a single silo.
def placeOneSilo(startX,startY,maxW,maxH):
    xOffset=maxW/12 #so the missiles can be TL anchored (instead of TC) 
    (dx,dy)=(maxW/3,maxH/3)
    (missileW,missileH)=(dx*5/12,dy*3/2)
    silo=[]
    for row in xrange(4): # missiles arranged in a 1-2-3-4 pyramid
        for col in xrange(row+1):
            silo.append(placeStoredMissile(startX-dx*(row/2.0-col)-xOffset,
                                            startY+dy*row,missileW,missileH))
    return tuple(silo)

#This function returns the coordinates of a silo missile, given x,y,width,height
def placeStoredMissile(x0,y0,mW,mH):
    #the missile is 3 pixels wide and 5 tall
    (x1,x2,x3,y3,y5)=(x0+mW/3,x0+2*mW/3,x0+mW,y0+3*mH/5,y0+mH)
    return(x1,y0, x1,y3, x0,y3, x0,y5, x1,y5, x1,y3,
           x2,y3, x2,y5, x3,y5, x3,y3, x2,y3, x2,y0)

#This function calculates the loction of each city (bottom-left anchored),
#as well as the width and height of the cities, for use in placeCities (below)
def roughlyPlaceCities(canvas,s,ground,bigW,smallW,smallH):
    (cityW,cityH)=(smallW-smallH*12/5,smallH*2.5)
    smallGap=(s-3*bigW-2*smallW-4*cityW)/8.0
    dx=cityW+smallGap+smallH*6/5
    cityPlacingInfo=[(bigW+smallGap,ground)] #x0,y0
    cityPlacingInfo.append((bigW+smallGap+dx,ground-smallH*4/5)) #x1,y1
    cityPlacingInfo.append((bigW+smallGap+2*dx,ground)) #x2,y2
    cityPlacingInfo.append(((s+bigW)/2+smallGap,ground)) #x3,y3
    cityPlacingInfo.append(((s+bigW)/2+smallGap+dx,ground-smallH*4/5)) #x4,y4
    cityPlacingInfo.append((s-bigW-smallGap-cityW,ground)) #x5,y5
    cityPlacingInfo.append((cityW,cityH))
    canvas.data["cityPlacingInfo"]=tuple(cityPlacingInfo)

#This function calculates the 9 locations that the missiles
#may target, and saves them to the canvas for later use
def findMissileTargets(canvas):
    missileTargets=[] #3 silos and 6 cities, in that order, coords in tuples
    for (startX,startY) in canvas.data["siloSpots"]:
        missileTargets.append((startX,startY))
    cityPlacingInfo=canvas.data["cityPlacingInfo"]
    cityW=cityPlacingInfo[-1][0] #last data piece in the info is (cityW,cityH)
    for i in xrange(6): #6 cities
        (startX,startY)=cityPlacingInfo[i]
        missileTargets.append((startX+cityW/2,startY))
    canvas.data["missileTargets"]=tuple(missileTargets)

#####################################
############ placeCities ############
#####################################

#This function generates the full polygonal coordinates for 6 cities, according
#to given positions and sizes, and saves them in the canvas for later use
def placeCities(canvas):
    #cityPlacingInfo is a tuple of city locations, ending with cityW and cityH
    cityPlacingInfo=canvas.data["cityPlacingInfo"]
    (cityW,cityH)=cityPlacingInfo[-1]
    cities=[]
    for i in xrange(6):
        (startX,startY)=cityPlacingInfo[i]
        placeCity(cities,startX,startY,cityW,cityH)
    canvas.data["cities"]=tuple(cities)

#This function takes the box that a city may fill and randomly generates a
#city to fill that space. A city is a set of 3 tuples of coordinates that will,
#when individually entered into create_polygon and superimposed, make a city
def placeCity(cities,startX,startY,cityW,cityH):#anchor DL
    (back,mid,front)=makeCityPlan()
    back=scale(back,cityW,cityH,startX,startY)
    mid=scale(mid,cityW,cityH,startX+cityW/16,startY) #offset by 1 pixel
    front=scale(front,cityW,cityH,startX+cityW/8,startY) #offset by 2 pixels
    cities.append((back,mid,front))

#Turns the city plan into reall coordinates for a polygon on the canvas
def scale(cityPlan,cityW,cityH,startX,startY):    
    (dx,dy,subCity)=(cityW/16,cityH/8,cityPlan[:])
    for i in xrange(len(cityPlan)):
        if i%2==0: subCity[i]=startX+subCity[i]*dx
        else:
            subCity[i]=startY-dy*subCity[i]
    return subCity

#This simulated a pixelated city (retro-graphics style) using three polygons
#a city has 3 rows of buildings with different colors and decreasing size
#the widths are: back:16 pixels, mid:14 pixels, front:12 pixels
#max height is 8
def makeCityPlan():
    back=makeSkyline(16,3,7)
    mid=makeSkyline(14,1,5)
    front=makeSkyline(12,0,3)
    return (back,mid,front)

#generates a random polygon to given specifications
#that looks like a pixelated city skyline  
def makeSkyline(pixelWidth,floor,ceiling):
    skyline=[0]*4*(pixelWidth+1)
    #evens are x coordinates, odds are y coordinates
    for i in xrange(4*(pixelWidth+1)-1): # -1 so the last y coordinate stays 0
        if i%2==0: skyline[i]=i/4 #want:[0,y, 0,y, 1,y, 1,y, ... endX,y, endX,y]
        elif i%4==1: skyline[i]=skyline[i-2] #pair up y values (flat roofs)
        else:
            newFloor=random.randint(floor,ceiling) #encourages height variation
            if skyline[i-2]==newFloor: newFloor=random.randint(floor,ceiling)
            skyline[i]=newFloor
    return skyline

####################################
############### init ###############
####################################

def init(canvas):
    s=canvas.data["size"] #size of the canvas (both width and height)
    (canvas.data["mouseX"],canvas.data["mouseY"])=(s/2,s/2) #mouse location
    canvas.data["missiles"]=[] #the missiles on screen
    canvas.data["explosions"]=[] #the explosions on screen
    canvas.data["missilesLeft"] = [20]*3 #the missiles stored in each silo
    canvas.data["standingCities"]=[True]*6 #holds isStanding values for cities
    canvas.data["startedGame"]=False #whether or not the game has started
    canvas.data["gameOver"]=False #whether or not the game has ended
    canvas.data["inLevel"]=False #whether or not the player is in a level
    canvas.data["score"]=0 #the player's current score
    canvas.data["level"]=0 #the player's current level
    placeCities(canvas)
    redrawAll(canvas)

def run(size=640):
    root=Tk()
    root.resizable(width=False,height=False)
    canvas=Canvas(root,width=size,height=size)
    root.canvas=canvas.canvas=canvas
    canvas.data={}
    canvas.pack()
    canvas.data["size"]=float(size) #avoiding rounding errors
    precalculateLocations(canvas)
    init(canvas)
    root.bind("<Button-1>",mousePressed)
    root.bind("<Motion>",mouseMoved)
    root.bind("<Key>",keyPressed)
    root.mainloop()

run()
