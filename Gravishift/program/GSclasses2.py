from Tkinter import *

class Obstacle():
    def __init__(self,canvas,*args):
        self.canvas=canvas
        assert(len(args)%2==0)
        corners=[]
        for index in range(0,len(args),2):
            corners.append((args[index],args[index+1]))
        self.corners=corners
        self.obst=canvas.create_polygon(*args,fill="dark grey",width=0)

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
            checkCornersVerticalCase(x,y,deltaY,corners,intersections,r)
        #general motion case
        else:
            checkEdges(x,y,deltaX,deltaY,left,top,right,bottom,intersections,r)
            checkCorners(x,y,deltaX,deltaY,corners,intersections,r)
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

def checkCornersVerticalCase(x,y,deltaY,corners,intersections,r):
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

                
def checkCorners(x,y,deltaX,deltaY,corners,intersections,r):
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

########################################################


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
##    root.bind("<Button-1>", mousePressed)
##    root.bind("<Button-3>", rightMousePressed)
##    root.bind("<B1-Motion>", mouseMoved)
##    root.bind("<ButtonRelease-1>", mouseReleased)
##    root.bind("<Key>",keyPressed)
    obst=Obstacle(canvas,0,0,100,100,0,100)
    root.mainloop()

run()
