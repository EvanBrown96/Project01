## @file menu.py
#  Source file for the menu object
#
#  Project: Minesweeper
#  Author: Ayah Alkhatib
#  Created: 09/08/18

from executive import Executive
import tkinter as Tk

## @class Menu
#  @brief Prints menu and rules; Manages Executive instance
class Menu:

    ## Constructor; initializes class variables
    #  @author: Ayah
    def __init__(self, root):

        ## @var myGame
        #  instance of the executive class
        self.myGame = None

        # save root Tk window
        self.root = root

        # create welcome text and display it
        Tk.Label(root, text="Welcome to Minesweeper").pack()

        # create buttons
        self.play_button = Tk.Button(root, text="Play", command=self.start_game)
        self.rules_button = Tk.Button(root, text="Rules", command=self.game_rules)
        self.quit_button = Tk.Button(root, text="Quit", command=self.root.destroy)

        # display buttons
        self.play_button.pack()
        self.rules_button.pack()
        self.quit_button.pack()

        # create member variable for rules window, but don't create the actual window yet
        self.rules_window = None
        # flag to prevent rules window from being created multiple times
        self.rules_displayed = False


    def start_game(self):

        # hide the menu window, and the rules window if it is open
        self.root.withdraw()
        if self.rules_displayed:
            self.rules_window.withdraw()

        # create new game and call methods as normal
        self.myGame = Executive()
        self.myGame.setup()
        self.myGame.play()

        # after game finishes (by either loss or win), display the windows again
        self.root.deiconify()
        if self.rules_displayed:
            self.rules_window.deiconify()



    def on_rules_close(self):
        self.rules_displayed = False
        self.rules_window.destroy()



    ## Prints the game instructions
    #  @author: Ayah
    def game_rules(self):

        if self.rules_displayed:
            # if rules are already displayed, move them to the front and return
            self.rules_window.lift()
            return

        # set displayed flag
        self.rules_displayed = True

        # create a new window
        self.rules_window = Tk.Toplevel(self.root)

        # when window is closed, set
        self.rules_window.protocol("WM_DELETE_WINDOW", self.on_rules_close)

        # create and show rules text
        Tk.Label(self.rules_window, text="""Welcome to Minesweepers!

Here are the game instructions:

The game will provid players a square board with a number of hidden mines and similar number of flags.

Player has three choices of action:

    - Flag: to flag squares that might have mines.

    - Unflag: to unflag if player changed mind.

    - Reveal: to see what squares have underneath.

When player chose to reveal:

    - If the square has a mine -> Gameover!

    - If not a mine, it will show spaces and numbers to tell player the number of mines around the chosen square.

The goal is to flag all mines until the counter of flags equals to zero without revealing any mine.

Note: To enter a secret cheat mode, enter 'C' when asked for coordinates!

Good Luck!

""").pack()
