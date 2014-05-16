#Michael Choquette, mchoquet
#Creation of the menu and levels.

import StreamClasses

def makeLevel(canvas):
    level=canvas.data["level"]
    assert (level>=0)
    if level==0:
        menuBackground(canvas)
        menuButtons(canvas)
    else:
        levelBackground(canvas)
        levelSources(canvas,level)
        levelFilters(canvas,level)
        levelPieces(canvas,level)
        levelGoals(canvas,level)

def menuBackground(canvas):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.create_rectangle(0,0,W,H,width=0,fill="midnight blue") #backdrop
    text="Stream"
    font=("Courier",H/4,"bold")
    canvas.create_text(W/2,H/2,text=text,font=font,fill="purple") #title

def menuButtons(canvas):
    W=canvas.data["Width"]
    H=canvas.data["Height"]

############## level ##############

def levelBackground(canvas):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.create_rectangle(0,0,W,H,width=0,fill="black")

def levelSources(canvas,level):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.data["sources"].append(StreamClasses.Source(canvas,100,100,35,24,8))

def levelFilters(canvas,level):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.data["filters"].append(StreamClasses.Filter(canvas,400,400,100,"red"))

def levelPieces(canvas,level):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.data["pieces"].append(StreamClasses.Piece(canvas,400,200,35,180,"g"))

def levelGoals(canvas,level):
    W=canvas.data["Width"]
    H=canvas.data["Height"]
    canvas.data["goals"].append(StreamClasses.Goal(canvas,"stuff"))
