#Michael Chouqette
#this file contains code for solving the maze

def solve(maze):
    rows,cols = len(maze),len(maze[0])
    return dfs(maze,0,0,rows-1,cols-1,[])

#ASSUMES: no cycles in the maze
def dfs(maze,row,col,targetRow,targetCol,path):
    if row==targetRow and col==targetCol: return path
    for (drow,dcol) in [(-1,0),(0,1),(1,0),(0,-1)]:
        #first check if we just came this way
        if len(path)>0 and (-drow,-dcol)==path[-1]: continue
        if isValidDir(maze,row,col,drow,dcol):
            path.append((drow,dcol))
            result = dfs(maze,row+drow,col+dcol,targetRow,targetCol,path)
            if result!=None: return result
            path.pop() #the result was None, so this path was invalid
    #if none of them work, this way is a dead end, so backtrack
    return None

def isValidDir(maze,row,col,drow,dcol):
    rows,cols = len(maze),len(maze[0])
    return (0<=row+drow<rows and 0<=col+dcol<cols and
            ((drow==-1 and maze[row-1][col].south) or
             (dcol==-1 and maze[row][col-1].east) or
             (drow==1 and maze[row][col].south) or
             (dcol==1 and maze[row][col].east)))
