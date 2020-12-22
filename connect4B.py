# Project: Connect 4 AI
# Project name: connect4B.py
# Author: Greg Tystahl
# Date Created: 10/08/2020
# Purpose: Have the AI win against all other AI and tie itself the majority of the time

# Revision History:

# How to run: python connect4B.py
# (The rest is asked by the program)

import copy
import sys
MINUS_INFINITY=-10000000
POSITIVE_INFINITY=10000000
Dmax = 6

# Didn't use this class
class Node(object):
    def __init__(self,board):
        self.board=board

    def getBoard(self):
        return self.board


# This is the AI agent
class agentC4(object):
    def __init__(self, pnum):
        # Sets the player number on creation
        self.player = pnum

    def getMove(self, board):
        # This gets the move of the AI

        # Starts out at -1
        move = -1

        # If the AI is player 1
        if self.player == 1:
            # Start with max and go to min
            move = self.maxmin(board, self.player)
        elif self.player == 2: # If the AI is player 2
            # Start with min and go to max
            move = self.minmax(board, self.player)
        else:
            print("There is an initialization problem")

        # If the move comes back and there is nowhere to go
        if move == -1:
            # Gets the list of actions available
            actions = self.availableActions(board, self.player)

            # Gets the first action possible to continue the game
            move = actions[0][0]

        # This returns the chosen move
        return move

            
    def availableActions(self, board, player):

        # This stands for spaces accounted for ()
        saf = [0,0,0,0,0,0,0]

        # This is the action list that will be returned at the end
        actions=[]

        # This goes through the whole board square by square
        for rownum in range(0, len(board)):
            for spacenum in range(0, len(board[rownum])):
                space = board[rownum][spacenum]

                # tries to find the topmost occupied spot
                if space != 0:
                    # If it finds it but not on the top row
                    if saf[spacenum] == 0 and rownum != 0:
                        # Add the space to the accounted for and create the next state
                        saf[spacenum] = 1
                        newboard = copy.deepcopy(board)
                        newboard[rownum - 1][spacenum] = player
                        # Move with action list
                        mwal = [spacenum, newboard]

                        # Adds the action to the action list
                        actions.append(mwal)
                    elif rownum == 0:
                        saf[spacenum] = 1

                # If there is no topmost add it here
                elif space == 0 and rownum == 5:
                    # Add the space to the action
                    newboard = copy.deepcopy(board)
                    newboard[rownum][spacenum] = player
                    mwal = [spacenum, newboard]

                    # Add action to the actions list
                    actions.append(mwal)
                        
        # return the action list after things have been added to it
        return actions
    
    # If the AI is player 2
    def minmax(self, board, player):
        # Sets the move to something impossible
        move = -1

        # Gets the next move
        v, move = self.minval(board, MINUS_INFINITY, POSITIVE_INFINITY, move, 0, 2)

        # Returns the next move
        return move

    # If the AI is player 1
    def maxmin(self, board, player):
        # Sets the move to something impossible
        move = -1

        # Gets the next move
        v, move = self.maxval(board, MINUS_INFINITY, POSITIVE_INFINITY, move, 0, 1)

        # Returns the next move
        return move
    
    def maxval(self, board, alpha, beta, move, depth, player):

        # Increases the depth
        depth += 1

        # Checks to see if the depth is at the max
        if (depth >= Dmax):
            # Evaluated the board
            evaluate = evaluation(board, move)

            # Returns the evaluation and move
            return evaluate, move
        
        # Action with move list
        awml = self.availableActions(board, player)

        # Sets the comp val to neg infinity
        val = MINUS_INFINITY

        # Action with move
        for awm in awml:

            # Gets the next move
            nextmove = awm[0]
            
            # Gets the action
            action = awm[1]

            # Checks to see if this action wins the game
            p, t = checkWin(action)

            if t:
                # Checks to make sure that it isnt a stalemate win
                if p != -1:
                    # Returns a large value to trigger this as the best action
                    return POSITIVE_INFINITY * 2, nextmove

            # Gets the value and the move of the minval
            val2, move2 = self.minval(action, alpha, beta, nextmove, depth, 2)

            # Compares val2 against the retval
            if val2 >= val: # If the new val is greater use that one
                # Set the retval equal to the newval
                val = val2

                # Set the move to the move that was in question when it was sent to the eval
                # Works better to use next move instead of move2
                move = nextmove

                # Sets alpha equal to whats greater, val or alpha
                alpha = max([val, alpha])

            # If val is greater than beta
            if val > beta:
                # Return that value and move
                return val, move

        # Returns the chosen val and move at the end
        return val, move

    def minval(self, board, alpha, beta, move, depth, player):

        # Adds one to the depth
        depth += 1

        # Checks to see if the alg is at max depth
        if (depth >= Dmax):
            # If it is evaluate the board
            evaluate = evaluation(board, move)

            # return the move and evaluation of the board
            return evaluate, move
        
        # Action with move list
        awml = self.availableActions(board, player)

        # This is the retval set to really high
        val = POSITIVE_INFINITY
        
        # Action with move
        for awm in awml:
            # Gets the next move
            nextmove = awm[0]
            
            # Gets the action
            action = awm[1]

            # Checks to see if it is a win state
            p, t = checkWin(action)

            # If it is
            if t:
                # And it isn't a stalemate
                if p != -1:
                    # Return the move and a big negative num
                    return MINUS_INFINITY * 2, nextmove

            # This gets the val and move of maxval
            val2, move2 = self.maxval(action, alpha, beta, nextmove, depth, 1)

            # Checks to see if the new val is less than the old val
            if val2 <= val: # If it is
                # Sets the retval to val2
                val = val2

                # Sets the move to the move that was sent to max
                move = nextmove

                # Sets beta to be the smallest of the new val and itself
                beta = min([val, beta])

            # If the val in question is smaller than alpha
            if val < alpha:
                # Return it cause it doesn't need to be looked at
                return val, move

        # After checking everything, return the val and move
        return val, move

