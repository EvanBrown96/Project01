# @file executive.py
#  Source file for the UI class
#
#  Project: Minesweeper
#  Author: Ethan Lefert
#  Created: 09/08/18

from random import randint
from board import Board
import tkinter as Tk
from stopwatch import Stopwatch
from tkinter import messagebox
from window_functions import center_window, position_window



# @class Executive
#  @brief Handles user input and gameplay
class Executive:
    """
    Executive class to act as game manager

    Attributes:

        game_over: Boolean to record current game status

        cheat_mode: Boolean to record whether or not user is in cheat mode

        myBoard: Instance of the Board class

        root: tk root widget instance

        setup_callback: function to call to re-show setup window

        stopwatch: instance of stopwatch

        flag_img: tk photoimage instance for the flag

        cheat_button: button to click in order to cheat

    """

    # Constructor; initializes class variables
    #  @author: Ethan
    def __init__(self, root, setup_callback):
        """
        Constructor for Executive class

        Initializes all attributes
        """

        self.root = root
        self.setup_callback = setup_callback

        self.game_over = False
        self.cheat_mode = False
        self.myBoard = Board(root, self.hide_windows)
        self.cheat_board = Board(root, self.exit_cheat)
        self.cheat_board.board_window.title("Cheating...")
        self.cheat_board.board_window.bind("<Escape>", lambda _: self.exit_cheat())
        self.stopwatch = Stopwatch(root)

        # create game status window
        self.game_status = Tk.Toplevel(root)
        self.game_status.geometry("100x260")
        #center_window(self.setup_window)
        # initially hide the window
        self.game_status.withdraw()

        bg = "MediumOrchid1"

        # configure window title and color
        self.game_status.title("Game Status")
        self.game_status.configure(bg=bg, bd=10, relief="ridge", pady=24)
        self.game_status.resizable(width=False, height=False)

        # assign callback for window close
        self.game_status.protocol("WM_DELETE_WINDOW", self.hide_windows)

        # create flag counter
        self.flag_img = Tk.PhotoImage(file="./flag.gif")
        flags_counter = Tk.Label(self.game_status, textvariable=self.myBoard.num_flags, image=self.flag_img, compound=Tk.TOP, bg=bg, font=("Futura", 24))
        flags_counter.pack()

        # create timer text
        time_text = Tk.Label(self.game_status, text="\nTime:", bg=bg)
        time_text.pack()
        timer = Tk.Label(self.game_status, textvariable=self.stopwatch.formatted_time, bg=bg)
        timer.pack()
        # add extra space after timer
        Tk.Label(self.game_status, text="\n", bg=bg).pack()

        # create cheat mode button
        self.cheat_button = Tk.Button(self.game_status, text="Cheat!", command=self.cheat, highlightbackground=bg)
        self.cheat_button.pack()



    # Checks if all mines are flagged
    #  @author: Ethan
    #  @post: game_over flag has been updated
    def check_win(self):
        """
        Checks if all mines are flagged to determine is user has won the game

        Calls on_game_win function if the user has won

        """
        flag_on_mine = 0
        for i in range(0, self.width):
            for x in range(0, self.height):
                if self.myBoard.grid[i][x].is_mine and \
                   self.myBoard.grid[i][x].is_flagged:
                    flag_on_mine += 1

        if flag_on_mine == self.mines_num:
            self.on_game_win()



    # Generates board with user input for mines and size
    #  @author: Ethan
    #  @post: Board is generated based on user input
    def setup(self, width, height, mines):
        """
        Generates board to spec of user input

        Then shows board window and game status window

        Args:

            width: width of the board to setup

            height: height of the board to setup

            mines: number of mines in the board to setup
        """

        self.width = width
        self.height = height
        self.mines_num = mines

        # set the initial number of flags
        self.myBoard.num_flags.set(self.mines_num)

        # create board grid
        self.myBoard.grid = self.myBoard.make_grid(self.width, self.height, self.reveal_event, self.flag_event)

        # generate mines on the board grid
        self.myBoard.generate_mines(self.mines_num, self.width, self.height)

        # populate cells with number of adjacent mines
        self.myBoard.mine_check(self.width, self.height)

        # display squares on board window
        self.myBoard.gridSquares()

        # display board window
        center_window(self.myBoard.board_window)
        self.myBoard.board_window.deiconify()

        # display game status window
        position_window(self.game_status, self.myBoard.board_window.winfo_x()-100, self.myBoard.board_window.winfo_y())
        self.game_status.deiconify()

        # reset the stopwatch
        self.stopwatch.reset()

        # signal that the board has not yet had a selection
        self.myBoard.first_selection = True



    def reveal_event(self, x, y):
        """
        Performs necessary actions when a cell is clicked on

        Args:

            x: x-position of the cell clicked

            y: y-position of the cell clicked

        """

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
                self.stopwatch.start()
            self.myBoard.reveal(x, y)
            self.myBoard.moveMines()
            self.myBoard.resetGridMineCount()
            self.myBoard.mine_check(self.width, self.height)
            self.myBoard.checkAdditionalReveals()



    def flag_event(self, x, y):
        """
        Performs necessary actions when a cell is flagged/unflagged (right clicked)

        Args:

            x: x-position of the cell flagged

            y: y-position of the cell flagged

        """

        choice = "f"
        if(self.myBoard.grid[x][y].is_flagged):
            choice = "n"

        if not self.myBoard.grid[x][y].is_flagged and choice == "n":
            pass #print("Invalid try again")
        elif not self.myBoard.grid[x][y].is_flagged \
             and self.myBoard.num_flags.get() == 0 and choice == "f":
            pass #print("Out of flags. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "f":
            pass #print("Space is already flagged. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "f":
            pass #print("You can't flag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_revealed and choice == "n":
            pass #print("You can't unflag a revealed space. Try again.")
        elif self.myBoard.grid[x][y].is_flagged and choice == "n":
            self.myBoard.grid[x][y].unflag()
            self.myBoard.num_flags.set(self.myBoard.num_flags.get()+1)
        elif not self.myBoard.grid[x][y].is_flagged and choice == "f":
            # checking if first selection for stopwatch
            if self.myBoard.first_selection:
                # is first selection, toggle and start stopwatch
                self.myBoard.first_selection = False
                self.stopwatch.start()
            self.myBoard.grid[x][y].flag()
            self.myBoard.num_flags.set(self.myBoard.num_flags.get() - 1)
            self.check_win()



    def on_game_lose(self):
        """
        Run when user clicks on a mine
        """

        # stop stopwatch
        self.stopwatch.stop()

        # reveal all of the mines and freeze all cells to prevent further clicks
        for i in range(self.width):
            for j in range(self.height):
                if self.myBoard.grid[i][j].is_mine:
                    self.myBoard.grid[i][j].reveal()

                self.myBoard.grid[i][j].freeze()

        messagebox.showerror("YOU LOSE", "Too bad.")
        self.hide_windows()



    def on_game_win(self):
        """
        Run when user has flagged all mines
        """

        # stop stopwatch
        self.stopwatch.stop()

        # display and freeze all cells
        for i in range(self.width):
            for j in range(self.height):
                self.myBoard.grid[i][j].reveal()
                self.myBoard.grid[i][j].freeze()

        messagebox.showerror("YOU WIN!", "Congratulations!\n\nYour time was " \
                             + self.stopwatch.formatted_time.get())
        self.hide_windows()



    def cheat(self):
        """
        Run when user enters cheat mode
        """

        # create new board and make a grid for it
        self.cheat_board.grid = self.cheat_board.make_grid(self.width, self.height, None, None)
        self.cheat_board.width = self.width;
        self.cheat_board.height = self.height;

        # copy mine status and adjacent mine count from original board
        for i in range(self.width):
            for j in range(self.height):
                self.cheat_board.grid[i][j].is_mine = self.myBoard.grid[i][j].is_mine
                self.cheat_board.grid[i][j].num_adj_mines = self.myBoard.grid[i][j].num_adj_mines

        # display squares on board window
        self.cheat_board.gridSquares()

        # reveal and freeze all squares
        for i in range(self.width):
            for j in range(self.height):
                self.cheat_board.grid[i][j].reveal()
                self.cheat_board.grid[i][j].freeze()

        # hide main board window
        self.myBoard.board_window.withdraw()
        # show cheat window
        position_window(self.cheat_board.board_window, self.myBoard.board_window.winfo_x(), self.myBoard.board_window.winfo_y())
        self.cheat_board.board_window.deiconify()

        # set cheat mode flag
        self.cheat_mode = True
        self.cheat_button.configure(text="Back", command=self.exit_cheat)



    def exit_cheat(self):
        """
        function to call to hide the cheat board and reset cheat flag
        """
        # hide cheat window
        self.cheat_board.hide_board_window()
        # display original board window
        self.myBoard.board_window.deiconify()

        # set cheat mode flag
        self.cheat_mode = False
        self.cheat_button.configure(text="Cheat!", command=self.cheat)



    def hide_windows(self):
        """
        hides windows and stops processes associated with them
        """

        # stop stopwatch (it may have already been stopped, but not in all cases)
        self.stopwatch.stop()
        # hide board window
        self.myBoard.hide_board_window()
        # hide cheat window (if it is displayed)
        self.cheat_board.hide_board_window()
        self.cheat_mode = False
        self.cheat_button.configure(text="Cheat!", command=self.cheat)
        # hide game status window
        self.game_status.withdraw()
        # re-show setup window
        self.setup_callback()
