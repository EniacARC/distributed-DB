import threading
import multiprocessing
from SynClass import Sync


class SyncDatabase(Sync):
    def __init__(self, filepath: str, mode: bool, amount: int) -> None:
        """
        Initialize SyncDatabase with either threading or multiprocessing.

        :param filepath: Path to the database file.
        :param mode: If True, use threading; if False, use multiprocessing.
        :param amount: The number of concurrent readers allowed.
        """
        if mode:  # threading
            semaphore: threading.Semaphore = threading.Semaphore(amount)
            lock: threading.Lock = threading.Lock()
        else:  # multiprocessing
            semaphore: multiprocessing.Semaphore = multiprocessing.Semaphore(amount)
            lock: multiprocessing.Lock = multiprocessing.Lock()

        super().__init__(filepath, semaphore, lock, amount)
