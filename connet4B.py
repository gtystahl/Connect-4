# connect 4
#TODO: Change things so that it wins. It looks like it wins too fast though and that might be a problem
#TODO: Loses to defense because it doesnt detect x * x * as a huge potential bad
#TODO: Clean up h cause its not working at all. doesnt keep up with terminal state
#TODO: Does well when it goes first. Can defend ok but needs to start in the middle more

import copy
import sys
MINUS_INFINITY=-10000000
POSITIVE_INFINITY=10000000
Dmax = 6
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

        if move == -1:
            actions = self.availableActions(board, self.player)
            if len(actions) == 1:
                move = actions[0][0]

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
                    elif rownum == 0:
                        saf[spacenum] = 1

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
            evaluate = evaluation(board, move)

            #print(evaluate)

            #print("Board: ")
            #print(board)
            #print("Evaluate: " + str(evaluate))

            return evaluate, move

        #print("It made it past the if statement maxval")
        
        #Action with move list
        awml = self.availableActions(board, player)

        val = MINUS_INFINITY
        #Action with move
        for awm in awml:

            #Gets the next move
            nextmove = awm[0]
            
            #Gets the action
            action = awm[1]

            p, t = checkWin(action)

            if t:
                return POSITIVE_INFINITY * 2, nextmove

            #print(action)

            val2, move2 = self.minval(action, alpha, beta, nextmove, depth, 2)

            if val2 >= val:
                val = val2
                move = nextmove
                alpha = max([val, alpha])

            if val > beta:
                return val, move

        return val, move


    def minval(self, board, alpha, beta, move, depth, player):

        #player = (player % 2) + 1
        #print(player)

        depth += 1

        if (depth >= Dmax):
            evaluate = evaluation(board, move)

            #print(evaluate)

            #print("Board: ")
            #print(board)
            #print("Evaluate: " + str(evaluate))

            return evaluate, move

        #print("It made it past the if statement minval")
        
        #Action with move list
        #print(board)
        awml = self.availableActions(board, player)

        val = POSITIVE_INFINITY
        
        #Action with move
        for awm in awml:
            #Gets the next move
            nextmove = awm[0]
            
            #Gets the action
            action = awm[1]

            p, t = checkWin(action)

            if t:
                return MINUS_INFINITY * 2, nextmove

            #print(action)

            val2, move2 = self.maxval(action, alpha, beta, nextmove, depth, 1)

            if val2 <= val:
                val = val2
                move = nextmove
                beta = min([val, beta])

            if val < alpha:
                return val, move

        return val, move

def H1(board, player):
    #This H is for determining the value based on all connections
    #The scores are based on this:
        #1 is nothing
        #2 is 4
        #3 is 16
        #4 is 164

    #This is used to make sure it doesnt check the same path twice
    checkb = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    value = 0
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            if space != 0 and space == player:
                hor = True
                horval = 1
                ver = True
                verval = 1
                diagr = True
                diagrval = 1
                diagl = True
                diaglval = 1

                for i in range(1, 4):
                    try:
                        if board[rownum][spacenum + i] != space:
                            hor = False
                        elif board[rownum][spacenum + i] == space or board[rownum][spacenum + i] == 0:
                            horval *= 4
                    except:
                        hor = False

                    try:
                        if board[rownum + i][spacenum] != space:
                            ver = False
                        elif board[rownum + i][spacenum] == space or board[rownum + i][spacenum] == 0:
                            verval *= 4
                    except:
                        ver = False

                    try:
                        if board[rownum + i][spacenum - i] != space or spacenum - 1 < 0:
                            diagr = False
                        elif (board[rownum + i][spacenum - i] == space or board[rownum + i][spacenum - i] == 0) and spacenum - 1 >= 0:
                            diagrval *= 4
                    except:
                        diagr = False

                    try:
                        if board[rownum + i][spacenum + i] != space:
                            diagl = False
                        elif board[rownum + i][spacenum + i] == space or board[rownum + i][spacenum + i] == 0:
                            diaglval *= 4
                    except:
                        diagl = False

                if hor:
                    value += 100

                if ver:
                    value += 100

                if diagl:
                    value += 100

                if diagr:
                    value += 100

                if horval != 1:
                    value += horval

                if verval != 1:
                    value += verval

                if diagrval != 1:
                    value += diagrval

                if diaglval != 1:
                    value += diaglval

    return value

