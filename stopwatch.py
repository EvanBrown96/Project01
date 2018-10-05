import time
import tkinter as Tk


class Stopwatch:

    """
    Simple stopwatch class with functionality for starting, stopping, and
    getting current time on the stopwatch

    Attributes:
        start_time: Integer to record time (0 seconds) that stopwatch was
                    started

        end_time: Integer to record number of seconds since stopwatch started
    """

    # Constructor
    def __init__(self, root):
        """
        Constructor for Stopwatch
        Sets both start_time and end_time member variables to 0
        """
        self.start_time = 0
        self.end_time = 0
        self.formatted_time = Tk.StringVar()
        self.reset()
        self.last_after = None
        self.root = root

    def reset(self):
        self.formatted_time.set("00:00:00")

    # Starts stopwatch
    def start(self):
        """
        Starts stopwatch by setting the start_time to time.time(),
        rounded to the nearest whole number
        """
        self.start_time = round(time.time())

        def update():
            """
            Prints a formatted time from the stopwatch
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
        Stops stopwatch by settingt the end_time equal to
        time.time() - start_time, rounded to the nearest whole number
        """
        self.end_time = round(time.time() - self.start_time)
        if self.last_after:
            self.root.after_cancel(self.last_after)

    # Gets current time on stopwatch
    def currentTime(self):
        """
        Gets current time on stopwatch
        If start_time is 0, returns 0
        Else returns time.time() - start_time rounded to nearest whole number

        Returns:
            Current time on switch as an integer
        """
        # account for stopwatch not being started yet
        # don't want to return current time UTC
        if self.start_time == 0:
            return 0
        else:
            return round(time.time() - self.start_time)


    # Prints current time on stopwatch for user
    def printCurrentTime(self):
        """
        Prints a formatted time from the stopwatch
        """
        seconds = self.stopwatch.currentTime()
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        time = "Time: "
        if hours < 10:
            time += "0" + str(hours) + ":"
        else:
            time += str(hours) + ":"
        if minutes < 10:
            time += "0" + str(minutes) + ":"
        else:
            time += str(minutes) + ":"
        if seconds < 10:
            time += "0" + str(seconds)
        else:
            time += str(seconds)
        print(time)
