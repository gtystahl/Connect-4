# connect 4

import copy
import sys
MINUS_INFINITY=-10000000
POSITIVE_INFINITY=10000000
Dmax = 5
Tmax = 5

class Node(object):
    def __init__(self,board):
        self.board=board

    def getBoard(self):
        return self.board



class agentC4(object):
    def __init__(self, pnum):
        self.player = pnum

    def getMove(self, board):
        move = -1
        
        if self.player == 1:
            move = self.maxmin(board, self.player)
        elif self.player == 2:
            move = self.minmax(board, self.player)
        else:
            print("There is an initialization problem")

        return move

            
    def availableActions(self, board, player):

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
                    if saf[spacenum] == 0 and rownum != 0:
                        #Add the space to the accounted for and create the next state
                        saf[spacenum] = 1
                        newboard = copy.deepcopy(board)
                        newboard[rownum - 1][spacenum] = player
                        #Move with action list
                        mwal = [spacenum, newboard]
                        actions.append(mwal)

                #If there is no topmost add it here
                elif space == 0 and rownum == 5:
                    newboard = copy.deepcopy(board)
                    newboard[rownum][spacenum] = player
                    mwal = [spacenum, newboard]
                    actions.append(mwal)
                        
        #return the action list after things have been added to it                
        return actions
    
    # if O
    def minmax(self, board, player):
        move=-1

        v, move = self.minval(board, MINUS_INFINITY, POSITIVE_INFINITY, move, 0, 2)

        return move

    # if X
    def maxmin(self, board, player):
        move=-1

        v, move = self.maxval(board, MINUS_INFINITY, POSITIVE_INFINITY, move, 0, 1)
        
        return move
    
    def maxval(self, board, alpha, beta, move, depth, player):

        #player = (player % 2) + 1
        #print(player)
        
        depth += 1

        if (depth >= Dmax):
            evaluate = self.H1(board, player)

            print(evaluate)

            #print("Board: ")
            #print(board)
            #print("Evaluate: " + str(evaluate))

            return evaluate, move

        #print("It made it past the if statement maxval")
        
        #Action with move list
        awml = self.availableActions(board, player)

        if (len(awml) != 7):
            print("bad")

        val = MINUS_INFINITY
        #Action with move
        for awm in awml:
            #Gets the next move
            nextmove = awm[0]
            
            #Gets the action
            action = awm[1]

            #print(action)

            val2, move2 = self.minval(action, alpha, beta, nextmove, depth, 2)

            if val2 > val:
                val = val2
                move = move2
                alpha = max([val, alpha])

            if val >= beta:
                return val, move

        return val, move


    def minval(self, board, alpha, beta, move, depth, player):

        #player = (player % 2) + 1
        #print(player)

        depth += 1

        if (depth >= Dmax):
            evaluate = self.H1(board, player)

            print(evaluate)

            #print("Board: ")
            #print(board)
            #print("Evaluate: " + str(evaluate))

            return evaluate, move

        #print("It made it past the if statement minval")
        
        #Action with move list
        #print(board)
        awml = self.availableActions(board, player)

        if (len(awml) != 7):
            print("bad")

        val = POSITIVE_INFINITY
        
        #Action with move
        for awm in awml:
            #Gets the next move
            nextmove = awm[0]
            
            #Gets the action
            action = awm[1]

            #print(action)

            val2, move2 = self.maxval(action, alpha, beta, nextmove, depth, 1)

            if val2 < val:
                val = val2
                move = move2
                beta = min([val, beta])

            if val <= alpha:
                return val, move

        return val, move

    def H1(self, board, player):
        #This H is for determining the value based on all connections
        #The scores are based on this:
            #1 is nothing
            #2 is 1
            #3 is 3
            #4 is 6 (May also be caught by the terminal check)
        
        #This is used to make sure it doesnt check the same path twice
        checkb = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        value = 0
        for rownum in range(0, len(board)):
            for spacenum in range(0, len(board[rownum])):
                space = board[rownum][spacenum]

                if space != 0 and space == player:
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
                            if board[rownum + i][spacenum - i] != space or spacenum - 1 < 0:
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

    def h2(self, board, player):
        val = 0        
        
        return val
        


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
    board = copy.deepcopy(game)
    
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
    
    player=["O","X"]
    wgf = int(input("Who goes first? (1 for O, 2 for X) "))
    ply = 0
    order = [0,0]
    
    if wgf == 1:
        agent = agentC4(1)
        order[0] = agent
    elif wgf == 2:
        agent = agentC4(2)
        order[1] = agent
        
    while True:
        cb=C4.getCurrentBoard()

        C4.displayBoard()
        print("Player " + str((ply%2) + 1) + " turn.")

        if order[ply%2] == 0:
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

        else:
            C4.drop(agent.player, agent.getMove(C4.getCurrentBoard()))
            ply += 1

        player, terminal = checkWin(C4.getCurrentBoard())

        if terminal:
            C4.displayBoard()
            print(str(player) + " has won.")
            break

def trialstuff():
    agent = agentC4(0)
    game = gameC4()

    #board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,1],[0,0,0,0,0,0,2],
                    #[0,0,0,0,0,0,1],[1,0,0,0,0,0,1],[2,2,2,2,0,0,1]]

    board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0],[1,0,0,0,0,0,2],[1,1,0,0,0,0,2]]

    game.board = board
    
    game.displayBoard()

    print(agent.H1(board, 1))
    
if __name__=="__main__":
    main()
    #trialstuff()

    

