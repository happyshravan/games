#DTImages.py
#Michael Choquette
#mchoquet

from Tkinter import *
import math
import Im

#This program deals with the images for darkTide

#makes the images for the game, using information stored in the canvas,
#and saves those images to .gif files for later use.
#ground goes 210,210,115 to 255,255,220 (low to high, dark to light)
#"water" is 96,0,192, with varying opacity (alpha goes from 25% to 100%)
#note: this is a (ragged) 2d list of every possible picture for the cells
def makeSurfaceImages(canvas):
    maxCliffs=canvas.data.maxCliffs
    cliffHeight=canvas.data.cliffHeight
    maxWaterHeight=cliffHeight*(maxCliffs+1) #10 higher than highest ground
    dh=cliffHeight/5.0
    totalNumDepthLevels=maxWaterHeight/dh+1
    images=[0]*(maxCliffs+1)  
    baseRed,baseGreen,baseBlue=200,200,115 #the DARKEST ground color scheme
    dRed,dGreen,dBlue=55,55,105 #by how much the ground changes from low to high
    wRed,wGreen,wBlue=96,0,192 #the RGB value of the water
    for i in xrange(maxCliffs+1):
        h=cliffHeight*i
        numDepthLevels=int((maxWaterHeight-h)/dh+1)
        images[i]=[0]*numDepthLevels
        groundRed=baseRed+dRed*i/maxCliffs
        groundGreen=baseGreen+dGreen*i/maxCliffs
        groundBlue=baseBlue+dGreen*i/maxCliffs
        for depthLevel in xrange(numDepthLevels):
            if depthLevel==0:
                alphaDeep=0
                alphaShallow=0
            else:
                alphaDeep=.25+.75*depthLevel/(totalNumDepthLevels-1)
                if depthLevel>1:
                    alphaShallow=alphaDeep-.75/(totalNumDepthLevels-1)
                else:
                    alphaShallow=0
            print alphaDeep,alphaShallow
            rValDeep=int((1-alphaDeep)*groundRed+alphaDeep*wRed)
            gValDeep=int((1-alphaDeep)*groundGreen+alphaDeep*wGreen)
            bValDeep=int((1-alphaDeep)*groundBlue+alphaDeep*wBlue)
            deepColor=(rValDeep,gValDeep,bValDeep)
            rValShallow=int((1-alphaShallow)*groundRed+alphaShallow*wRed)
            gValShallow=int((1-alphaShallow)*groundGreen+alphaShallow*wGreen)
            bValShallow=int((1-alphaShallow)*groundBlue+alphaShallow*wBlue)
            shallowColor=(rValShallow,gValShallow,bValShallow)
            #define borderColor here
            borderColor=[0,0,0]
            if alphaShallow==0 and alphaDeep!=0: borderColor=deepColor
            else:
                for j in xrange(3): #one for each RGB value
                    dColor=deepColor[j]-shallowColor[j]
                    borderColor[j]=max(deepColor[j]+3*dColor,0)
            images[i][depthLevel]=makeImageSublist(canvas,deepColor,shallowColor,borderColor)
    canvas.data.surfaceImages=images

def alphaMix(a,b,alpha):
    return (1-alpha)*a+alpha*b

#the subList will be a list indexed by a linear combination of touchesUp,
#touchesDown, touchesRight, and touchesLeft
def makeImageSublist(canvas,deepColor,shallowColor,borderColor):
    cellSize=canvas.data.cellSize
    subList=[0]*16
    for i in xrange(16):
        up,right,down,left=i/8,(i/4)%2,(i/2)%2,i%2
        subList[i]=makeImage(up,down,right,left,deepColor,
                             shallowColor,borderColor,cellSize)
    return subList

#I'm not sure how to do this better; there's no way to get around the 16 cases
def makeImage(up,down,right,left,deepColor,shallowColor,borderColor,imSize):
    #up,down,right,and left are ints that tell if there's a neighbor there
    if up:
        if right:
            if down:
                if left:
                    return ImageURDL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageURD(deepColor,shallowColor,borderColor,imSize)
            else:
                if left:
                    return ImageURL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageUR(deepColor,shallowColor,borderColor,imSize)
        else:
            if down:
                if left:
                    return ImageUDL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageUD(deepColor,shallowColor,borderColor,imSize)
            else:
                if left:
                    return ImageUL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageU(deepColor,shallowColor,borderColor,imSize)
    else:
        if right:
            if down:
                if left:
                    return ImageRDL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageRD(deepColor,shallowColor,borderColor,imSize)
            else:
                if left:
                    return ImageRL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageR(deepColor,shallowColor,borderColor,imSize)
        else:
            if down:
                if left:
                    return ImageDL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return ImageD(deepColor,shallowColor,borderColor,imSize)
            else:
                if left:
                    return ImageL(deepColor,shallowColor,borderColor,imSize)
                else:
                    return Image(deepColor,shallowColor,borderColor,imSize)

