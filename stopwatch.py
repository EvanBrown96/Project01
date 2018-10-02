import time

class Stopwatch:

    """
    Simple stopwatch class
    """

    # Constructor
    def __init__(self):
      # @var start_time : time stopwatch started
      self.start_time = 0;
      # @var end_time : time stopwatch ended
      self.end_time = 0;

    # Starts stopwatch
    def start(self):
      self.start_time = round(time.time())

    # Starts stopwatch
    def stop(self):
        self.end_time = round(time.time() - self.start_time)

    # Gets current time on stopwatch
    def currentTime(self):
        # account for stopwatch not being started yet
        # don't want to return current time UTC
        if self.start_time == 0:
            return 0
        else:
            return round(time.time() - self.start_time)
