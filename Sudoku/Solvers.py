#Solvers.py
#Michael Choquette
#This contaons all the Sudoku solvers I've written

import math
import copy

#TIMES:
    #slooowSolve:
        #4x4: solved in 0.000367 seconds (0.00343 seconds variance)
        #9x9: didn't solve in 30 minutes :(
        #16x16: BAHAHAHAHAHA!
    #solve:
        #4x4: solved in 0.000112 seconds (0.00242 seconds variance)
        #9x9: solved in 0.904 seconds (0.0201 seconds variance)
        #16x16: solved in 963.585 seconds (16.06 minutes)
    #quickSolve: #BROKEN
        #4x4:
        #9x9:
        #16x16:
    #turboSolve:
        #4x4: solved in 0.0000677 seconds (0.00184 seconds variance)
        #9x9: solved in 0.00124 seconds (0.00221 seconds variance) 
        #16x16: solved in 3.442 seconds (0.0435 seconds variance) 
    #logicSolve:
        #4x4:
        #9x9:
        #16x16:

################################################################################
################################# slooowSolve ##################################
################################################################################

#the sloooooooooooow version
#this can do 4x4, but not 9x9

def slooowSolve(canvas):
    board,startingBoard=canvas.data.board,canvas.data.startingBoard
    if isFull(board) and not hasContradiction(board): return True
    n=len(board)
    for row in xrange(n):
        for col in xrange(n):
            for i in xrange(1,n+1):
                if rightPlace(board,startingBoard,row,col,i):
                    return True
    return False

#idea: make a list of row,cols that can be changed and loop through that instead
#Also, can I get rid of the 0 dependency somehow?

#if it's immutable, return False because this way was wrong
#if it can be changed:
    #change it to i
    #check if there's a contradiction now
    #if there's not, check if it's full and return True if it is (it's solved)
#if you have to keep looking:
    #for every cell AFTER row,col:
        #try to fill it with every legal number
            #return True if it was the right place
        #if none of the numbers were right -> reset that row,col to 0
#if none of them worked, return False because this wasn't the right place

#NOTE: need to test for solution in solve too (what if it starts solved???)
def rightPlace(board,startingBoard,row,col,i):
    if startingBoard[row][col]!=0: return False
    board[row][col]=i
    if hasContradiction(board):
        board[row][col]=0
        return False
    if isFull(board): return True
    n=len(board)
    for newRow in xrange(row,n):
        for newCol in xrange(n):
            if newRow>row or newCol>col:
                for i in xrange(1,n+1):
                    if rightPlace(board,startingBoard,newRow,newCol,i):
                        return True
                if startingBoard[newRow][newCol]==0:board[newRow][newCol]=0
    return False

#make a temp list, and put the values into the places where the would be IF:
    #1. the list was sorted correctly, and
    #2. there were no repeat numbers
#if two numbers are placed in the same spot, return True
#Note: as this only tests for strong contradictions, it ignores 0s that it sees
def hasContradiction(board):
    n=len(board)
    numberList=[0]*n
    #rows
    for row in xrange(n):
        for value in board[row]:
            if value>0 and value<=n:
                if numberList[value-1]!=0:
##                    print "multiple occurences of",value,"in row",row
                    return True
                numberList[value-1]=value
        for i in xrange(n):
            numberList[i]=0
    #cols
    for col in xrange(n):
        for row in xrange(n):
            value=board[row][col]
            if value>0 and value<=n:
                if numberList[value-1]!=0:
##                    print "multiple occurences of",value,"in col",row
                    return True
                numberList[value-1]=value
        for i in xrange(n):
            numberList[i]=0
    #squares
    root=int(math.sqrt(n))
    for squareNum in xrange(n):
        startRow,startCol=squareNum/root*root,squareNum%root*root
        for cellNum in xrange(n):
            dRow,dCol=divmod(cellNum,root)
            value=board[startRow+dRow][startCol+dCol]
            if value>0 and value<=n:
                if numberList[value-1]!=0:
##                    print "multiple occurences of",value,"in square",squareNum
                    return True
                numberList[value-1]=value
        for i in xrange(n):
            numberList[i]=0
    return False

def isFull(board):
    n=len(board)
    for row in board:
        for val in row:
            if val<1 or val>n: return False
    return True

################################################################################
#################################### solve #####################################
################################################################################

#it takes maybe 1/4 second to selve a 9x9, but can't handle a 16x16

