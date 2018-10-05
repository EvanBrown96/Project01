# @file executive.py
#  Source file for the UI class
#
#  Project: Minesweeper
#  Author: Ethan Lefert
#  Created: 09/08/18

from random import randint
from board import Board
import tkinter as Tk
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
        self.myBoard = Board(root, self.hide_windows)

        self.game_status = Tk.Toplevel(root)
        self.game_status.geometry("100x200")
        #center_window(self.setup_window)

        self.game_status.withdraw()
        # self.game_status.deiconify()

        self.setup_callback = setup_callback

        bg = "MediumOrchid1"

        self.game_status.title("Game Status")
        self.game_status.configure(bg=bg, bd=10, relief="ridge", pady=32)
        self.game_status.resizable(width=False, height=False)
        self.game_status.protocol("WM_DELETE_WINDOW", self.hide_windows)

        self.flag_img = Tk.PhotoImage(file="./flag.gif")
        self.flags_counter = Tk.Label(self.game_status, textvariable=self.myBoard.num_flags, image=self.flag_img, compound=Tk.BOTTOM, bg=bg)
        self.flags_counter.pack()

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
        self.myBoard.num_flags.set(self.mines_num)
        self.myBoard.grid = self.myBoard.make_grid(self.width, self.height, self.reveal_event, self.flag_event)
        self.myBoard.generate_mines(self.mines_num, self.width, self.height)
        self.myBoard.mine_check(self.width, self.height)
        self.myBoard.gridSquares()
        self.myBoard.board_window.deiconify()
        self.game_status.deiconify()


        """
        Requests user input for playing the game as long as the game is not
        over
        Presents revealed board upon game over
        """
        

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
             and self.myBoard.num_flags.get() == 0 and choice == "f":
            print("Out of flags. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "f":
            print("Space is already flagged. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "f":
            print("You can't flag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "n":
            print("You can't unflag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "n":
            self.myBoard.grid[x][y].unflag()
            self.myBoard.num_flags.set(self.myBoard.num_flags.get()+1)
        elif not self.myBoard.grid[x][y].is_flagged and choice == "f":
            # checking if first selection for stopwatch
            if self.myBoard.first_selection:
                # is first selection, toggle and start stopwatch
                self.myBoard.first_selection = False
                self.myBoard.stopwatch.start()
            self.myBoard.grid[x][y].flag()
            self.myBoard.num_flags.set(self.myBoard.num_flags.get() - 1)
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
        self.hide_windows()

    def on_game_win(self):
        for i in range(self.width):
            for j in range(self.height):
                self.myBoard.grid[i][j].reveal()
                self.myBoard.grid[i][j].freeze()

        messagebox.showerror("YOU WIN!", "Congratulations!")
        self.hide_windows()

    def hide_windows(self):
        self.myBoard.hide_board_window()
        self.game_status.withdraw()
        self.setup_callback()
        # for i in range(0, self.width):
        #     for j in range(0, self.height):
        #         self.myBoard.grid[i][j].num_adj_mines = False
        #         self.myBoard.grid[i][j].reveal()
        # self.myBoard.print_board(self.width, self.height, self.myBoard.grid)
