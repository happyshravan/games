#Michael Choquette, mchoquet
#MissileCommand.py
#This file contains the Tkinter version of Missile Command

from Tkinter import *
import random

#################################
####### user interaction ########
#################################

def mousePressed(event):
    canvas=event.widget.canvas

def keyPressed(event):
    canvas=event.widget.canvas

def mouseMoved(event):
    canvas=event.widget.canvas

#################################
########### animation ###########
#################################

def timerFired(canvas,counter=0):
    pass

#################################
########### redrawAll ###########
#################################

def redrawAll(canvas):
    pass


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

#This function finds the 9 locations that the missiles
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
    canvas.data["missiles"]=[] #the missiles on the screen
    canvas.data["explosions"]=[] #the explosions on the screen
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
