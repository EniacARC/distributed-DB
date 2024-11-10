from DatabaseRead import DataBase
import threading
import multiprocessing
from typing import Callable, Any


class Sync:
    def __init__(self, filepath: str, sem_read: threading.Semaphore | multiprocessing.Semaphore,
                 lock_write: threading.Lock | multiprocessing.Lock, read_amount: int) -> None:
        """
        Initializes the Sync class for controlling concurrent read/write operations.

        :param filepath: Path to the database file.
        :param sem_read: Semaphore to control read access (allows a limited number of concurrent readers).
        :param lock_write: Lock for write operations to ensure exclusive write access.
        :param read_amount: The maximum number of concurrent readers allowed.
        """
        self.semaphore: threading.Semaphore | multiprocessing.Semaphore = sem_read
        self.lock_write: threading.Lock | multiprocessing.Lock = lock_write
        self.read_amount: int = read_amount
        self.writer: bool = False
        self.db: DataBase = DataBase(filepath)

    def __get_read(self, func: Callable[..., Any], *args: Any) -> Any:
        """
        Perform a read operation, ensuring proper semaphore management.

        :param func: The function to be called for the read operation.
        :param args: Arguments to be passed to the read function.
        :return: The result of the read function.
        """
        r_value: Any = None
        try:
            self.semaphore.acquire()
            r_value = func(*args)
        except Exception as ex:
            print(ex)
        finally:
            self.semaphore.release()
            return r_value

    def __get_write(self, func: Callable[..., Any], *args: Any) -> Any:
        """
        Perform a write operation, ensuring proper lock and semaphore management.

        :param func: The function to be called for the write operation.
        :param args: Arguments to be passed to the write function.
        :return: The result of the write function.
        """
        r_value: Any = None
        try:
            self.lock_write.acquire()
            for _ in range(self.read_amount):
                self.semaphore.acquire()

            r_value = func(*args)
        except Exception as ex:
            print(ex)
        finally:
            for _ in range(self.read_amount):
                self.semaphore.release()
            self.lock_write.release()
            return r_value

    def get_value(self, key: str) -> Any:
        """
        Get the value associated with a key.

        :param key: The key whose value is to be retrieved.
        :return: The value associated with the key.
        """
        return self.__get_read(self.db.get_value, key)

    def set_value(self, key: str, val: Any) -> bool:
        """
        Set the value associated with a key.

        :param key: The key to associate with the value.
        :param val: The value to set.
        :return: True if the value was successfully set, False otherwise.
        """
        return self.__get_write(self.db.set_value, key, val)

    def delete_value(self, key: str) -> None:
        """
        Delete the value associated with a key.

        :param key: The key whose value is to be deleted.
        """
        self.__get_write(self.db.delete_value, key)