def H1(board, player):
    # This H is for determining the value based on all connections
    # The scores are based on this per connection found:
    #   1 is nothing
    #   2 is 4
    #   3 is 16
    #   4 is 164
    # 4 in a row is also counted by having a possible open space or spaces since the next moves could be placed there

    # This is the value that will be returned at the end
    value = 0

    # This goes through each space on the board
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            # Checks to make sure the space is equal to the player and not zero
            if space != 0 and space == player:

                # These values are used to determine the scales shown at the beginning
                # The booleans are used to find 4 in a row
                hor = True
                horval = 1
                ver = True
                verval = 1
                diagr = True
                diagrval = 1
                diagl = True
                diaglval = 1

                # This goes and looks at the next three spaces
                for i in range(1, 4):

                    # Horizontal
                    # Tries to find the next horizontal space
                    try:
                        # If it is not equal to the space, set hor to false
                        if board[rownum][spacenum + i] != space:
                            hor = False
                        elif board[rownum][spacenum + i] == space or board[rownum][spacenum + i] == 0: #If the next space is open or the same
                            # Set the horval to *= 4
                            horval *= 4
                    except:
                        # If the space cannot exist then it cannot be 4 in a row
                        hor = False

                    # This is vertical and works the exact same as above with minor changes
                    try:
                        if board[rownum + i][spacenum] != space:
                            ver = False
                        elif board[rownum + i][spacenum] == space or board[rownum + i][spacenum] == 0:
                            verval *= 4
                    except:
                        ver = False

                    # This is diagonal right and it works a bit different than the rest
                    # Each if statement it checks to make sure the spacenum is not negative cause if it is
                    # Python uses that value and will grab something that it shouldnt
                    try:
                        if board[rownum + i][spacenum - i] != space or spacenum - 1 < 0:
                            diagr = False
                        elif (board[rownum + i][spacenum - i] == space or board[rownum + i][spacenum - i] == 0) and spacenum - 1 >= 0:
                            diagrval *= 4
                    except:
                        diagr = False

                    # This is diagonal left and works like ver and hor
                    try:
                        if board[rownum + i][spacenum + i] != space:
                            diagl = False
                        elif board[rownum + i][spacenum + i] == space or board[rownum + i][spacenum + i] == 0:
                            diaglval *= 4
                    except:
                        diagl = False

                # For each of these ifs, if the possibility for 4 in a row is still good, add 100
                if hor:
                    value += 100

                if ver:
                    value += 100

                if diagl:
                    value += 100

                if diagr:
                    value += 100

                # For each of these ifs, if the final val is greater than one
                # (Since singles that are trapped are ignored) add the value to the overall value
                if horval != 1:
                    value += horval

                if verval != 1:
                    value += verval

                if diagrval != 1:
                    value += diagrval

                if diaglval != 1:
                    value += diaglval

    # Return the overall value
    return value

