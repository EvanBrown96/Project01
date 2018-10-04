## @file menu.py
#  Source file for the menu object
#
#  Project: Minesweeper
#  Author: Ayah Alkhatib
#  Created: 09/08/18

from setup import Setup
import tkinter as Tk
from window_functions import center_window

## @class Menu
#  @brief Prints menu and rules; Manages Executive instance
class Menu:

    """
    Menu class to act as game menu

    Attributes:

        setup: Instance of the Setup class for getting user input to setup the board

        root: instance of Tk root window

        play_button: tkinter button to play the game

        rules_button: tkinter button to show the rules window

        quit_button: tkinter button to quit the entire process

        rules_window: tkinter window for the rules to display in

        rules_displayed: flag if the rules are currently displayed or not

    """

    ## Constructor; initializes class variables
    #  @author: Ayah
    def __init__(self, root):
        """
        Constructor for Menu class

        Initializes all attributes

        Args:

            root: instance of Tk root window

        """

        ## @var myGame
        #  instance of the executive class
        self.setup = None

        # save root Tk window and set dimensions and centering
        self.root = root
        root.geometry("400x200")
        center_window(self.root)

        # this prevents window from temporarily appearing in its original position
        root.withdraw()
        root.deiconify()

        bg = "lightgreen"

        # configure window
        root.title("Minesweeper 2018")
        root.configure(bg=bg, bd=10, relief="ridge", pady=30)
        root.resizable(width=False, height=False)

        # create welcome text and display it
        Tk.Label(root, text="Welcome to Minesweeper", bg=bg, font=('copperplate', 24)).pack()

        # create buttons
        self.play_button = Tk.Button(root, text="Play", command=self.start_game, highlightbackground=bg)
        self.rules_button = Tk.Button(root, text="Rules", command=self.game_rules, highlightbackground=bg)
        self.quit_button = Tk.Button(root, text="Quit", command=self.root.destroy, highlightbackground=bg)

        # display buttons
        self.play_button.pack()
        self.rules_button.pack()
        self.quit_button.pack()

        # create member variable for rules window, but don't create the actual window yet
        self.rules_window = None
        # flag to prevent rules window from being created multiple times
        self.rules_displayed = False



    def start_game(self):
        """
        Hides main menu window and displays the board setup window
        """

        # hide the menu window, and the rules window if it is open
        self.root.withdraw()
        if self.rules_displayed:
            self.rules_window.withdraw()

        def show_callback():
            # after game finishes (by either loss or win), display the windows again
            self.root.deiconify()
            if self.rules_displayed:
                self.rules_window.deiconify()

        # create board setup window
        self.setup = Setup(self.root, show_callback)



    ## Prints the game instructions
    #  @author: Ayah
    def game_rules(self):
        """
        Prints the game instructions
        """

        if self.rules_displayed:
            # if rules are already displayed, move them to the front and return
            self.rules_window.lift()
            return

        # set displayed flag
        self.rules_displayed = True

        # create a new window
        self.rules_window = Tk.Toplevel(self.root)
        self.rules_window.geometry("550x425")
        center_window(self.rules_window)

        self.rules_window.withdraw()
        self.rules_window.deiconify()

        bg = "khaki"

        # configure window
        self.rules_window.title("Rules")
        self.rules_window.configure(bg=bg, bd=10, relief="ridge")
        self.rules_window.resizable(width=False, height=False)

        def on_rules_close():
            """
            Destroys the rules window sets window flag to false
            """
            self.rules_displayed = False
            self.rules_window.destroy()

        # when window is closed, call function to set flag
        self.rules_window.protocol("WM_DELETE_WINDOW", on_rules_close)
        # also allow escape to close the window
        self.rules_window.bind("<Escape>", lambda _: on_rules_close())

        # create and show rules text
        Tk.Label(self.rules_window, bg=bg, text="----- How to Play -----").pack()
        Tk.Label(self.rules_window, bg=bg, justify=Tk.LEFT, text="""
The game will provide players a tiled board with a number of hidden mines
and an equal number of flags which with to mark the mines.

The player has three choices of action:
- Flag: flag a tile that might have a mine
- Unflag: unflag if you think you made a mistake
- Reveal: show what a tile has hiding underneath

When you choose to reveal:
- If the square has a mine -> Gameover!
- Not a mine -> Display number of adjacent squares that DO have a mine

Goal: place a flag where all of the mines are.

Also, as an added difficulty, some or all of the mines will move
    around every time you select to reveal!

Note: To see your current time, enter 'T' when asked for coordinates;
    you can also enter 'C' to enter cheat mode!

Good Luck!"""
        ).pack()
