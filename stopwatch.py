import time


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
    def __init__(self):
        """
        Constructor for Stopwatch
        Sets both start_time and end_time member variables to 0
        """
        self.start_time = 0
        self.end_time = 0

    # Starts stopwatch
    def start(self):
        """
        Starts stopwatch by setting the start_time to time.time(),
        rounded to the nearest whole number
        """
        self.start_time = round(time.time())

    # Starts stopwatch
    def stop(self):
        """
        Stops stopwatch by settingt the end_time equal to
        time.time() - start_time, rounded to the nearest whole number
        """
        self.end_time = round(time.time() - self.start_time)

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
