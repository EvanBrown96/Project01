import time
import tkinter as Tk



class Stopwatch:

    """
    Simple stopwatch class with functionality for starting, stopping, and resetting

    Attributes:

        start_time: Integer to record time (0 seconds) that stopwatch was
                    started

        formatted_time: stores a formatted time string of the current time

        root: tkinter root widget - needed for timer periodic callbacks

        last_after: stores last last timer callback, so that it can be cancelled
        when the timer is stopped

    """



    def __init__(self, root):
        """
        Constructor for Stopwatch

        Sets start_time variable to 0, and resets the formatted time

        Args:

            root: tkinter root widget, for callbacks

        """
        self.start_time = 0
        self.formatted_time = Tk.StringVar()

        self.last_after = None
        self.root = root

        self.reset()



    def reset(self):
        """
        resets the formatted time to string of 0s
        """
        self.formatted_time.set("00:00:00")



    def start(self):
        """
        Starts stopwatch by setting the start_time to time.time(),
        rounded to the nearest whole number

        Then makes a periodic callback to update the formatted time in 200 ms
        """
        self.start_time = round(time.time())

        def update():
            """
            updates the formatted time with current time, and makes a new callback
            """
            seconds = 0 if self.start_time == 0 else round(time.time() - self.start_time)
            hours = seconds // 3600
            seconds = seconds % 3600
            minutes = seconds // 60
            seconds = seconds % 60
            cur_time = ""
            if hours < 10:
                cur_time += "0" + str(hours) + ":"
            else:
                cur_time += str(hours) + ":"
            if minutes < 10:
                cur_time += "0" + str(minutes) + ":"
            else:
                cur_time += str(minutes) + ":"
            if seconds < 10:
                cur_time += "0" + str(seconds)
            else:
                cur_time += str(seconds)

            self.formatted_time.set(cur_time)
            self.last_after = self.root.after(200, update)

        update()



    # Starts stopwatch
    def stop(self):
        """
        Stops stopwatch by removing the latest callback
        """
        if self.last_after:
            self.root.after_cancel(self.last_after)