def solve(canvas):
    board=canvas.data.board
    mutables=getMutableCells(canvas.data.startingBoard)
    if len(mutables)==0: return True
    for guess in xrange(1,len(board)+1):
        if correct(board,mutables,0,guess): return True
    return False

def getMutableCells(startingBoard):
    n=len(startingBoard)
    mutables=[]
    for row in xrange(n):
        for col in xrange(n):
            if startingBoard[row][col]==0: mutables.append((row,col))
    return tuple(mutables)

#takes in the index of where it is in the mutable tuple-of-tuples
#assigns the guess value to board[row][col]
#if this causes a contradiction at [row][col]: return False
#at this point we know there are no contradictions,
    #so if this index was the last one it should return True
#then it tries to add each number to the next index in the tuple-of-tuples:
    #if it works, return True because the current guess must have been correct
    #if none of them work, reset newRow,newCol 0 and return False
def correct(board,mutables,index,guess):
    board[mutables[index][0]][mutables[index][1]]=guess
    if localContradiction(board,mutables[index]):
        return False
    if index==len(mutables)-1: return True
    for newGuess in xrange(1,len(board)+1):
        if correct(board,mutables,index+1,newGuess):
            return True
    board[mutables[index+1][0]][mutables[index+1][1]]=0 #newRow,newCol=0
    return False

#make a temp list, and put the values into the places where the would be IF:
    #1. the list was sorted correctly, and
    #2. there were no repeat numbers
#if two numbers are placed in the same spot, return True for a contradiction
#Note: as this only tests for strong contradictions, it ignores 0s that it sees
def localContradiction(board,(row,col)):
    n=len(board)
    numberList=[0]*n
    #row
    for value in board[row]:
        if value>0 and value<=n:
            if numberList[value-1]!=0:return True
            numberList[value-1]=value
    numberList=[0]*n
    #col
    for row1 in xrange(n):
        value=board[row1][col]
        if value>0 and value<=n:
            if numberList[value-1]!=0:return True
            numberList[value-1]=value
    numberList=[0]*n
    #squares
    root=int(math.sqrt(n))
    startRow,startCol=row/root*root,col/root*root
    for cellNum in xrange(n):
        dRow,dCol=divmod(cellNum,root)
        value=board[startRow+dRow][startCol+dCol]
        if value>0 and value<=n:
            if numberList[value-1]!=0:return True
            numberList[value-1]=value
    return False

################################################################################
################################ quickSolve ####################################
################################################################################

#At each square on the board is a list of the values penciled in at the square
    #only look at squares with more then 1 possible inital value value
    #save those options in a list?
        #no way to backtrack them :(
        #calculate them as I go then

#broken, and I don't care to fix it right now

def quickSolve(canvas):
    possibilities=getPossibilities(canvas.data.startingBoard)
    board=canvas.data.board=getBoard(possibilities)
    cellsToInspect=getCellsToInspect(possibilities)
    if len(cellsToInspect)==0: return True
    print cellsToInspect
    for guess in possibilities[cellsToInspect[0][0]][cellsToInspect[0][1]]:
        if guessedRight(board,cellsToInspect,0,guess):
            canvas.data.board=getBoard(board)
            return True
    canvas.data.board=-1
    return False

def getPossibilities(startingBoard):
    n=len(startingBoard)
    return map(lambda row:
               map(lambda col:getGuesses(startingBoard,(row,col)),range(n)),
               range(n))

#start with all values possible, then remove everything else
#if there's only one option, still return it in a list by itself
def getGuesses(board,(row,col)):
    if board[row][col]!=0: return[board[row][col]]
    n=len(board)
    root=int(math.sqrt(n))
    lr,lc=row/root*root,col/root*root
    guesses=filter(lambda val:val not in board[row],range(1,n+1))
    for i in xrange(n): #looking through the rest of the board
        if board[i][col] in guesses: guesses.remove(board[i][col])
        if board[lr+i/root][lc+i%root] in guesses:
            guesses.remove(board[lr+i/root][lc+i%root])
    return guesses

def getBoard(possibilities):
    n=len(possibilities)
    return map(lambda row:map(lambda col:possibilities[row][col][0] if
                              len(possibilities[row][col])==1 else 0,
                              range(n)),range(n))

def getCellsToInspect(possibilities):
    cellsToInspect=[]
    n=len(possibilities)
    for row in xrange(n):
        for col in xrange(n):
            if len(possibilities[row][col])>1: cellsToInspect.append((row,col))
            else:
                assert len(possibilities[row][col])>0
    return cellsToInspect

