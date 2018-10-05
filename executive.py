# @file executive.py
#  Source file for the UI class
#
#  Project: Minesweeper
#  Author: Ethan Lefert
#  Created: 09/08/18

from random import randint
from board import Board
from tkinter import messagebox
# importing copy module for creating deep copies for cheat mode
import copy


# @class Executive
#  @brief Handles user input and gameplay
class Executive:
    """
    Executive class to act as game manager

    Attributes:

        game_over: Boolean to record current game status

        cheat_mode: Boolean to record whether or not user is in cheat mode

        myBoard: Instance of the Board class
    """

    # Constructor; initializes class variables
    #  @author: Ethan
    def __init__(self, root, setup_callback):
        """
        Constructor for Executive class

        Initializes all attributes
        """
        self.root = root
        self.game_over = False
        self.cheat_mode = False
        self.myBoard = Board(root, setup_callback)

    # Checks if all mines are flagged
    #  @author: Ethan
    #  @post: game_over flag has been updated
    def check_win(self):
        """
        Checks if all mines are flagged to determine is user has won the game

        Returns:
            0 if user has not won the game
        """
        flag_on_mine = 0
        for i in range(0, self.width):
            for x in range(0, self.height):
                if self.myBoard.grid[i][x].is_mine and \
                   self.myBoard.grid[i][x].is_flagged:
                    flag_on_mine += 1
        if flag_on_mine == self.mines_num:
            self.on_game_win()
        else:
            return 0

    # Generates board with user input for mines and size
    #  @author: Ethan
    #  @post: Board is generated based on user input
    def setup(self, width, height, mines):
        """
        Generates board to spec of user input
        """

        self.width = width
        self.height = height
        self.mines_num = mines
        self.myBoard.num_flags = self.mines_num
        self.myBoard.grid = self.myBoard.make_grid(self.width, self.height, self.reveal_event, self.flag_event)
        self.myBoard.generate_mines(self.mines_num, self.width, self.height)
        self.myBoard.mine_check(self.width, self.height)
        self.myBoard.gridSquares()
        self.myBoard.board_window.deiconify()

    # Takes coordinates from user and handles input
    #  @pre: Board has been setup
    #  @author: Ethan
    def play(self):
        """
        Requests user input for playing the game as long as the game is not
        over
        Presents revealed board upon game over
        """
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
                leave_cheat_mode = input('Enter any input to leave cheat \
mode...')
                # leave cheat mode
                self.cheat_mode = False
                print('Leaving cheat mode...')
            else:
                # Printing board and number of flags
                self.myBoard.print_board(self.width, self.height,
                                         self.myBoard.grid)
                print("Number of flags: %s" % self.myBoard.num_flags)
                # not in cheat mode
                # get x coordinate
                while True:
                    x = input("Enter a X coordinate: ")
                    # account for cheat input
                    if x == 'c' or x == 'C':
                        self.cheat_mode = True
                        break
                    # user requested to see current time on stopwatch
                    elif x == 't' or x == 'T':
                        self.myBoard.printCurrentTime()
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
                if self.cheat_mode is True:
                    # is applied, continue to next iteration of loop
                    continue

                # get x coordinate
                while True:
                    y = input("Enter a Y coordinate: ")
                    # account for cheat input
                    if y == 'c' or y == 'C':
                        self.cheat_mode = True
                        break
                    # user requested to see current time on stopwatch
                    elif y == 't' or y == 'T':
                        self.myBoard.printCurrentTime()
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
                if self.cheat_mode is True:
                    # is applied, continue to next iteration of loop
                    continue

                # cheat code not applied
                # ask user for action with selected coordinates
                choice = input("Enter an action flag [f], reveal [r], \
unflag [n]: ")

    def reveal_event(self, x, y):
        if self.myBoard.grid[x][y].is_revealed and not \
            self.myBoard.grid[x][y].is_mine:
            pass
        elif self.myBoard.grid[x][y].is_flagged:
            pass
        elif self.myBoard.grid[x][y].is_mine:
            self.on_game_lose()
        else:
            # checking if first selection for stopwatch
            if self.myBoard.first_selection:
                # is first selection, toggle and start stopwatch
                self.myBoard.first_selection = False
                self.myBoard.stopwatch.start()
            self.myBoard.reveal(x, y)
            self.myBoard.moveMines()
            self.myBoard.resetGridMineCount()
            self.myBoard.mine_check(self.width, self.height)
            self.myBoard.checkAdditionalReveals()

    def flag_event(self, x, y):
        choice = "f"
        if(self.myBoard.grid[x][y].is_flagged):
            choice = "n"

        if not self.myBoard.grid[x][y].is_flagged and choice == "n":
            print("Invalid try again")
        elif not self.myBoard.grid[x][y].is_flagged \
             and self.myBoard.num_flags == 0 and choice == "f":
            print("Out of flags. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "f":
            print("Space is already flagged. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "f":
            print("You can't flag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "n":
            print("You can't unflag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "n":
            self.myBoard.grid[x][y].unflag()
            self.myBoard.num_flags += 1
        elif not self.myBoard.grid[x][y].is_flagged and choice == "f":
            # checking if first selection for stopwatch
            if self.myBoard.first_selection:
                # is first selection, toggle and start stopwatch
                self.myBoard.first_selection = False
                self.myBoard.stopwatch.start()
            self.myBoard.grid[x][y].flag()
            self.myBoard.num_flags -= 1
            self.check_win()

    def on_game_lose(self):
        #print("aaa")
        #self.stopwatch.stop()
        for i in range(self.width):
            for j in range(self.height):
                if self.myBoard.grid[i][j].is_mine:
                    self.myBoard.grid[i][j].reveal()

                self.myBoard.grid[i][j].freeze()

        messagebox.showerror("YOU LOSE", "Stupid Loser haha")
        self.myBoard.return_to_setup()

    def on_game_win(self):
        for i in range(self.width):
            for j in range(self.height):
                self.myBoard.grid[i][j].reveal()
                self.myBoard.grid[i][j].freeze()

        messagebox.showerror("YOU WIN!", "Congratulations!")
        self.myBoard.return_to_setup()

        # for i in range(0, self.width):
        #     for j in range(0, self.height):
        #         self.myBoard.grid[i][j].num_adj_mines = False
        #         self.myBoard.grid[i][j].reveal()
        # self.myBoard.print_board(self.width, self.height, self.myBoard.grid)
