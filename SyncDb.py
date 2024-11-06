import threading
import multiprocessing
from SynClass import Sync


class SyncDatabase(Sync):
    def __init__(self, filepath, mode, amount):
        if mode != 0 and mode != 1:
            raise Exception("invalid mode!")
        if mode == 0:  # multi threading
            semaphore = threading.Semaphore(amount)
        else:
            semaphore = multiprocessing.Semaphore(amount)

        super().__init__(filepath, semaphore, amount)
