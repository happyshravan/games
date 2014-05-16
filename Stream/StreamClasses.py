#Michael Choquette, mchoquet
#The classes for the game Stream

import math

class Particle():
    def __init__(this,canvas,x,y,vx,vy,w):
        this.canvas=canvas
        this.x=x
        this.y=y
        this.vx=vx
        this.vy=vy
        this.w=w
        this.particle=canvas.create_line(x,y,x,y,width=w,fill="white")
        this.timeLeft=150

    def move(this,dx,dy):
        (x,y)=(this.x,this.y)
        this.canvas.coords(this.particle,x,y,x+dx,y+dy)
        (this.x,this.y)=(x+dx,y+dy)
        this.timeLeft-=1

class Source():
    def __init__(this,canvas,x,y,r,vx,vy):
        this.canvas=canvas
        this.x=x
        this.y=y
        this.r=r
        this.vx=vx
        this.vy=vy
        this.source=canvas.create_oval(x-r,y-r,x+r,y+r,fill="",outline="white")

class Filter():
    def __init__(this,canvas,x,y,r,color):
        this.canvas=canvas
        this.x=x
        this.y=y
        this.r=r
        this.color=color
        this.filter=canvas.create_oval(x-r,y-r,x+r,y+r,fill="",outline="red")

class Piece():
    def __init__(this,canvas,x,y,pieceR,effectR,effect):
        this.canvas=canvas
        this.x=x
        this.y=y
        this.pieceR=pieceR
        this.effectR=effectR
        this.effect=effect
        #drawing the piece- effect radius, object, and type indicator
        this.outer=canvas.create_oval(x-effectR,y-effectR,x+effectR,y+effectR,
                                      fill="",outline="white")
        this.inner=canvas.create_oval(x-pieceR,y-pieceR,x+pieceR,y+pieceR,
                                      width=0,fill="white")
        this.logo=canvas.create_oval(x-pieceR/2,y-pieceR/2,x+pieceR/2,
                                     y+pieceR/2,width=0,fill="dark grey")

    def getForce(this,x,y): #####pre-calculate for speed?####
        if (((x-this.x)**2+(y-this.y)**2)<=(this.effectR)**2):
            if this.effect=="g":
                (dx,dy)=(this.x-x,this.y-y)
                d=math.sqrt(dx**2+dy**2)
##              for a realistic gravity, use (dx/(d**3),dy/(d**3)) instead
                return (dx/d,dy/d)
            elif this.effect=="u": return (0,-1)
            elif this.effect=="r": return (1,0)
            elif this.effect=="d": return (0,1)
            elif this.effect=="l": return (-1,0)
        return (0,0)

    def move(this,dx,dy):
        canvas=this.canvas
        canvas.move(this.outer,dx,dy)
        canvas.move(this.inner,dx,dy)
        canvas.move(this.logo,dx,dy)
        this.x+=dx
        this.y+=dy

class Goal():
    def __init__(this,canvas,stuff): ###decide what to do with this later
        pass
