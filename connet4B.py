# connect 4

import copy
import sys
MINUS_INFINITY=-10000000
PLUS_INFINITY=10000000

class Node(object):
    def __init__(self,board):
        self.board=board

    def getBoard(self):
        return self.board



class agentC4(object):
    def __init__(self):
        self.dum=0

    def avaiableActions(self, board, player):

        #This stands for spaces accounted for ()
        saf = [0,0,0,0,0,0,0]

        #This is the action list that will be returned at the end
        actions=[]

        #This goes through the whole board square by square
        for rownum in range(0, len(board)):
            for spacenum in range(0, len(board[rownum])):
                space = board[rownum][spacenum]

                #tries to find the topmost occupied spot
                if space != 0:
                    #If it finds it but not on the top row
                    if saf[spacenum] != 0 and rownum != 0:
                        #Add the space to the accounted for and create the next state
                        saf[spacenum] = 1
                        newboard = copy.deepcopy(board)
                        newboard[rownum - 1][spacenum] = player
                        actions.append(newboard)

                    #If there is no topmost add it here
                    if saf[spacenum] == 0 and rownum == 5:
                        newboard = copy.deepcopy(board)
                        newboard[rownum][spacenum] = player
                        actions.append(newboard)
                        
        #return the action list after things have been added to it                
        return actions
    
    # if O
    def minmax(self,board):
        player = 0
        move=-1

        return move

    # if X
    def maxmin(self,board):
        player = 1
        move=-1
        return move
    
    def maxval(self,board,player):
        #Finds the best next move
        #Seems like this AI is more offensive than defensive. Might need to change

        player = (player % 2) + 1

        actions = availableActions(board, player)

        bestval = MINUS_INFINITY
        bestaction = None
        
        for a in actions:
            newval = findGoodVal(a)

            if newval > bestval:
                bestval = newval
                bestaction = a

        minval(bestaction, player)
        return None


    def minval(self, board, player):
        return None

    def findGoodVal(self, board):
        #This is used to make sure it doesnt check the same path twice
        checkb = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        value = 0
        for rownum in range(0, len(board)):
            for spacenum in range(0, len(board[rownum])):
                space = board[rownum][spacenum]

                if space != 0:
                    hor = True
                    ver = True
                    diagr = True
                    diagl = True
                    
                    for i in range(1, 4):
                        try:
                            if board[rownum][spacenum + i] != space:
                                hor = False
                            elif hor:
                                value += 1
                        except:
                            hor = False

                        try:
                            if board[rownum + i][spacenum] != space:
                                ver = False
                            elif ver:
                                value += 1
                        except:
                            ver = False

                        try:
                            if board[rownum + i][spacenum - i] != space:
                                diagr = False
                            elif diagr:
                                value += 1
                        except:
                            diagr = False

                        try:
                            if board[rownum + i][spacenum + i] != space:
                                diagl = False
                            elif diagr:
                                value += 1
                        except:
                            diagl = False
                

        return value


class gameC4(object):
    def __init__(self):
        self.board=[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

    #the move
    def drop(self,player,column):
        p=0
        for i in range(5,-1,-1):
            if self.board[i][column]==0:
                self.board[i][column]=player
                
                break
            p+=1
       

        if p==6:
            raise(Full)
            
   

    def displayBoard(self):
        symbol=["*","O","X"]
        print("  0 1 2 3 4 5 6")
        for i in range(6):
            print(i,end=" ")
            for j in range(7):
                print(symbol[self.board[i][j]],end=" ")

       

            print("\n")
        
    def getCurrentBoard(self):
        return self.board


    


class Exists(Exception):
    pass

class Full(Exception):
    pass

def checkWin(game):
    #This checks to see if someone has won

    #This is the board we will be checking
    board = copy.deepcopy(game.getCurrentBoard())
    
    #This goes through each of the rows in the board
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            if space != 0:

                hor = True
                ver = True
                diagl = True
                diagr = True
                #Finds horizontal, verticle, diagleft, diagright
                for i in range(1, 4):
                    try:
                        if board[rownum][spacenum + i] != space:
                            hor = False
                    except:
                        hor = False

                    try:
                        if board[rownum + i][spacenum] != space:
                            ver = False
                    except:
                        ver = False

                    try:
                        if board[rownum + i][spacenum - i] != space:
                            diagr = False
                    except:
                        diagr = False

                    try:
                        if board[rownum + i][spacenum + i] != space:
                            diagl = False
                    except:
                        diagl = False

                if hor or ver or diagl or diagr:
                    return space, True
    return -1, False

def main():


    C4=gameC4()
    O=agentC4()

    
    
    player=["O","X"]
    wgf = int(input("Who goes first? (1 for O, 2 for X) "))

    if wgf == 1:
        ply=0
    elif wgf == 2:
        ply=1
        
    while True:
        cb=C4.getCurrentBoard()

        moveO=O.minmax(cb)

        C4.displayBoard()
        print("Player " + str((ply%2) + 1) + " turn.")

        good = False
        try:
            column = input("Enter a column to drop: ")
            if (column == "exit"):
                return 0
            column = int(column)
            good = True
        except ValueError:
            print("That is not an allowed command")

        if good:
            try:
                # here is the human X player (the maxmin player)
                C4.drop((ply%2) + 1,column)
                ply += 1
            except Full:
                print("try again")

            player, terminal = checkWin(C4)

            if terminal:
                C4.displayBoard()
                print(str(player) + " has won.")
                break

if __name__=="__main__":
    main()


    

