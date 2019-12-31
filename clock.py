import time


class Clock:
    def __init__(self):
        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.on_time = 0

        self.dtime = 1

    def update(self):
        current_time = time.time()
        self.dtime = current_time - self.last_frame_time
        self.last_frame_time = current_time
        self.on_time = time.time() - self.start_time

    def get_fps(self):
        """ Return the game fps.
        if dtime is 0, return infinity. """
        if self.dtime:
            return 1 / self.dtime
        else:
            return float("inf")
