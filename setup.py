import tkinter as Tk
from tkinter import messagebox
from executive import Executive
from window_functions import center_window



class Setup:
    """
    Creates and provides functions for window to take in board specifications
    from user.

    Attributes:

        exec: instance of executive class, for actually playing the game with

        root: instance of tk root window

        menu_callback: function to call when the setup window is closed, to re-show
        the main menu window

        setup_window: instance of tk window for input of board parameters

        width_input: tk entry for user to put width value in

        height_input: tk entry for user to put height value in

        mines_input: tk entry for suer to put mines count in

    """



    def __init__(self, root, menu_callback):

        """
        constructor for setup class

        creates tkinter widgets for setup window

        Args:

            root: instance of tk root window

            menu_callback: function to call when the setup window is closed, to re-show
            the main menu window

        """

        def setup_callback():
            """
            callback to pass in to executive for calling to re-show setup window after game end
            """
            self.setup_window.deiconify()

        # creates executive instance
        self.root = root
        self.exec = Executive(root, setup_callback)
        self.menu_callback = menu_callback

        # creates setup window and centers it
        self.setup_window = Tk.Toplevel(root)
        self.setup_window.geometry("200x200")
        center_window(self.setup_window)

        bg = "indianred2"

        # configures setup window title and title
        self.setup_window.title("Setup Board")
        self.setup_window.configure(bg=bg, bd=10, relief="ridge", pady=32)
        self.setup_window.resizable(width=False, height=False)

        # create function to call in order to move back to main menu
        def return_to_menu():
            self.setup_window.destroy()
            self.menu_callback()

        # define window close, escape and return key bindings
        self.setup_window.protocol("WM_DELETE_WINDOW", return_to_menu)
        self.setup_window.bind("<Escape>", lambda _: return_to_menu())
        self.setup_window.bind("<Return>", lambda _: self.validate())

        # create width text & entry
        width_text = Tk.Label(self.setup_window, text="Width", bg=bg)
        self.width_input = Tk.Entry(self.setup_window, width=12, highlightbackground=bg) #, textvariable=self.width_val)

        width_text.grid(row=0, column=0, sticky=Tk.E)
        self.width_input.grid(row=0, column=1)

        # create height text & entry
        height_text = Tk.Label(self.setup_window, text="Height", bg=bg)
        self.height_input = Tk.Entry(self.setup_window, width=12, highlightbackground=bg) #, textvariable=self.height_val)

        height_text.grid(row=1, column=0, sticky=Tk.E)
        self.height_input.grid(row=1, column=1)

        # create mines text & entry
        mines_text = Tk.Label(self.setup_window, text="Mines", bg=bg)
        self.mines_input = Tk.Entry(self.setup_window, width=12, highlightbackground=bg) #, textvariable=self.mines_val)

        mines_text.grid(row=2, column=0, sticky=Tk.E)
        self.mines_input.grid(row=2, column=1)

        # button that starts the game, or displays an error if the dimensions are invalid
        begin = Tk.Button(self.setup_window, text="Begin Game", command=self.validate, highlightbackground=bg)
        begin.grid(row=3, column=0, columnspan=2)



    def validate(self):
        """
        checks if the user's inputs are valid, and starts the game if they are
        """

        def checknum(val):
            """
            checks if the string entered is a nonnegative number

            Args:

                val: the string to check if is a number

            Returns:

                True if the string is a nonnegative number

            """

            if len(val) == 0:
                return False

            for i in range(len(val)):
                if not val[i].isdigit():
                    return False

            return True

        # get user entry from inputs
        width = self.width_input.get()
        height = self.height_input.get()
        mines = self.mines_input.get()

        # check that all entries are numbers
        if not checknum(width):
            messagebox.showerror("Entry Error", "Board width must be a number!")
        elif not checknum(height):
            messagebox.showerror("Entry Error", "Board height must be a number!")
        elif not checknum(mines):
            messagebox.showerror("Entry Error", "Mine count must be a number!")
        else:

            width = int(width)
            height = int(height)
            mines = int(mines)

            # if they are all numbers, check that they are in bounds
            if width < 2:
                messagebox.showerror("Entry Error", "Too small of a width")
            elif width > 15:
                messagebox.showerror("Entry Error", "Too large of a width")
            elif height < 2:
                messagebox.showerror("Entry Error", "Too small of a height")
            elif height > 15:
                messagebox.showerror("Entry Error", "Too large of a height")
            elif mines >= width * height:
                messagebox.showerror("Entry Error", "Too many mines!")
            elif mines < 1:
                messagebox.showerror("Entry Error", "Too few mines!")
            else:
                # hide setup window and tell executive instance to start game
                self.setup_window.withdraw()
                self.exec.setup(width, height, mines)