def H2(b, player):
    #This tries to find 3 in a row that can be completed from either side and if it can go for that

    val = 0

    board = copy.deepcopy(b)

    # Three row list
    trl = []

    checknum = 3

    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            hor = True

            ver = True

            diagr = True

            diagl = True

            if (space != 0 and space == player) or space >= 3:
                board[rownum][spacenum] = checknum

                for i in range(1, 3):
                    try:
                        nextspace = board[rownum][spacenum + i]
                        if nextspace == player or (nextspace >= 3 and not nextspace == space):
                            board[rownum][spacenum + i] = checknum
                        else:
                            hor = False
                    except:
                        hor = False

                    try:
                        nextspace = board[rownum + i][spacenum + i]
                        if nextspace == player or (nextspace >= 3 and not nextspace == space):
                            board[rownum + i][spacenum + i] = checknum
                        else:
                            diagl = False
                    except:
                        diagl = False

                    try:
                        if spacenum - i >= 0:
                            nextspace = board[rownum + i][spacenum - i]
                            if nextspace == player or (nextspace >= 3 and not nextspace == space):
                                board[rownum + i][spacenum - i] = checknum
                            else:
                                diagr = False
                        else:
                            diagr = False
                    except:
                        diagr = False

                if hor:
                    trl.append([0, rownum, spacenum])
                if diagl:
                    trl.append([1, rownum, spacenum])
                if diagr:
                    trl.append([2, rownum, spacenum])

                checknum += 1

    for item in trl:
        # type
        t = item[0]

        # rownum
        rn = item[1]

        # spacenum
        sn = item[2]

        # Horizontal
        if t == 0:
            good = True
            if sn - 1 >= 0:
                backspace = board[rn][sn - 1]
                if backspace != 0:
                    good = False
                try:
                    frontspace = board[rn][sn + 3]
                    if frontspace != 0:
                        good = False
                except:
                    good = False
            else:
                good = False

            if good:
                val += 300

        # Diag Right
        if t == 1:
            good = True
            if sn - 3 >= 0:
                try:
                    backspace = board[rn + 3][sn - 3]
                    if backspace != 0:
                        good = False
                except:
                    good = False
                if rn - 1 >= 0:
                    try:
                        frontspace = board[rn - 1][sn + 1]
                        if frontspace != 0:
                            good = False
                    except:
                        good = False
                else:
                    good = False
            else:
                good = False

            if good:
                val += 300

        # Diag Left
        if t == 2:
            good = True
            if sn - 1 >= 0 and rn - 1 >= 0:
                backspace = board[rn - 1][sn - 1]
                if backspace != 0:
                    good = False

                try:
                    frontspace = board[rn + 3][sn + 3]
                    if frontspace != 0:
                        good = False
                except:
                    good = False
            else:
                good = False

            if good:
                val += 300


    return val

def H3(board, move):
    val = 0
    change = 5
    
    space = -1
    for rownum in range(0, len(board)):
        space = board[rownum][move]
        if space != 0:
            break

    try:
        nextspace = board[rownum + 1][move]
        if (nextspace == 0):
            val += change
    except:
        val += 0

    try:
        nextspace = board[rownum][move + 1]
        if (nextspace == 0):
            val += change
    except:
        val += 0

    if move - 1 >= 0:
        nextspace = board[rownum][move - 1]
        if nextspace == 0:
            val += change


        
        
    return val


def evaluation(board, move):
    return (H1(board, 1) + H2(board, 1) + H3(board, move)) - 2 * (H1(board, 2) + H2(board, 2))
        


class gameC4(object):
    def __init__(self):
        #self.board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,2,0,0],
         #           [0,0,0,0,1,2,0],[0,2,1,2,1,1,2],[0,2,2,1,2,1,1]]
        # Good board
        self.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

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

    #This checks to see if the board is full and it is a stalemate
    stale = True

    #This is the board we will be checking
    board = copy.deepcopy(game)
    
    #This goes through each of the rows in the board
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            if space == 0 and stale:
                stale = False

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
                        if spacenum - i >= 0:
                            if board[rownum + i][spacenum - i] != space:
                                diagr = False
                        else:
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

    if stale:
        return -1, True

    return -1, False

def main():


    C4=gameC4()
    
    player=["O","X"]
    aoh = input("AI vs or Human? ('a' or 'h') ")

    ply = 0

    if aoh == "h":
        # Who goes first
        wgf = int(input("Who goes first? (1 for O, 2 for X) "))
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
                mv = agent.getMove(C4.getCurrentBoard())
                C4.drop(agent.player, mv)
                print("Move: " + str(mv))
                ply += 1

            player, terminal = checkWin(C4.getCurrentBoard())

            if terminal and player != -1:
                C4.displayBoard()
                print(str(player) + " has won.")
                break
            elif terminal and player == -1:
                C4.displayBoard()
                print("The board is a stalemate")
                break

    elif aoh == "a":
        agent1 = agentC4(1)
        agent2 = agentC4(2)

        while True:
            C4.displayBoard()

            if (ply % 2) == 0:
                mv = agent1.getMove(C4.getCurrentBoard())
                C4.drop(agent1.player, mv)
                print("Move: " + str(mv))
                ply += 1
            else:
                mv = agent2.getMove(C4.getCurrentBoard())
                C4.drop(agent2.player, mv)
                print("Move: " + str(mv))
                ply += 1

            player, terminal = checkWin(C4.getCurrentBoard())

            if terminal and player != -1:
                C4.displayBoard()
                print(str(player) + " has won.")
                break
            elif terminal and player == -1:
                C4.displayBoard()
                print("The board is a stalemate")
                break






def trialstuff():
    agent = agentC4(0)
    game = gameC4()

    board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 1, 1, 2, 0], [0, 2, 1, 2, 1, 1, 2], [0, 2, 2, 1, 2, 1, 1]]

    #board = [[2,2,2,0,2,2,1],[1,1,1,0,1,1,1],[2,2,2,0,2,2,1],
                    #[2,1,2,0,1,1,2],[2,1,1,0,2,1,1],[1,2,1,0,2,2,1]]

    game.board = board
    
    game.displayBoard()

    #print(agent.H2(board, 2))
    #print(agent.availableActions(board, 1))
    print(checkWin(board))
    
if __name__=="__main__":
    main()
    #trialstuff()

    