def H2(b, player):
    # This tries to find 3 in a row that can be completed from either side and if it can go for that

    # This is the final return value
    val = 0

    #This gets a copy of the board
    board = copy.deepcopy(b)

    # Three row list. Used to hold all three connections
    trl = []

    # This is used to keep track of what spaces have already been checked to not be checked again
    checknum = 3

    # Goes through each space in the board
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            # These are the bools that will hold is a possible is found
            hor = True

            diagr = True

            diagl = True

            # Checks to make sure the space is not zero or another player or if it is greater than the original checkval
            if (space != 0 and space == player) or space >= 3:
                # Changes that space to checknum
                board[rownum][spacenum] = checknum

                # Goes though a range of 3 to find 3 connections
                for i in range(1, 3):
                    # Horizontal
                    try:
                        # Gets the nextspace
                        nextspace = board[rownum][spacenum + i]

                        # if nextspace is the player or nextpace is a checkval and not itself
                        if nextspace == player or (nextspace >= 3 and not nextspace == space):
                            # Change the nextval to the new checknum
                            board[rownum][spacenum + i] = checknum
                        else:
                            # If it is blocked and no three in a row, set hor to false
                            hor = False
                    except:
                        # If there is an error then hor is false
                        hor = False

                    # This is diagonal left. Same as horizontal above
                    try:
                        nextspace = board[rownum + i][spacenum + i]
                        if nextspace == player or (nextspace >= 3 and not nextspace == space):
                            board[rownum + i][spacenum + i] = checknum
                        else:
                            diagl = False
                    except:
                        diagl = False

                    # This is diagonal right. It needs to check to make sure spacenum is greater than zero
                    # Otherwise it is the same as above
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

                # If the 3 in a row holds for any of the direction, add it to three row list
                if hor:
                    trl.append([0, rownum, spacenum])
                if diagl:
                    trl.append([1, rownum, spacenum])
                if diagr:
                    trl.append([2, rownum, spacenum])

                checknum += 1

    # Goes through each item in three row list
    for item in trl:
        # type
        t = item[0]

        # rownum
        rn = item[1]

        # spacenum
        sn = item[2]

        # Horizontal
        if t == 0:
            # Sets a good value to be checked later
            good = True
            # If the spacenum is greater than zero
            if sn - 1 >= 0:
                # Gets the backspace of the row
                backspace = board[rn][sn - 1]

                # If it is not equal to zero then it sets good to false
                if backspace != 0:
                    good = False

                # Tries to get the frontspace if possible
                try:
                    # Gets frontspace
                    frontspace = board[rn][sn + 3]

                    # If frontspace is not 0 then good is false
                    if frontspace != 0:
                        good = False
                except:
                    # If there are any errors good is auto false
                    good = False
            else:
                # If spacenum isnt possible then good is false
                good = False

            if good:
                # If the row passes the test then 300 is added to its score
                val += 300

        # Diagonal right. Works very similar to above with minor extra checks of positivity
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

        # Diagonal left. Works closely to diagonal right with less positivity checks for frontspace
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

    # Returns the final value after the good tests
    return val

def H3(board, move):
    # This h is used to get the AI to try to play closer to the middle where there are more options to go

    # This is the final return value
    val = 0

    # This is the value of change for this h
    change = 5

    # This finds the row that space is on
    for rn in range(0, len(board)):
        space = board[rn][move]
        if space != 0:
            rownum = rn
            break

    # Tries to see if it can go up
    try:
        nextspace = board[rownum + 1][move]
        if (nextspace == 0):
            # If it can then add change to overall val
            val += change
    except:
        # If it cant then nothing is added
        val += 0

    # Tries to see if it can go right
    try:
        nextspace = board[rownum][move + 1]
        if (nextspace == 0):
            # If it can then add change
            val += change
    except:
        # If it cant then nothing is added
        val += 0

    # Tries to go left
    if move - 1 >= 0:
        nextspace = board[rownum][move - 1]
        if nextspace == 0:
            # If it can then add change
            val += change

    # Return the final val after the change
    return val


def evaluation(board, move):
    # This is the function that determines the value of the board
    # What it is intended to do is take the value of itself and subtract the value of its opponent.
    # This makes it so that the AI really wants to win, but would rather tie than lose

    return (H1(board, 1) + H2(board, 1) + H3(board, move)) - 2 * (H1(board, 2) + H2(board, 2))
        


