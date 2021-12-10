from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def __init__(self):
        super().__init__()

    def close(self):
        self.put(self.SENTINEL)
