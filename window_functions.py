def center_window(window):
    """
    centers the given window/widget on the screen

    Args:

        window: the tk window (root/toplevel) instance to center

    """
    window.update_idletasks()
    # get current window width & height
    width = window.winfo_width()
    height = window.winfo_height()
    # calculate centered x and y
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    # resize window
    window.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))

    # this prevents window from temporarily appearing in its original position
    window.withdraw()
    window.deiconify()



def position_window(window, x, y):
    """
    sends the given window to the given x, y position

    Args:

        window: the tk window (root/toplevel) instance to move

        x: pixel x-position to move to

        y: pixel y-position to move to

    """
    window.update_idletasks()

    window.geometry('+{}+{}'.format(x, y))

    window.withdraw()
    window.deiconify()