class gameC4(object):
    # Untouched by me

    def __init__(self):
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
    # This checks to see if someone has won

    # This checks to see if the board is full and it is a stalemate
    stale = True

    # This is the board we will be checking
    board = copy.deepcopy(game)
    
    # This goes through each of the rows in the board
    for rownum in range(0, len(board)):
        for spacenum in range(0, len(board[rownum])):
            space = board[rownum][spacenum]

            # If there is a free space there is not stalemate
            if space == 0 and stale:
                stale = False

            # If the space is not empty
            if space != 0:

                # These are the booleans for true 4 in a row
                hor = True
                ver = True
                diagl = True
                diagr = True

                # Finds horizontal, vertical, diagleft, diagright
                for i in range(1, 4):
                    # Horizontal
                    try:
                        # Tries to get the next space and checks to see if it is the same as the beginning space
                        if board[rownum][spacenum + i] != space:
                            # If it isnt then hor is false
                            hor = False
                    except:
                        # If there is an error then it cant be 4 in a row
                        hor = False

                    # Vertical. Works just like horizontal
                    try:
                        if board[rownum + i][spacenum] != space:
                            ver = False
                    except:
                        ver = False

                    # Diagonal right. Works like above but has extra spacenum positive check
                    try:
                        if spacenum - i >= 0:
                            if board[rownum + i][spacenum - i] != space:
                                diagr = False
                        else:
                            diagr = False
                    except:
                        diagr = False

                    # Diagonal left works like the first 2
                    try:
                        if board[rownum + i][spacenum + i] != space:
                            diagl = False
                    except:
                        diagl = False

                # If there are any wins possible in this config, return true and the winning player num
                if hor or ver or diagl or diagr:
                    return space, True

    # If stale is still true then the game is a stalemate
    if stale:
        return -1, True

    # There were no wins so return false
    return -1, False

def main():

    # Creates the game object
    C4=gameC4()

    # Sets the players set
    players = ["", "O","X"]

    # Allows the user to choose to watch the AI fight itself or to play against it
    aoh = input("AI vs or Human? ('a' or 'h') ")

    # This is the player count used to determine whose turn it is
    ply = 0

    # If the user chose to play the AI
    if aoh == "h":
        # Who goes first
        wgf = int(input("Who goes first? (1 for O, 2 for X) "))

        # This is used for determining whose turn it is based on what the user chooses
        order = [0,0]

        # If the user chooses for the AI to go first
        if wgf == 1:
            # Set the first item in order to the agent
            agent = agentC4(1)
            order[0] = agent
        elif wgf == 2: # If they chose to go first then set the agent to order item 2
            agent = agentC4(2)
            order[1] = agent

        # This is the game and will run till someone wins
        while True:
            # Displays the board
            C4.displayBoard()

            # Prints the players turn
            print("Player " + players[((ply % 2) + 1)] + " turn.")

            # If it is the players turn
            if order[ply%2] == 0:
                # This is used to check the players move
                good = False
                try:
                    # Gets the users input
                    column = input("Enter a column to drop: ")

                    # If the players wants they can exit although they never should
                    if (column == "exit"):
                        return 0

                    # Tries to make the users input an int
                    column = int(column)

                    # If it does then set good to true
                    good = True
                except ValueError:
                    # This catches that the user put something that they shouldnt have
                    print("That is not an allowed command")

                # If the player put something that was good then it tries to use that command
                if good:
                    try:
                        # Tries to drop at their number
                        C4.drop((ply%2) + 1,column)

                        # Flip the turn
                        ply += 1
                    except Full:
                        # If they cant then they try again
                        print("try again")

            else: # If it is the AIs turn
                # Get the move of the agent
                mv = agent.getMove(C4.getCurrentBoard())

                # drop at the move specified
                C4.drop(agent.player, mv)

                # Print the move of the AI
                print("Move: " + str(mv))

                # Flip the turn
                ply += 1

            # Checks to see if someone has one
            player, terminal = checkWin(C4.getCurrentBoard())

            # If someone has won
            if terminal and player != -1:
                # Display that they have one and break
                C4.displayBoard()
                print(players[player] + " has won.")
                break
            elif terminal and player == -1: # If it is a stalemate
                # Display that it is a stalemate and break
                C4.displayBoard()
                print("The board is a stalemate")
                break

    elif aoh == "a": # If the AI are vs each other
        # Create two AIs
        agent1 = agentC4(1)
        agent2 = agentC4(2)

        while True:
            # Displays the board
            C4.displayBoard()

            # If its AI 1s turn
            if (ply % 2) == 0:
                # Get the move, play the move, flip the turn
                mv = agent1.getMove(C4.getCurrentBoard())
                C4.drop(agent1.player, mv)
                print("Move: " + str(mv))
                ply += 1
            else: # If it is AI 2s turn
                # Get the move, play the move, flip the turn
                mv = agent2.getMove(C4.getCurrentBoard())
                C4.drop(agent2.player, mv)
                print("Move: " + str(mv))
                ply += 1

            # Check to see if anyone has won
            player, terminal = checkWin(C4.getCurrentBoard())

            # If someone has
            if terminal and player != -1:
                # Display who won and and break
                C4.displayBoard()
                print(players[player] + " has won.")
                break
            elif terminal and player == -1: # If it is a stalemate
                # Display its a stalemate and break
                C4.displayBoard()
                print("The board is a stalemate")
                break


if __name__ == "__main__":
    main()