#I only make good guesses, so if I get to the end I've solved it
def guessedRight(board,cellsToInspect,index,guess):
    board[cellsToInspect[index][0]][cellsToInspect[index][1]]=guess
    if index==len(cellsToInspect)-1: return True
    possibleGuesses=getGuesses(board,cellsToInspect[index+1])
    if len(possibleGuesses)==0: return False
    for newGuess in possibleGuesses:
        if guessedRight(board,cellsToInspect,index+1,newGuess): return True
    board[cellsToInspect[index+1][0]][cellsToInspect[index+1][1]]=0
    return False

################################################################################
################################ turboSolve ####################################
################################################################################

#VERSION 2.0
def turboSolve(canvas):
    board,n,root=getBoard(canvas.data.startingBoard)
    candidates,counts=getCandidatesAndCounts(board,n)
    if len(candidates)==0: return True
    minCount,minRow,minCol=n+1,-1,-1
    for row,col in candidates:
        count=counts[row][col]
        if count<minCount: minCount,minRow,minCol=count,row,col
        if count==2: break #the 0s and 1s are caught in getBoard
    for guess in board[minRow][minCol]:
        if rightNumber(board,counts,minRow,minCol,candidates,guess,root):
            canvas.data.board=board
            return True
    return False

#I did this functionally before, but it was a tiny bit slower
def getBoard(startingBoard):
    n=len(startingBoard)
    root=int(math.sqrt(n))
    board=[0]*n
    for row in xrange(n):
        board[row]=[0]*n
        for col in xrange(n):
            board[row][col]=pencilIn(startingBoard,row,col,n,root)
    return board,n,root

#start with all values possible, then remove everything else
def pencilIn(board,row,col,n,root):
    if board[row][col]!=0: return board[row][col]
    lr,lc,numbers=row/root*root,col/root*root,range(1,n+1)
    for i in xrange(n): #looking through the rest of the board
        if board[row][i] in numbers: numbers.remove(board[row][i])
        if board[i][col] in numbers: numbers.remove(board[i][col])
        (dr,dc)=divmod(i,root)
        if board[lr+dr][lc+dc] in numbers:
            numbers.remove(board[lr+dr][lc+dc])
    assert len(numbers)>0 #invalid board
    return numbers if len(numbers)>1 else numbers[0]

#everywhere that starts out as a number will have a count of -1
def getCandidatesAndCounts(board,n):
    candidates=[]
    counts=[0]*n
    for row in xrange(n):
        counts[row]=[-1]*n
        for col in xrange(n):
            if type(board[row][col])==list:
                candidates.append((row,col))
                counts[row][col]=len(board[row][col])
    return candidates,counts

#make the guess:
#if that was the last guess: return True
#look through the candidates for inspection (the unsolved squares):
    #if you find an empty list, undo the move and return False
    #pick the shortest list, and make each guess in it
#if none of the guesses were right, undo the move and return False    
def rightNumber(board,counts,row,col,candidates,guess,root):
    newChanges,oldOptions=makeGuess(board,counts,row,col,guess,candidates,root)
    if len(candidates)==0: return True
    minCount,minR,minC=root*root+1,0,0
    for r,c in candidates:
        count=counts[r][c]
        if count==0:
            unmakeGuess(board,counts,guess,newChanges)
            board[row][col]=oldOptions
            candidates.append((row,col))
            return False
        if count<minCount: minCount,minR,minC=count,r,c
        if count==1: break #you see the later 0s faster this way (unproven) 
    #no copy is necessary: it's being broken and fixed in the loop each time
    for newGuess in board[minR][minC]:
        if rightNumber(board,counts,minR,minC,candidates,newGuess,root):
            return True
    unmakeGuess(board,counts,guess,newChanges)
    board[row][col]=oldOptions
    candidates.append((row,col))
    return False

#interesting: since I remove row,col from my candidates and I
    #only reference counts with respect to my candidates, I don't have to change
    #my counts[row][col] when I remove row,col form candidates: I can leave
    #it as is and it won't be incremented or decremented at all
#remember, the actual row,col is NOT in newChanges
def makeGuess(board,counts,row,col,guess,candidates,root):
    lr,lc=row/root,col/root
    oldOptions=board[row][col] #does NOT need to be copied: overwrite != change
    candidates.remove((row,col))
    board[row][col]=guess #not modifying, so no alias trouble with oldOptions
    newChanges=[]
    for possR,possC in candidates:
        if ((possR==row or possC==col or (possR/root==lr and possC/root==lc))
            and guess in board[possR][possC]):
            board[possR][possC].remove(guess)
            counts[possR][possC]-=1
            newChanges.append((possR,possC))
    return newChanges,oldOptions

