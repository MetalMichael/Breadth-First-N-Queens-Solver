#!/usr/bin/env python

import sys
import copy
from os import system

import pprint

#Set the console title
system("title Michael Fiford - Breadth First N-Queen Solver")

class QueenSolver:
    #Store for the amount of queens we're placing, or table size
    tableSize = 0
    
    #The alphabet, for nice cell referencing on the output
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    #The queue of possibile moves that we will create and loop through
    queue = []
    
    #Whether or not the solver can be ran
    canRun = False
    
    #For Pretty Print output
    pp = False
    
    def setup(self, queenNumber):
        #Set the number of queens/table size
        self.tableSize = queenNumber
        
        #Can run, so long as there are no errors
        self.canRun = True
        
        #Show error if there is no solution, or would take too long
        if queenNumber < 4:
            print "ERROR: A solution is not available for this few number of queens"
            self.canRun = False
        elif queenNumber > 13:
            print "ERROR: This solution would take too long to calculate, and your computer would probably run out of memory first!"
            self.canRun = False
    
    #Create an empty table
    def blankTable(self):
        print "Creating a blank table"
        table = []
        for row in xrange(self.tableSize):
            new = []
            for col in xrange(self.tableSize):
                new.append(0);
            table.append(new)
        return table
    
    #Place a queen in a table
    def placeQueen(self, table, row, col):
        print "Placing a queen in " + self.alphabet[row] + str(col+1)
        #Copy the table, as python is annoying and will change both
        t2 = copy.deepcopy(table)
        t2[row][col] = 1
        return t2
    
    #The main program loop
    def loopBoard(self):
        #The column we are currently looking at
        col = 1
        #Loop while the queue isn't empty, and there are still move possibilities to explore
        while len(self.queue):
            print ""
            #Create a new empty queue
            print "Creating new, empty queue"
            queue2 = []
            #Update status
            print ""
            print col, "Queens Placed"
            
            print "Queue Status: (Length = " + str(len(self.queue)) + ")"
            for s in self.queue:
                self.display(s)
            
            #What column we are on. 0 indexed so add 1 for the user
            print "Looking at Column " + str(col+1)
            
            #Loop the queue, looking for positions from each status
            #s is an array containing the current queen positions for this status
            for s in self.queue:
                #An array of tables containing all moves that were posible  from this status
                print "Getting Moves"
                availableMoves = self.getPositions(s, col)
                #If we are placing the last queen, and there are solutions available, finish
                print "Checking if we are on the last queen (" + str(col+2) + " vs " + str(self.tableSize+1) + ")"
                print "Also, were any solutions found? (" + str(len(availableMoves)) + ")"
                if col == self.tableSize -1 and len(availableMoves):
                    print "We are!"
                    #Clear queue
                    self.queue = []
                    #Get the solution (or one of them, we only care about the first one)
                    s = availableMoves[0]
                    break;
                #Add the possible moves to the new queue
                #This a table containing all queens now placed
                if(len(availableMoves)):
                    print "Adding moves to queue"
                    queue2 += availableMoves
            #Replace the old queue with the new one
            print "Replacing the old queue with the new one"
            self.queue = queue2
            #Increase Queen/col counter
            print "Increasing column"
            col += 1
        self.finish(s, col)
    
    #Get an array of moves that are available, given info about the current table, and the current column
    def getPositions(self, table, col):        
        #Create a row counter, and array to contain our position info
        row = 0
        possiblePositions = []
        
        #Loop all rows on the board
        while row < self.tableSize:
            #If we can place in this space
            if self.canPlace(table, row, col):
                #Add the table with the newly added queen to the list of possible moves
                possiblePositions.append(self.placeQueen(table, row, col))
            row += 1
        return possiblePositions
    
    #Check whether or not we can place a queen in a position, given the table and the row and col of the desired position
    #Return True if space is available
    def canPlace(self, table, row, col):
        print "Looking to see if it is possible to place a queen in " + self.alphabet[row] + str(col+1)
        # - Direction
        # Check left/right
        x = 0
        #Loop across the table
        while x < self.tableSize:
            if table[x][col]:
                return False
            x += 1
        
        # | Direction
        #Check up/down
        y = 0
        #Loop down the table
        while y < self.tableSize:
            if table[row][y]:
                return False
            y += 1
        
        
        # / Direction
        #Check up right Diagonal
        #We can start in the cell 1 up and 1 right of the cell in question, as we have already checked the actual cell in the above 2 checks
        x = row + 1
        y = col + 1
        #Loop up/right through the table
        while x < self.tableSize and y < self.tableSize:
            if table[x][y]:
                return False            
            x += 1
            y += 1
        #Check down left Diagonal
        #Again, not starting in the cell specified
        x = row - 1
        y = col - 1
        #Loop down/left through the table
        while x >= 0 and y >= 0:
            if table[x][y]:
                return False
            x -= 1
            y -= 1
        
        # \ Direction
        #Check up left diagonal
        #Again, not starting in the cell specified
        x = row - 1
        y = col + 1
        #Loop up left through the table
        while x >= 0 and y < self.tableSize:
            if table[x][y]:
                return False
            x -= 1
            y += 1
        #Check down right diagonal
        #Again, not starting in the cell specified
        x = row + 1
        y = col - 1
        #Loop down right through the table
        while x < self.tableSize and y >= 0:
            if table[x][y]:
                return False
            x += 1
            y -= 1
            
        return True
    
    #Output a table to a user, looking all pretty
    def display(self, table):
        #Max Number Length, so we can indent our table nicely later
        mnl = len(str(len(table)))
        
        #New Line
        print ""
        
        #Top of the table, E.g "     A B C D"
        print " "*mnl, "  ",
        for x in range(self.tableSize):
            print self.alphabet[x],
        #New Line
        print ""
        #Row spacer, E.g "   * - - - - *
        print " " * mnl, " *",
        for x in range(self.tableSize):
            print "-",
        print "*"
        
        #Row Counter
        #Print the actual table, with the Queens as 1's, empty space as 0
        #Also prefixed by the row number, E.g " 3 | 0 1 0 0 |
        x = 1
        for row in table:
            #If numbers are shorter than the largest number, give them extra spaces so the rows still line up
            extraPadding = mnl - len(str(x))
            #Show the number prefix, spaces, and | symbol, E.g " 6  | "
            print "", x, " "*int(extraPadding) + "|",
            #Show the value of the cell (1 or 0)
            for col in row:
                print col,
            #End of the row
            print "|"
            #Next Row
            x += 1
        #Show the same row spacer as at the top of the table, E.g "   * - - - - *
        print " " * mnl, " *",
        for x in range(self.tableSize):
            print "-",
        print "*"
    
    #We're done! Show output to the user
    def finish(self, table, col):
        #If we found the right number of queens
        if col == self.tableSize:
            print ""
            print "Total of", self.tableSize, "Queens placed!"
            print "Solution:"
            self.display(table)
        else:
            print ""
            print "ERROR: Could not place all queens for some unknown reason =["
    
    #Run the script
    def run(self):
        if not self.canRun:
            print "ERROR: Can not run"
        else:
            print ""
            print "Working..."
            print ""
            
            #Setup Pretty Print
            self.pp = pprint.PrettyPrinter(indent=4, width=30)
            
            table = self.blankTable()
            #This is created when the object was initialised. Just mention it here.
            print "Initialising with empty list"
            self.queue = self.getPositions(table, 0)
            self.loopBoard()

