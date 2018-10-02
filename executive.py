## @file executive.py
#  Source file for the UI class
#
#  Project: Minesweeper
#  Author: Ethan Lefert
#  Created: 09/08/18

from random import randint
from board import Board
# importing copy module for creating deep copies for cheat mode
import copy


## @class Executive
#  @brief Handles user input and gameplay
class Executive:

    ## Constructor; initializes class variables
    #  @author: Ethan
    def __init__(self):
        ## @var mines
        #  stores the number of mines
        self.mines = 0
        ## @var num_flags
        #  stores the number of flags
        self.num_flags = 0
        ## @var game_over
        #  flag for game status
        self.game_over = False
        ## @var cheat_mode
        # variable for whether or not user is in cheat mode
        self.cheat_mode = False
        ## @var myBoard
        #  instance of the board class
        self.myBoard = Board()

# ##Trys to move the mine several times verse just once, set the tolerance to increase the probability of a successful moved
# #default tolerance set to 10
    def validTransformation(self, tolerance, i, j):
        if not tolerance == 0:
            a = randint(0, self.width - 1)
            b = randint(0, self.height - 1)
            if not self.myBoard.grid[a][b].is_mine and not self.myBoard.grid[a][b].is_flagged and self.myBoard.is_valid_cell(a, b) and not self.myBoard.grid[a][b].is_revealed:
                self.myBoard.grid[i][j].is_mine = False
                self.myBoard.grid[a][b].is_mine = True
                self.myBoard.grid[a][b].was_moved = True;
                #Uncomment to show transformation of mine position
                #print("Value i,j :" + str(i) + ", " + str(j) + " with was_moved to: " + str(a) + ", " +str(b))
                return True;
            else:
                self.validTransformation(tolerance-1, i, j)

    ##Iterates through each cell of the 2D array and determines if there is a mine
    #If there is a mine the mine is removed and placed somewhere else not revealed or a mine
    def moveMines(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.myBoard.grid[i][j].is_mine and not self.myBoard.grid[i][j].is_flagged and not self.myBoard.grid[i][j].was_moved:
                    if self.validTransformation(10, i, j):
                        self.myBoard.reveal(i, j)

    # ## Recursively calls reveal_adjacent() to uncover squares
    # #  @authors: Ethan, Kristi
    # #  @param x, x-coordinate of cell
    # #  @param y, y-coordinate of cell
    # def reveal(self, x, y):
    #     self.myBoard.grid[x][y].is_revealed = True
    #     if self.myBoard.grid[x][y].num_adj_mines == 0:
    #         self.myBoard.reveal_adjacent(x - 1, y - 1)
    #         self.myBoard.reveal_adjacent(x - 1, y)
    #         self.myBoard.reveal_adjacent(x - 1, y + 1)
    #         self.myBoard.reveal_adjacent(x + 1, y)
    #         self.myBoard.reveal_adjacent(x, y - 1)
    #         self.myBoard.reveal_adjacent(x, y + 1)
    #         self.myBoard.reveal_adjacent(x + 1, y - 1)
    #         self.myBoard.reveal_adjacent(x + 1, y + 1)

    # ## Checks that coordinates are within bounds of board
    # #  @author: Kristi
    # #  @param x, x-coordinate of cell
    # #  @param y, y-coordinate of cell
    # def is_valid_cell(self, x, y):
    #     if 0 <= x < self.width and 0 <= y < self.height:
    #         return True
    #     return False

    # ## Reveals cells that aren't mines; Called by reveal()
    # #  @authors: Ethan, Kristi
    # #  @param x, x-coordinate of cell
    # #  @param y, y-coordinate of cell
    # def reveal_adjacent(self, x, y):
    #     if not self.myBoard.is_valid_cell(x, y):
    #         return
    #     if self.myBoard.grid[x][y].is_revealed or self.myBoard.grid[x][y].is_flagged:
    #         return
    #     if self.myBoard.grid[x][y].num_adj_mines == 0:
    #         self.myBoard.grid[x][y].is_revealed = True
    #         self.myBoard.reveal(x, y)
    #     else:
    #         if not self.myBoard.grid[x][y].is_mine:
    #             self.myBoard.grid[x][y].is_revealed = True
    #         return

    ## Checks if all mines are flagged
    #  @author: Ethan
    #  @post: game_over flag has been updated
    def check_win(self):
        flag_on_mine = 0
        for i in range(0, self.width):
            for x in range(0, self.height):
                if self.myBoard.grid[i][x].is_mine and self.myBoard.grid[i][x].is_flagged:
                    flag_on_mine += 1
        if flag_on_mine == self.mines:
            print("You Win!")
            self.game_over = True
        else:
            return 0

    ## Generates board with user input for mines and size
    #  @author: Ethan
    #  @post: Board is generated based on user input
    def setup(self):

        while True:
            try:
                board_size_select = int(input("Please enter the board width between 2 and 15: "))
            except ValueError:
                print("That\'s not a number!")
            else:
                if 2 <= board_size_select <= 15:
                    self.width = board_size_select
                    break
                else:
                    print('Not a valid board size. Try again')

        while True:
            try:
                board_size_select = int(input("Please enter the board height between 2 and 15: "))
            except ValueError:
                print("That\'s not a number!")
            else:
                if 2 <= board_size_select <= 15:
                    self.height = board_size_select
                    break
                else:
                    print('Not a valid board size. Try again')

        max_mines = self.width * self.height - 1

        while True:
            try:
                mine_num_select = int(
                    input("Enter the number of mines, it should be between 1 and " + str(max_mines) + ": "))
            except ValueError:
                print("That\'s not a number!")
            else:
                if 1 <= mine_num_select <= max_mines:
                    self.mines = mine_num_select
                    break
                else:
                    print('Not a valid amount of mines. Try again')

        self.num_flags = self.mines

        self.myBoard.grid = self.myBoard.make_grid(self.width, self.height)
        self.myBoard.generate_mines(self.mines, self.width, self.height, self.myBoard.grid)
        self.myBoard.mine_check(self.width, self.height, self.myBoard.grid)



    ## Takes coordinates from user and handles input
    #  @pre: Board has been setup
    #  @author: Ethan
    def play(self):
        while not self.game_over:
            # Checking if in cheat mode
            if self.cheat_mode:
                # in cheat mode
                print('Entering cheat mode, revealing entire board...')
                # make duplicate board and reveal all spaces
                cheat_board = copy.deepcopy(self.myBoard.grid)
                for i in range(0, self.width):
                    for j in range(0, self.height):
                        cheat_board[i][j].is_revealed = True
                self.myBoard.print_board(self.width, self.height, cheat_board)
                # present notice on how to leave cheat mode
                leave_cheat_mode = input('Enter any input to leave cheat mode...')
                # leave cheat mode
                self.cheat_mode = False
                print('Leaving cheat mode...')
            else:
                # Printing board and number of flags
                self.myBoard.print_board(self.width, self.height, self.myBoard.grid)
                print("Number of flags: %s" % self.num_flags)
                # not in cheat mode
                # get x coordinate
                while True:
                    x = input("Enter a X coordinate: ")
                    # account for cheat input
                    if x == 'c' or x == 'C':
                        self.cheat_mode = True
                        break
                    # not cheat input, check if numeric
                    elif not x.isnumeric():
                        print("That\'s not an integer. Try again.")
                    # not cheat input, is numeric, check if within range
                    elif int(x) < 0 or int(x) >= self.width:
                        print("Invalid input. Try again.")
                    # good input
                    else:
                        # make x an int
                        x = int(x)
                        break

                # check if cheat applied
                if self.cheat_mode == True:
                    # is applied, continue to next iteration of loop
                    continue

                # get x coordinate
                while True:
                    y = input("Enter a Y coordinate: ")
                    # account for cheat input
                    if y == 'c' or y == 'C':
                        self.cheat_mode = True
                        break
                    # not cheat input, check if numeric
                    elif not y.isnumeric():
                        print("That\'s not an integer. Try again.")
                    # not cheat input, is numeric, check if within range
                    elif int(y) < 0 or int(y) >= self.height:
                        print("Invalid input. Try again.")
                    # good input
                    else:
                        # make y an int
                        y = int(y)
                        break

                # check if cheat applied
                if self.cheat_mode == True:
                    # is applied, continue to next iteration of loop
                    continue

                # cheat code not applied, ask user for action with selected coordinates
                choice = input("Enter an action flag [f], reveal [r], unflag [n]: ")
                if x >= self.width or y >= self.height:
                    print("Invalid try again")
                elif choice != "f" and choice != "n" and choice != "r":
                    print("Invalid choice try again")
                elif not self.myBoard.grid[x][y].is_flagged and choice == "n":
                    print("Invalid try again")
                elif not self.myBoard.grid[x][y].is_flagged and self.num_flags == 0 and choice == "f":
                    print("Out of flags. Try again.")
                elif self.myBoard.grid[x][y].is_flagged and choice == "f":
                    print("Space is already flagged. Try again.")
                elif self.myBoard.grid[x][y].is_revealed and choice == "f":
                    print("You can't flag a revealed space. Try again.")
                elif self.myBoard.grid[x][y].is_revealed and choice == "n":
                    print("You can't unflag a revealed space. Try again.")
                elif self.myBoard.grid[x][y].is_flagged and choice == "n":
                    self.myBoard.grid[x][y].is_flagged = False
                    self.num_flags += 1
                elif not self.myBoard.grid[x][y].is_flagged and choice == "f":
                    self.myBoard.grid[x][y].is_flagged = True
                    self.num_flags -= 1
                    self.check_win()
                #Testing to see if is_revealed is being switched to true
                elif self.myBoard.grid[x][y].is_revealed and not self.myBoard.grid[x][y].is_mine and choice == "r":
                    print("Space is already revealed. Try again.")
                elif self.myBoard.grid[x][y].is_flagged and choice == "r":
                    print("You can't reveal a flagged space. Unflag before guessing this space or guess a different space.")
                elif self.myBoard.grid[x][y].is_mine and choice == "r":
                    print("Game Over")
                    self.game_over = True
                else:
                    self.myBoard.reveal(x, y)
                    self.moveMines()
                    self.myBoard.resetGridMineCount(self.myBoard.grid)
                    self.myBoard.mine_check(self.width, self.height, self.myBoard.grid)




        for i in range(0, self.width):
            for j in range(0, self.height):
                self.myBoard.grid[i][j].is_revealed = True
                self.myBoard.grid[i][j].num_adj_mines = False
        self.myBoard.print_board(self.width, self.height, self.myBoard.grid)
