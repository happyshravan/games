#michael Choquette
#These programs manage the player's completed levels and scores

import GSlevels
import GSclasses

def setProScores(canvas): #setting my best scores
    proScores={}
    proScores[1]=1
    proScores[2]=1
    proScores[3]=1
    proScores[4]=2
    proScores[5]=2
    proScores[6]=2
    proScores[7]=2
    proScores[8]=2
    proScores[9]=4
    proScores[10]=3
    proScores[11]=3
    proScores[12]=3
    canvas.data["proScores"]=proScores

def loadHighScores(canvas): #reads the player's scores into a dictionary.
    highScores={}
    levels=canvas.data["levels"]
    try:
        fileHandler=open("GravishiftHighScores.txt","rt")
        scores=fileHandler.readlines()
        fileHandler.close()
    except:
        scores=["9"]*levels
    for i in xrange(levels):
        highScores[i+1]=int(scores[i])
    canvas.data["highScores"]=highScores

def saveHighScores(canvas): #saves a dictionary of player's scores into a file.
    levels=canvas.data["levels"]
    highScores=canvas.data["highScores"]
    string=str(highScores[1])
    for i in xrange(2,levels+1):
        string+="\n"+str(highScores[i])
    fileHandler=open("GravishiftHighScores.txt","wt")
    fileHandler.write(string)
    fileHandler.close()

#checks if a score is better than the last high score, and stors it if it is.
def checkScore(canvas): 
    level=canvas.data["level"]
    highScores=canvas.data["highScores"]
    #modifying the relevant score if it's better than the high score
    highScores[level]=min(highScores[level],canvas.data["score"])
    canvas.data["highScores"]=highScores
    saveHighScores(canvas)

def saveTiles(canvas):
    level=canvas.data["level"]
    text=""
    for tile in canvas.data["tiles"]:
        text+=str(tile.x)+","+str(tile.y)+","+str(tile.homeX)+","+str(tile.homeY)+","+tile.direction+"\n"
    fileHandler=open("Level"+str(level)+"Tiles.txt","wt")
    fileHandler.write(text)
    fileHandler.close()

def loadTiles(canvas,useSavedTileSpots):
    level=canvas.data["level"]
    canvas.data["score"]=0
    try:
        if useSavedTileSpots:
            fileHandler=open("Level"+str(level)+"Tiles.txt","rt")
            tileStats=fileHandler.readlines()
            fileHandler.close()
        else:
            GSlevels.makeTiles(canvas)
            return
    except:
        GSlevels.makeTiles(canvas)
        return
    width=canvas.data["canvasWidth"]
    height=canvas.data["canvasHeight"]
    tW=width/12
    tH=tW
    tiles=[]
    for tileText in tileStats:
        (tileX,tileY,homeX,homeY,tileDir)=tileText.split(",")
        (tileX,tileY,homeX,homeY)=(int(tileX),int(tileY),int(homeX),int(homeY))        
        tileDir=tileDir.rstrip()
        tile=GSclasses.Tile(canvas,tileX,tileY,tW,tH,tileDir)
        tile.homeX=homeX
        tile.homeY=homeY
        if ((tileX,tileY)!=(homeX,homeY)):
            tile.inPlay=True
            canvas.data["score"]+=1
        tiles.append(tile)
    canvas.data["tiles"]=tiles