#Ask the user how many Queens they want to use
def ask():
    while True:
        print ""
        print "How many Queens would you like use?  [8]"
        input = raw_input()
        #Check if the input given is an integer
        if input.isdigit():
            return int(input)
        #If no input is given, use the standard 8
        elif input == "":
            return 8;
        print "ERROR: Invalid Input"

#Run the program
def run():
    #Instanciate the solver
    qs = QueenSolver()
    #While ask hasn't given a valid input
    while(not qs.canRun):
        qs.setup(ask())
    print ""
    #GO!
    qs.run()

#Prompt the user if they want to run the program again
def prompt():
    #Has valid input been received?
    while True:
        print ""
        print "Would you like to run the script again? Please enter Y/N  [N]"
        input = raw_input()
        #Check if the input given is Y or N
        if input == "Y" or input == "y":
            return True
        #Also accept an empty string in place of N
        elif input == "N" or input == "n" or input == "":
            return False
        print "ERROR: Invalid Input"
    
if __name__ == "__main__":
    print ""
    print ""
    print "  #######################################"
    print "  ## Breadth First Search Queen Solver ##"
    print "  ## By: Michael Fiford - COMF3        ##"
    print "  ## Date: 03/12/2013                  ##"
    print "  #######################################"

    #Run the script, and prompt them after if they want to run it again
    shouldRun = True
    while(shouldRun):
        run()
        shouldRun = prompt()