############### section 1
                
def ImageURDL(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            Im.setRGB(image,x,y,deepColor)
    return image

def ImageURD(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            if x<2:
                Im.setRGB(image,x,y,borderColor)
            else:
                Im.setRGB(image,x,y,deepColor)
    return image

def ImageURL(deepColor,shallowColor,borderColor,imageSize):
    return Im.lRotate(ImageURD(deepColor,shallowColor,borderColor,imageSize))

def ImageUR(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            if y<x-1:
                Im.setRGB(image,x,y,deepColor)
            elif y>x+1:
                Im.setRGB(image,x,y,shallowColor)
            else:
                Im.setRGB(image,x,y,borderColor)
    return image

############### section 2

def ImageUDL(deepColor,shallowColor,borderColor,imageSize):
    return Im.rotate180(ImageURD(deepColor,shallowColor,borderColor,imageSize))

def ImageUD(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            if x<2 or x>imageSize-3:
                Im.setRGB(image,x,y,borderColor)
            else:
                Im.setRGB(image,x,y,deepColor)
    return image

def ImageUL(deepColor,shallowColor,borderColor,imageSize):
    return Im.lRotate(ImageUR(deepColor,shallowColor,borderColor,imageSize))

def ImageU(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            if y<x-1 and y<imageSize-2-x:
                Im.setRGB(image,x,y,deepColor)
            elif y<x+1 and y<imageSize-x:
                Im.setRGB(image,x,y,borderColor)
            else:
                Im.setRGB(image,x,y,shallowColor)
    return image

############## section 3

def ImageRDL(deepColor,shallowColor,borderColor,imageSize):
    return Im.rRotate(ImageURD(deepColor,shallowColor,borderColor,imageSize))

def ImageRD(deepColor,shallowColor,borderColor,imageSize):
    return Im.rRotate(ImageUR(deepColor,shallowColor,borderColor,imageSize))

def ImageRL(deepColor,shallowColor,borderColor,imageSize):
    return Im.lRotate(ImageUD(deepColor,shallowColor,borderColor,imageSize))

def ImageR(deepColor,shallowColor,borderColor,imageSize):
    return Im.rRotate(ImageU(deepColor,shallowColor,borderColor,imageSize))

############## section 4

def ImageDL(deepColor,shallowColor,borderColor,imageSize):
    return Im.rotate180(ImageUR(deepColor,shallowColor,borderColor,imageSize))

def ImageD(deepColor,shallowColor,borderColor,imageSize):
    return Im.rotate180(ImageU(deepColor,shallowColor,borderColor,imageSize))

def ImageL(deepColor,shallowColor,borderColor,imageSize):
    return Im.lRotate(ImageU(deepColor,shallowColor,borderColor,imageSize))

def Image(deepColor,shallowColor,borderColor,imageSize):
    image=PhotoImage()
    b=imageSize/2 #the border zone
    for x in xrange(imageSize):
        for y in xrange(imageSize):
            #outside
            if y>b-x+2 and y<3*b-x-1 and y>x-b and y<x+b-3:
                Im.setRGB(image,x,y,deepColor)
            elif y>b-x-1 and y<3*b-x+1 and y>x-b-2 and y<x+b:
                Im.setRGB(image,x,y,borderColor)
            else:
                Im.setRGB(image,x,y,shallowColor)
    return image

################################################################################
        #TEST CODE

def init(canvas):
    #drawing a sample set of generated images
    canvas.data.maxCliffs=4
    canvas.data.cliffHeight=10
    canvas.data.cellSize=10
    makeSurfaceImages(canvas)
    s=canvas.data.cellSize
    images=canvas.data.surfaceImages
    groundLevel=3
    for waterLevel in xrange(len(images[groundLevel])):
        y=(waterLevel+.5)*s
        for i in xrange(16): #16 images per waterLevel
            x=(i+.5)*s
            canvas.create_image(x,y,image=images[groundLevel][waterLevel][i])
##    test=PhotoImage(file="testPhoto.gif")
##    canvas.create_image(600,300,image=test)
##    canvas.data.test=test
##    test2=Im.rotate(test,50)
##    canvas.create_image(300,300,image=test2)
##    canvas.data.test2=test2

def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    canvas = Canvas(root, width=800, height=600)
    canvas.pack(fill=BOTH, expand=YES)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct(): pass
    canvas.data = Struct()
    print Im.getRGB(canvas,100,100)
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    # root.bind("<KeyPress>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