#note: this does not fix board[row][col], only it's neighbors
def unmakeGuess(board,counts,guess,newChanges):
    for fixRow,fixCol in newChanges:
        board[fixRow][fixCol].append(guess)
        counts[fixRow][fixCol]+=1

################################################################################
################################ logicSolve ####################################
################################################################################


#idea:
    #rank the options by order of difficulty:
        #naked singles = 0
        #hidden singles = 1
        #naked pairs = 2
        #hidden pairs = 3
        #naked triples = 4
        #hidden triples = 5
        #...
        #
        #h/n 1 = 1
        #h/n 2 = 2
        #...
        #h/n x = x
    #apply them across the entire board, breadth-first, one-at-a-time
    #record which cells are changed
        #for every changed cell:
            #apply all the SIMPLER rules on that cell's row, column and box
            #again, keep track of the changes (recursion!)
    
#http://www.sudokuwiki.org/Sudoku.htm

def logicSolve(canvas):
    possibleValues=findPossibleValueBoard(canvas.data.startingBoard)
    n=len(possibleValues)
    solvedSquares=map(lambda row:map(lambda col:
                                     len(possibleValues[row][col])==1,
                                     range(n)),range(n))
    difficultyCap=n
    for i in xrange(1,difficultyCap):
        applyRuleEverywhere(possibleValues,solvedSquares,i)
        if isSolved(solvedSquares):
            canvas.data.board=map(lambda row:map(lambda col:
                                                 possibleValues[row][col][0],
                                                 range(n)),range(n))
            return True
    print "logicSolve could not crack it..."
    print "either the board was unfair, or I am incomplete."
    print possibleValues
    return False

def findPossibleValueBoard(startingBoard):
    n=len(startingBoard)
    return map(lambda row:
               map(lambda col:getNumsLeft(startingBoard,row,col),range(n)),
               range(n))

#start with all values possible, then remove everything else
def getNumsLeft(startingBoard,row,col):
    if startingBoard[row][col]!=0: return[startingBoard[row][col]]
    n=len(board)
    root=int(math.sqrt(n))
    lr,lc,numsLeft=row/root*root,col/root*root,range(1,n+1)
    for i in xrange(n): #looking through the rest of the board
        if startingBoard[row][i] in numsLeft:
            numsLeft.remove(startingBoard[row][i])
        if startingBoard[i][col] in numsLeft:
            numsLeft.remove(startingBoard[i][col])
        if startingBoard[lr+i/root][lc+i%root] in numsLeft:
            numsLeft.remove(startingBoard[lr+i/root][lc+i%root])
    return numsLeft

def isSolved(solvedSquares):
    n=len(solvedSquares)
    for row in xrange(n):
        for col in xrange(n):
            if solvedSquares[row][col]==False: return False
    return True

def applyRuleEverywhere(possibleValues,solvedSquares,ruleNumber):
    assert ruleNumber>0
    findAllNSets(possibleValues,solvedSquares,ruleNumber)

def findAllNSets(possibleValues,solvedSquares,size):
    n=len(possibleValues)
    for i in xrange(n):
        checkIthRow(possibleValues,solvedSquares,size,i)
        checkIthCol(possibleValues,solvedSquares,size,i)
        checkIthBox(possibleValues,solvedSquares,size,i)

def checkIthRow(possibleValues,solvedSquares,size,i):
    checkHiddensRowI(possibleValues,solvedSquares,size,i)
    checkNakedsRowI(possibleValues,solvedSquares,size,i)

#n choose k (subset=[])
def combinations(listy,k,subset):
    if k==0: yield subset
    elif len(listy)>0:
        first=listy[0]
        rest=listy[1:]
        for c in combinations(rest,k-1,subsets+[first]):yield c
        for c in combinations(rest,k,subsets):yield c

#for each combination of i cells in the row, check if there's a set of i in it
    #for each potential set of i, make sure it's nowhere else in the row
def checkHiddensRowI(possibleValues,solvedSquares,size,i):
    n=len(possibleValues)
    possibleCells=range(n)
    for col in xrange(n):
        if solvedSquares[i][col]: possibleCells.remove(col)
    for combination in combinations(possibleCells,size,[]):
        pass

def checkNakedsRowI(possibleValues,solvedSquares,size,i):
    n=len(possibleValues)

def checkIthCol(possibleValues,solvedSquares,size,i):
    pass

def checkIthBox(possivleBalues,solvedSquares,size,i):
    pass
