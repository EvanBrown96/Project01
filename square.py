# @file square.py
#  Source file for the square object
#
#  Project: Minesweeper
#  Author: Kristi Daigh
#  Created: 09/07/18


# @class Square
#  @brief Defines and manages properties for Square object
class Square:

    """
    Square class for managing properties of a square in Minesweeper

    Attributes:
        is_mine: Boolean to record whether or not a square is a mine

        is_flagged: Boolean to record whether or not a square is flagged

        is_revealed: Boolean to record whether or not a square is revealed

        num_adj_mines: Integer to record number of mines adjacent to square

        was_moved: Boolean to record whether or not a square has been moved
    """

    # Constructor
    #  @author: Kristi
    def __init__(self):
        """
        Constructor for Square class
        Initialized all attributes to false or 0 depending on type of Boolean
        or Integer
        """
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.num_adj_mines = 0
        self.was_moved = False

    # Prints the square based on properties
    #  @author: Kristi
    def print_square(self):
        """
        Prints the square with respect to the current status of the square's
        attributes
        """
        if not self.is_revealed:
            if self.is_flagged:
                print(str("F").ljust(2), end=' ')
            else:
                print(str("#").ljust(2), end=' ')
        else:
            if self.is_mine:
                print(str("*").ljust(2), end=' ')
            elif self.num_adj_mines:
                print(str(self.num_adj_mines).ljust(2), end=' ')
            else:
                print(str(" ").ljust(2), end=' ')
