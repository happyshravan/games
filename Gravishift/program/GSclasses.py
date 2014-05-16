#Michael Choquette
#These are the classes for the game GraviShift.

import random
import math

class Ball():
    def __init__(self,canvas,x,y,r,pathColor="blue"):
        self.canvas=canvas
        self.radius=r
        self.vx=0
        self.vy=0
        self.lastLocation=(x,y)
        self.pathColor=pathColor
        self.rolling=(False,None)
        self.atRest=False

    def location(self):
        canvas=self.canvas
        (left,top,right,bottom)=canvas.coords(self.ball)
        return ((left+right)/2.0,(top+bottom)/2.0)

    def draw(self):
        canvas=self.canvas
        r=self.radius
        (x,y)=self.lastLocation
        self.ball=canvas.create_oval(x-r,y-r,x+r,y+r,width=0,fill="white")
        
    def move(self,dx,dy):
        canvas=self.canvas
        canvas.move(self.ball,dx,dy)

    def drawPath(self,lastX=None,lastY=None,newX=None,newY=None):
        #draw the path
        canvas=self.canvas
        pathColor=self.pathColor
        if (lastX==None):
            (lastX,lastY)=self.lastLocation
            (newX,newY)=self.location()
        line=canvas.create_line(lastX,lastY,newX,newY,width=2,fill=pathColor)
        canvas.itemconfig(line,tag="path")
        canvas.lift(self.ball)
        self.lastLocation=(newX,newY)

############################

class Tile():
    def __init__(self,canvas,x,y,width,height,direction):
        self.canvas=canvas
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.homeX=x
        self.homeY=y
        self.coords=(x-width/2,y-height/2,x+width/2,y+height/2)
        self.direction=direction
        self.inPlay=False
        self.setForce()
        self.setColor()

    def setForce(self):
        direction=self.direction
        canvas=self.canvas
        gravity=canvas.data["gravity"]
        if direction=="up": self.force=(0,-2.5*gravity)
        elif direction=="right": self.force=(2.5*gravity,0)
        elif direction=="down": self.force=(0,2.5*gravity)
        elif direction=="left": self.force=(-2.5*gravity,0)

    def setColor(self):
        direction=self.direction
        if direction=="up": self.color="purple"
        elif direction=="right": self.color="yellow"
        elif direction=="down": self.color="light blue"
        elif direction=="left": self.color="orange"

    def drawBox(self):
        canvas=self.canvas
        (left,top,right,bottom)=self.coords
        direction=self.direction
        color=self.color
        self.box=canvas.create_rectangle(left,top,right,bottom,stipple="gray25",
                                         fill=color,outline=color)

    def getChevCoords(self):
        height=self.height
        width=self.width
        x=self.x
        y=self.y
        direction=self.direction
        if (direction=="up"):
            distToSide=width/2
            distToFront=-height/10+1
        elif (direction=="down"):
            distToSide=width/2
            distToFront=height/10-1
        elif (direction=="right"):
            distToSide=height/2
            distToFront=width/10-1
        elif (direction=="left"):
            distToSide=height/2
            distToFront=-width/10+1
        if ((direction=="up") or (direction=="down")):
            frontX=x
            frontY=y+distToFront
            wing1X=frontX-distToSide
            wing2X=frontX+distToSide
            wing1Y=wing2Y=y-distToFront
        elif((direction=="right") or (direction=="left")):
             frontY=y
             frontX=x+distToFront
             wing1Y=frontY-distToSide
             wing2Y=frontY+distToSide
             wing1X=wing2X=x-distToFront
        return (frontX,frontY,wing1X,wing1Y,wing2X,wing2Y)

    def drawChevron(self):
        canvas=self.canvas
        x=self.x
        y=self.y
        (frontX,frontY,wing1X,wing1Y,wing2X,wing2Y)=self.getChevCoords()
        color=self.color
        chevron=[]
        chevron.append(canvas.create_line(frontX,frontY,wing1X,wing1Y,
                                          fill=color,width=2))
        chevron.append(canvas.create_line(frontX,frontY,wing2X,wing2Y,
                                          fill=color,width=2))
        self.chevron=chevron
        left=min(frontX,wing1X,wing2X)
        right=max(frontX,wing1X,wing2X)
        top=min(frontY,wing1Y,wing2Y)
        bottom=max(frontY,wing1Y,wing2Y)
        
        self.chevBox=(left,top,right,bottom) #comparison errors

    def draw(self):
        self.drawBox()
        self.drawChevron()

    def moveTo(self,x,y):
        #getting dx,dy
        dx=x-self.x
        dy=y-self.y
        #getting the objects
        canvas=self.canvas
        box=self.box
        (chev1,chev2)=self.chevron
        #moving the objects
        canvas.move(box,dx,dy)
        canvas.move(chev1,dx,dy)
        canvas.move(chev2,dx,dy)
        #increment location markers
        self.x=x
        self.y=y
        (cLeft,cTop,cRight,cBottom)=self.chevBox
        self.chevBox=(cLeft+dx,cTop+dy,cRight+dx,cBottom+dy)
        (left,top,right,bottom)=self.coords
        self.coords=(left+dx,top+dy,right+dx,bottom+dy)

    def animate(self):
        direction=self.direction
        canvas=self.canvas
        (dx,dy)=self.force
        dx*=3
        dy*=3
        (left,top,right,bottom)=self.coords
        (chev1,chev2)=self.chevron
        (cLeft,cTop,cRight,cBottom)=self.chevBox
        if((cLeft+dx<left)or(cTop+dy<top)or
           (cRight+dx>right)or(cBottom+dy>bottom)):
            dx*=-8
            dy*=-8
        for line in self.chevron:
            canvas.move(line,dx,dy)
        self.chevBox=(cLeft+dx,cTop+dy,cRight+dx,cBottom+dy)

    def resetChev(self):
        canvas=self.canvas
        (x,y)=(self.x,self.y)
        (left,top,right,bottom)=self.chevBox
        (cx,cy)=((left+right)/2,(top+bottom)/2)
        (dx,dy)=(x-cx,y-cy)
        for line in self.chevron:
            canvas.move(line,dx,dy)
        self.chevBox=(left+dx,top+dy,right+dx,bottom+dy)
      
