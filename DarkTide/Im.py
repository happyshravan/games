#DTImages.py
#Michael Choquette
#mchoquet

from Tkinter import *
import math

#This module contains methods for general image manipulation

#n%a (always returns a float)
    #assumes that a is an int
def floatMod(n,a):
    return n-((int(n)/a)*a)

#v2 (with area mapping)
#should not be used to rotate a rotated image
#theta is in DEGREES
def rotate(image,theta):
    theta=math.radians(floatMod(theta,360))
    oldWidth,oldHeight=image.width(),image.height()
    oldCx,oldCy=oldWidth/2.0,oldHeight/2.0
    newWidth,newHeight=findNewDimensions(image,theta)
    newCx,newCy=newWidth/2.0,newHeight/2.0
    sinT,cosT=math.sin(theta),math.cos(theta)
    rotatedImage=PhotoImage(width=newWidth,height=newHeight)
    oldColor=[0,0,0]#I only need to define it once
    for x in xrange(newWidth):
        for y in xrange(newHeight):
            oldX=oldCx+(x-newCx)*cosT-(y-newCy)*sinT
            oldY=oldCy+(x-newCx)*sinT+(y-newCy)*cosT
            if oldX>=0 and oldX<=oldWidth-1 and oldY>=0 and oldY<=oldHeight-1:
                x1,y1=int(oldX),int(oldY)#pixel the UL corner of oldPixel is in
                dx,dy=oldX-x1,oldY-y1 #how far into this pixel oldPixel starts
                try: #UL
                    c1=map(lambda color:(1-dx)*(1-dy)*color,getRGB(image,x1,y1))
                except:
                    c1=(0,0,0)
                try: #UR
                    c2=map(lambda color: dx*(1-dy)*color,getRGB(image,x1+1,y1))
                except:
                    c2=(0,0,0)
                try: #LL
                    c3=map(lambda color: dy*(1-dx)*color,getRGB(image,x1,y1+1))
                except:
                    c3=(0,0,0)
                try: #LR
                    c4=map(lambda color: dx*dy*color,getRGB(image,x1+1,y1+1))
                except:
                    c4=(0,0,0)
                for i in xrange(3):
                    oldColor[i]=int(c1[i]+c2[i]+c3[i]+c4[i])
                if oldColor!=[0,0,0]:
                    setRGB(rotatedImage,x,y,oldColor)
    return rotatedImage

def findNewDimensions(image,theta):
    dx,dy=image.width(),image.height()
    diagonal=math.sqrt(dx**2+dy**2)
    alpha=math.atan(1.0*dy/dx)
    w1=abs(diagonal*math.cos(theta+alpha))
    w2=abs(diagonal*math.cos(theta-alpha))
    h1=abs(diagonal*math.sin(theta+alpha))
    h2=abs(diagonal*math.sin(theta-alpha))
    return int(round(max(w1,w2))),int(round(max(h1,h2)))

#return the image rotated 90 degrees clockwise
def rRotate(image):
    newWidth,newHeight=image.height(),image.width()
    rotatedImage=PhotoImage(width=newWidth,height=newHeight)
    for x in xrange(newWidth):
        for y in xrange(newHeight):
            setRGB(rotatedImage,x,y,getRGB(image,y,newWidth-1-x))
    return rotatedImage

#returns the image rotated 90 degrees counterclockwise
def lRotate(image):
    newWidth,newHeight=image.height(),image.width()
    rotatedImage=PhotoImage(width=newWidth,height=newHeight)
    for x in xrange(newWidth):
        for y in xrange(newHeight):
            setRGB(rotatedImage,x,y,getRGB(image,newHeight-1-y,x))
    return rotatedImage

#returns the image rotated 180 degreed
def rotate180(image):
    newWidth,newHeight=image.width(),image.height()
    rotatedImage=PhotoImage(width=newWidth,height=newHeight)
    for x in xrange(newWidth):
        for y in xrange(newHeight):
            setRGB(rotatedImage,x,y,getRGB(image,newWidth-1-x,newHeight-1-y))
    return rotatedImage

#returns the image reflected around the x axis
def reflectX(image):
    width,height=image.width(),image.height()
    flippedImage=PhotoImage(width=width,height=height)
    for x in xrange(width):
        for y in xrange(height):
            setRGB(flippedImage,x,y,getRGB(image,height-1-x,y))
    return flippedImage

#returns the image reflected about the y axis
def reflectY(image):
    width,height=image.width(),image.height()
    flippedImage=PhotoImage(width=width,height=height)
    for x in xrange(width):
        for y in xrange(height):
            setRGB(flippedImage,x,y,getRGB(image,x,height-1-y))
    return flippedImage

def setRGB(image, x, y,(red, green, blue)):
    color = hexColor(red, green, blue)
    image.put(color, to=(x,y))

def getRGB(image, x, y):
    value = image.get(x, y)
    return tuple(map(int, value.split(" ")))

def hexColor(red, green, blue):
    return ("#%02x%02x%02x" % (red, green, blue))
