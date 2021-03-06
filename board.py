## @file board.py
#  Source file for the board object
#
#  Project: Minesweeper
#  Author: Clare Meyer
#  Created: 09/06/18

from random import randint
from square import Square
import tkinter as Tk



class Board:

    """
    Board class that handles game board creation and functionality

    Attributes:
        width: Integer for width of the board

        height: Integer for height of the board

        mines_num: Integer for recording number of mines

        num_flags: Integer for recording number of flags

        grid: 2D array to store Square instances that make up board

        first_selection: Boolean for recording whether or not an interaction is
                         the user's first interaction

        board_window: tk toplevel window instance for board

    """

    ## Constructor
    #  @author: Clare
    def __init__(self, root, hide_callback):
        """
        constructor for board class

        Args:

            root: root tk widget instance

            hide_callback: function to call in order to hide all windows
            and return to setup window

        """
        self.width = 0
        self.height = 0
        self.mines_num = 0
        self.num_flags = Tk.IntVar(0)
        self.grid = [0][0]
        self.first_selection = True

        # create and center board window
        self.board_window = Tk.Toplevel(root)

        # configure window
        self.board_window.title("Minesweeper 2018")
        self.board_window.resizable(width=False, height=False)
        self.board_window.protocol("WM_DELETE_WINDOW", hide_callback)

        # initially hide window
        self.board_window.withdraw()



    def gridSquares(self):
        """
        place all the squares into the board window
        """

        # set size of board window to needed size based on width & height
        self.board_window.geometry("{}x{}".format(40*self.width, 40*self.height))

        # add squares to grid
        for i in range(self.width):
            for j in range(self.height):
                self.grid[i][j].grid(row=j, column=i, sticky="nesw")

        # set size of columns
        for i in range(self.width):
            self.board_window.grid_columnconfigure(i, minsize=40)

        # set size of rows
        for i in range(self.height):
            self.board_window.grid_rowconfigure(i, minsize=40)



    def ungridSquares(self):
        """
        remove all the squares from the board window
        """
        for i in range(self.width):
            for j in range(self.height):
                self.grid[i][j].destroy()



    ## Generates a grid object
    #  @author: Clare
    #  @param: size, size of the grid
    #  @returns: grid
    def make_grid(self, width, height, reveal_callback, flag_callback):
        """
        Populates grid to user specification

        Args:
            width: Integer for width of board

            height: Integer for height of board

            reveal_callback: function to call when a square is revealed

            flag_callback: function to call when a square is flagged

        Returns:
            grid: Populated 2D array to act as game board

        """
        width = int(width)
        height = int(height)
        grid = [[0 for y in range(height)] for x in range(width)]
        for i in range(0, width):
            for j in range(0, height):
                grid[i][j] = Square(self.board_window, i, j, reveal_callback, flag_callback)
        return grid

    ## Randomly places mines on board
    #  @author: Ayah
    #  @pre: a grid has been generated
    #  @param: num_mines, user-selected number of mines
    #  @param: size, size of the grid
    #  @param: grid, grid to be populated
    #  @post: the grid is populated with mines
    def generate_mines(self, mines, width, height):
        """
        Randomly places mines on board

        Args:
            mines: Integer number of mines to be used

            width: Integer for width of board

            height: Integer for height of board

        """
        self.mines_num = mines;
        self.width = width;
        self.height = height;
        for i in range(0, self.mines_num):
            is_bomb = False
            while not is_bomb:
                a = randint(0, self.width - 1)
                b = randint(0, self.height - 1)
                if not self.grid[a][b].is_mine:
                    self.grid[a][b].is_mine = True
                    is_bomb = True

    ## Prints a formatted game board
    #  @author: Clare
    #  @pre: grid does not have formatting
    #  @param: size, size of the grid
    #  @param: main_grid, grid to be printed
    #  @post: grid is printed to look nice for the user
    def print_board(self, width, height, main_grid):
        """
        Prints a formatted game board, followed by making a call to print a
        formatted time from stopwatch

        Args:

            width: Integer for width of board

            height: Integer for height of board

            main_grid: 2D array to be printed

        """

        width = int(width)
        height = int(height)

        grid = [[0 for x in range(height + 2)] for y in range(width + 2)]

        for i in range(0, height+2):
            for j in range(0, width+2):
                if(i == 0 and j == 0 or i == 0 and j == 1 or i == 1 and j == 0
                or i == 1 and j == 1):
                    grid[j][i] = " "
                elif j == 0:
                    grid[j][i] = i-2
                elif i == 0:
                    grid[j][i] = j-2
                elif j == 1:
                    grid[j][i] = "|"
                elif i == 1:
                    grid[j][i] = "--"
                else:
                    grid[j][i] = main_grid[j - 2][i - 2]

        for i in range(0, height+2):
            for j in range(0, width+2):
                if i == 0 or i == 1 or j == 0 or j == 1:
                    if i == 1 and j == 0:
                        print(grid[j][i], end=' ')
                    elif i == 0 and j == 0 or i == 0 and j == 1 or i == 1 and j == 1:
                        print((str(grid[j][i]).ljust(2)), end=' ')
                    elif i == 0 or j == 0:
                        print((str(grid[j][i]).zfill(2)), end=' ')
                    else:
                        print(str(grid[j][i]).ljust(2), end=' ')
                else:
                    grid[j][i].print_square()
            print('\n', end=' ')
        self.printCurrentTime()

    ## Counts number of adjacent mines for a given cell
    #  @authors: Kyle, Kristi
    #  @param x, x-coordinate of cell
    #  @param y, y-coordinate of cell
    #  @param: size, size of the grid
    #  @param: grid, grid to be checked
    def count_nearby_mines(self, x, y, width, height):
        """
        Counts the number of adjacent mines for a given Square

        Args:
            x: Integer coordinate of Square on the x-axis

            y: Integer coordinate of Square on the y-axis

            width: Integer for width of board

            height: Integer for height of board
        """
        if self.grid[x][y].is_mine:
            return

        for i in range(-1, 2):
            if x+i >= 0 and x+i < width:
                for j in range(-1, 2):
                    if y+j >= 0 and y+j < height:
                        if self.grid[x+i][y+j].is_mine:
                            self.grid[x][y].num_adj_mines += 1



    def checkAdditionalReveals(self):
        """
        Ensures Squares that were already revealed but were changed to 0 after
        the mines moved are revealed properly
        """
        for i in range(self.width):
            for j in range(self.height):

                if self.grid[i][j].is_revealed:
                    self.reveal(i, j)



    # Simple loop to reset num_adj_mines to 0 before being evaluated again
    def resetGridMineCount(self):
        """
        Resets number of adjacent mines to 0 before evaluating the board
        """
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.grid[x][y].num_adj_mines = 0;
                self.grid[x][y].was_moved = False;



    ## Counts/labels number of adjacent mines for board
    #  @author: Kyle
    #  @param: size, size of the grid
    #  @param: grid, grid to be checked
    #  @post: each square is labeled with num_adj_mines
    def mine_check(self, width, height):
        """
        Assigns number of adjacent mines for each Square to the Square member
        variable

        Args:

            width: Integer width of the board

            height: Integer height of the board
        """
        for x in range(width):
            for y in range(height):
                #grid[x][y].num_adj_mines = 0;
                #oldCount = grid[x][y].num_adj_mines
                self.count_nearby_mines(x, y, width, height)



    ## Recursively calls reveal_adjacent() to uncover squares
    #  @authors: Ethan, Kristi
    #  @param x, x-coordinate of cell
    #  @param y, y-coordinate of cell
    def reveal(self, x, y):
        """
        Recursively calls reveal_adajenct to reveal Squares

        Args:

            x: Integer coordinate on the x-axis

            y: Integer coordinate on the y-axis
        """
        self.grid[x][y].reveal()
        if self.grid[x][y].num_adj_mines == 0:
            self.reveal_adjacent(x - 1, y - 1)
            self.reveal_adjacent(x - 1, y)
            self.reveal_adjacent(x - 1, y + 1)
            self.reveal_adjacent(x + 1, y)
            self.reveal_adjacent(x, y - 1)
            self.reveal_adjacent(x, y + 1)
            self.reveal_adjacent(x + 1, y - 1)
            self.reveal_adjacent(x + 1, y + 1)



    ## Reveals cells that aren't mines; Called by reveal()
    #  @authors: Ethan, Kristi
    #  @param x, x-coordinate of cell
    #  @param y, y-coordinate of cell
    def reveal_adjacent(self, x, y):
        """
        Reveals cells that aren't mines

        Args:

            x: Integer coordinate on the x-axis

            y: Integer coordinate on the y-axis
        """
        if not self.is_valid_cell(x, y):
            return
        if self.grid[x][y].is_revealed or self.grid[x][y].is_flagged:
            return
        if self.grid[x][y].num_adj_mines == 0:
            self.grid[x][y].reveal()
            self.reveal(x, y)
        else:
            if not self.grid[x][y].is_mine:
                self.grid[x][y].reveal()
            return



    ## Checks that coordinates are within bounds of board
    #  @author: Kristi
    #  @param x, x-coordinate of cell
    #  @param y, y-coordinate of cell
    def is_valid_cell(self, x, y):
        """
        Checks that coordinates are within bounds of the board

        Args:

            x: Integer coordinate on the x-axis

            y: Integer coordinate on the y-axis
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False



    # ##Trys to move the mine several times verse just once, set the tolerance to increase the probability of a successful moved
    # #default tolerance set to 10
    def validTransformation(self, tolerance, x, y):
        """
        Determines if moved mines are moved properly

        Args:

            tolerance: Integer weight for propability of successful move

            x: Integer coordinate on the x-axis

            y: Integer coordinate on the y-axis

        Returns:

            True if valid transformation
        """
        if not tolerance == 0:
            i = randint(0, self.width - 1)
            j = randint(0, self.height - 1)
            if not self.grid[i][j].is_mine and not self.grid[i][j].is_flagged and self.is_valid_cell(i, j) and not self.grid[i][j].is_revealed:
                self.grid[x][y].is_mine = False
                self.grid[i][j].is_mine = True
                self.grid[i][j].was_moved = True;
            else:
                self.validTransformation(tolerance-1, x, y)



    ##Iterates through each cell of the 2D array and determines if there is a mine
    #If there is a mine the mine is removed and placed somewhere else not revealed or a mine
    def moveMines(self):
        """
        Moves mines to a location that is not revealed nor is a mine
        """
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.grid[i][j].is_mine and not self.grid[i][j].is_flagged and not self.grid[i][j].was_moved:
                    self.validTransformation(10, i, j)



    def hide_board_window(self):
        """
        performs actions to properly hide the board window
        """

        # remove all squares from window
        self.ungridSquares()
        # update window so squares will disappear before window does
        #   otherwise, squares will appear for a second when window pops up again
        self.board_window.update()
        # hide window
        self.board_window.withdraw()