##########################

class Goal():
    def __init__(self,canvas,left,top,right,bottom):
        self.canvas=canvas
        self.coords=(left,top,right,bottom)
        self.achieved=False

    def draw(self):
        canvas=self.canvas
        color="red"
        (left,top,right,bottom)=self.coords
        self.goal=canvas.create_rectangle(left,top,right,bottom,outline="red",
                                          fill="red",stipple="gray25")

    def achieve(self):
        self.achieved=True
        canvas=self.canvas
        canvas.itemconfig(self.goal,fill="green",outline="green")

    def unachieve(self):
        self.achieved=False
        canvas=self.canvas
        canvas.itemconfig(self.goal,fill="red",outline="red")

    def intersection(self,ball,x,y,endX,endY):
        r=ball.radius
        deltaX=endX-x
        deltaY=endY-y
        (left,top,right,bottom)=self.coords
        intersections=[]
        #corners are valued such that x,y is the origin (for simplification)
        corners=[(left-x,top-y),(right-x,top-y),
                 (right-x,bottom-y),(left-x,bottom-y)]
        #vertical motion case
        if (deltaX==0):
            checkEdgesVerticalCase(x,y,left,top,right,bottom,deltaY,r,intersections)
            checkCornersVerticalCase(x,y,r,deltaY,corners,intersections)
        #general motion case
        else:
            checkEdges(x,y,deltaX,deltaY,left,top,right,bottom,intersections,r)
            checkCorners(x,y,r,deltaX,deltaY,corners,intersections)
        return (chooseFirstByTime(intersections)!=None)
            
        
        

############################

class Button():
    def __init__(self,canvas,x,y,width,height,buttonType,buttonLevel):
        self.canvas=canvas
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.coords=(x-width/2,y-height/2,x+width/2,y+height/2)
        self.type=buttonType
        self.usable=False
        self.proScore=False
        self.level=buttonLevel
        self.setText()

    def setText(self):
        width=self.width
        buttonType=self.type
        if (buttonType=="startStop"):
            self.text="start/stop (s)"
            self.font=("calibri",width/10)
        elif (buttonType=="restart"):
            self.text="restart (r)"
            self.font=("calibri",width/10)
        elif(buttonType=="level"):
            self.text="level:"+str(self.level)
            self.font=("calibri",width/9)

    def draw(self):
        canvas=self.canvas
        (left,top,right,bottom)=self.coords
        text=self.text
        font=self.font
        if self.usable: self.fill="grey"
        else:
            self.fill="brown"
        #if you match or beat my score I make the button pretty :)
        if self.proScore: self.fill="gold"
        level=self.level
        if (level>0):
            highScore=canvas.data["highScores"][level]
            if highScore<9:
                text+=" score:"+str(highScore)
        #create button
        canvas.create_rectangle(left,top,right,bottom,
                                            fill=self.fill,width=0)
        #create buttonText
        canvas.create_text(self.x,self.y,text=text,
                                    font=font)
        
############################

