import time

class Stopwatch:

    """
    Simple stopwatch class
    """

    # Constructor
    def __init__(self):
      # @var start_time : time stopwatch started
      self.start_time = None;
      # @var end_time : time stopwatch ended
      self.end_time = None;

    # Starts stopwatch
    def start(self):
      self.start_time = time.time()

    # Starts stopwatch
    def stop(self):
        self.end_time = time.time() - self.start_time
