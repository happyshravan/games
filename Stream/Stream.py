#Michael Choquette, mchoquet
#A game about manipulating a stream of particles

from Tkinter import *
import time
import StreamClasses
import StreamLevels
import random
import math

############################
##### user interaction #####
############################

def keyPressed(event):
    pass

def mousePressed(event):
    canvas=event.widget.canvas
    for piece in canvas.data["pieces"]:
        if (event.x-piece.x)**2+(event.y-piece.y)**2<=piece.pieceR**2:
            canvas.data["chosenPiece"]=piece
            canvas.data["displacement"]=(piece.x-event.x,piece.y-event.y)

def mouseDragged(event):
    canvas=event.widget.canvas
    piece=canvas.data["chosenPiece"]
    if piece!=None:
        (w,h,r)=(canvas.data["Width"],canvas.data["Height"],piece.pieceR)
        (dispX,dispY)=canvas.data["displacement"]
        (newX,newY)=(min(max(event.x+dispX,r),w-r),min(max(event.y+dispY,r),h-r))
        (dx,dy)=(newX-piece.x,newY-piece.y)
        piece.move(dx,dy)

def mouseReleased(event):
    canvas=event.widget.canvas
    canvas.data["chosenPiece"]=None
    canvas.data["displacement"]=None

def mouseMoved(event):
    pass

############################
######### gameplay #########
############################

def doPieceEffects(canvas):
    for particle in canvas.data["particles"]:
        (vx,vy)=(particle.vx,particle.vy)
        for piece in canvas.data["pieces"]:
            if (piece.effect in ["u","d","l","r","g"]):
                (xForce,yForce)=piece.getForce(particle.x,particle.y)
                vx+=xForce
                vy+=yForce
        (particle.vx,particle.vy)=(vx,vy)

def moveParticles(canvas):
    doPieceEffects(canvas)
    for particle in canvas.data["particles"]:
        (vx,vy)=(particle.vx*0.97,particle.vy*0.97)
        if abs(vx)<0.2: vx=0
        if abs(vy)<0.2: vy=0
        particle.move(vx,vy)
        (particle.vx,particle.vy)=(vx,vy)

def removeParticles(canvas):
    particles=canvas.data["particles"]
    width=canvas.data["Width"]
    height=canvas.data["Height"]
    if ((len(particles)>0)and(particles[0].timeLeft<=0)):
        for i in xrange(4*len(canvas.data["sources"])):
            canvas.delete(particles[0].particle)
            particles.pop(0)
    for i in xrange(len(particles)-1,-1,-1):
        particle=particles[i]
        if ((particle.vx==particle.vy==0)or
            (particle.x<0)or(particle.x>width)or
            (particle.y<0)or(particle.y>height)):
            particles.pop(i)
            canvas.delete(particle.particle)
        
def makeParticles(canvas):
    particles=canvas.data["particles"]
    for source in canvas.data["sources"]:
        for i in xrange(4):
            r=source.r*random.random()
            theta=2*math.pi*random.random()
            x=source.x+r*math.cos(theta)
            y=source.y+r*math.sin(theta)
            particles.append(StreamClasses.Particle(canvas,x,y,source.vx,
                                                    source.vy,1))
    for piece in canvas.data["pieces"]:
        canvas.lift(piece.outer)
        canvas.lift(piece.inner)
        canvas.lift(piece.logo)

def checkGoals(canvas):
    pass

def checkVictory(canvas):
    pass

def timerFired(canvas):
    start=time.clock()
    moveParticles(canvas)
    removeParticles(canvas)
    makeParticles(canvas)
    checkGoals(canvas) #Later, this will include playSounds
    checkVictory(canvas) #may just have this in timerFired
    end=time.clock()
    duration=int(1000*(end-start))
    delay=max(16-duration,1) #the variable delay may help compensate for lag
    canvas.after(delay,timerFired,canvas)

############################
###### initialization ######
############################

def init(canvas):
    canvas.data["buttons"]=[]
    canvas.data["particles"]=[]
    canvas.data["sources"]=[]
    canvas.data["filters"]=[]
    canvas.data["pieces"]=[]
    canvas.data["goals"]=[]
    canvas.data["won"]=False
    canvas.data["chosenPiece"]=None
    canvas.data["displacement"]=None
    StreamLevels.makeLevel(canvas)
    if canvas.data["level"]>0:timerFired(canvas)

def run(Width,Height):
    root=Tk()
    assert ((Width>0)and(Height>0))
    canvas=Canvas(root,width=Width,height=Height)
    canvas.pack()
    canvas.canvas=root.canvas=canvas
    canvas.data={}
    canvas.data["Width"]=Width
    canvas.data["Height"]=Height
    canvas.data["level"]=1
    init(canvas)
    root.bind("<Key>",keyPressed)
    root.bind("<Button-1>",mousePressed)
    root.bind("<B1-Motion>",mouseDragged)
    root.bind("<ButtonRelease-1>",mouseReleased)
##    root.bind("<>",mouseMoved)
    root.mainloop()

run(800,600)
    