class Obstacle():
    def __init__(self,canvas,*args):
        self.canvas=canvas
        assert(len(args)%2==0)
        if len(args)==4:
            self.coords=args
            self.draw()
            self.complex=False
        else:
            print "That's not a simple obstacle!"

    def draw(self):
        canvas=self.canvas
        (left,top,right,bottom)=self.coords
        self.obst=canvas.create_rectangle(left,top,right,bottom,
                                          fill="dark grey",width=0)

    def firstIntersection(self,x,y,endX,endY,r):
        (left,top,right,bottom)=self.coords
        deltaX=endX-x
        deltaY=endY-y
        intersections=[]
        #corners are valued such that x,y is the origin (for simplification)
        corners=[(left-x,top-y),(right-x,top-y),
                 (right-x,bottom-y),(left-x,bottom-y)]
        #vertical motion case
        if (deltaX==0):
            checkEdgesVerticalCase(x,y,left,top,right,bottom,deltaY,r,intersections)
            checkCornersVerticalCase(x,y,r,deltaY,corners,intersections)
        #general motion case
        else:
            checkEdges(x,y,deltaX,deltaY,left,top,right,bottom,intersections,r)
            checkCorners(x,y,r,deltaX,deltaY,corners,intersections)
        return chooseFirstByTime(intersections)

def checkEdgesVerticalCase(x,y,left,top,right,bottom,deltaY,r,intersections):
    if((x>=left)and(x<=right)):
        endY=y+deltaY
        if ((deltaY>0)and(y<top-r)and(endY>=top-r)): #ball hits top
            collX=x
            collY=top-r
            theta=0
            dy=collY-y
            time=1.0*dy/deltaY
            intersections.append((collX,collY,theta,time))
        elif((deltaY<0)and(y>bottom+r)and(endY<=bottom+r)):#ball hits bottom
            collX=x
            collY=bottom+r
            theta=0
            dy=collY-y
            time=1.0*dy/deltaY
            intersections.append((collX,collY,theta,time))

def checkCornersVerticalCase(x,y,r,deltaY,corners,intersections):
    for (d,e) in corners:
        det=(r**2-d**2)
        if det>=0:
            x1=0
            y1=e+math.sqrt(det)
            collX1=x1+x
            collY1=y1+y
            time1=1.0*(collY1-y)/deltaY
            try:
                theta1=math.atan((x1-d)/(y1-e))
            except:
                theta1=math.pi/2
            intersections.append((collX1,collY1,theta1,time1))

            x2=0
            y2=e-math.sqrt(det)
            collX2=x2+x
            collY2=y2+y
            time2=1.0*(collY2-y)/deltaY
            try:
                theta2=math.atan((x2-d)/(y2-e))
            except:
                theta2=math.pi/2
            intersections.append((collX2,collY2,theta2,time2))

def checkEdges(x,y,deltaX,deltaY,left,top,right,bottom,intersections,r):
    m=deltaY/deltaX
    endX=x+deltaX
    endY=y+deltaY
    #check left and right edges
    if(((x<left-r)and(endX>=left-r))or((x>right+r)and(endX<=right+r))):
        if((x<left-r) and (endX>=left-r)):
            dx=left-r-x
        else:
            dx=right+r-x
        dy=m*dx
        collX=x+dx
        collY=y+dy
        #if it's a left-right wall collision, add that point to the list
        if ((collY>=top)and(collY<=bottom)):
            theta=math.pi/2
            time=1.0*dx/deltaX
            intersections.append((collX,collY,theta,time))
    #check top and bottom edges: if m==0, it can't possibly hit the top or bottom
    if((((y<top-r)and(endY>=top-r))or((y>bottom+r)and(endY<=bottom+r)))and(m!=0)):
        if((y<top-r)and(endY>=top-r)):
            dy=top-r-y
        else:
            dy=bottom+r-y
        dx=dy/m
        collX=x+dx
        collY=y+dy
        #if it's a top-bottom collision, add that point to the list
        if ((collX>=left)and(collX<=right)):
            theta=0
            time=1.0*dx/deltaX
            intersections.append((collX,collY,theta,time))

                
def checkCorners(x,y,r,deltaX,deltaY,corners,intersections):
    m=deltaY/deltaX
    a=(1+m**2)
    for (d,e) in corners:
        b=-2*(d+e*m)
        c=d**2+e**2-r**2
        det=(b**2-4*a*c)
        if det>=0:
            x1=(-b+math.sqrt(det))/(2*a)
            y1=m*x1
            try:
                theta1=math.atan((x1-d)/(y1-e))
            except:
                theta1=math.pi/2
            collX1=x1+x
            collY1=y1+y
            time1=1.0*(collX1-x)/deltaX
            intersections.append((collX1,collY1,theta1,time1))
            
            x2=(-b-math.sqrt(det))/(2*a)
            y2=m*x2
            try:
                theta2=math.atan((x2-d)/(y2-e))
            except:
                theta2=math.pi/2
            collX2=x2+x
            collY2=y2+y
            time2=1.0*(collX2-x)/deltaX
            intersections.append((collX2,collY2,theta2,time2))

def chooseFirstByTime(intersections):
    minTime=1
    for index in xrange(len(intersections)):
        time=intersections[index][3]
        if ((time>0.0000000000001) and (time<=minTime)):
            minIndex=index
            minTime=time
    try: return intersections[minIndex]
    except:
        return None
