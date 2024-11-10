from typing import Union
import threading
import multiprocessing
from DatabaseRead import DataBase


class Sync:
    def __init__(self, filepath: str, sem_read: Union[threading.Semaphore, multiprocessing.Semaphore],
                 lock_write: Union[threading.Lock, multiprocessing.Lock], read_amount: int) -> None:
        """
        Initializes the Sync class for controlling concurrent read/write operations.

        :param filepath: Path to the database file.
        :param sem_read: Semaphore to control read access (allows a limited number of concurrent readers).
        :param lock_write: Lock for write operations to ensure exclusive write access.
        :param read_amount: The maximum number of concurrent readers allowed.
        """
        self.semaphore = sem_read
        self.lock_write = lock_write
        self.read_amount = read_amount
        self.writer = False
        self.db = DataBase(filepath)

    def __get_read(self, func, *args) -> object:
        """
        Handles the read operation with semaphore locking.

        :param func: The function to execute (e.g., `db.get_value`).
        :param args: Arguments to pass to the function.
        :return: The result of the function call (object).
        """
        r_value = None
        try:
            self.semaphore.acquire()
            r_value = func(*args)
        except Exception as ex:
            print(ex)
        finally:
            self.semaphore.release()
            return r_value

    def __get_write(self, func, *args) -> bool:
        """
        Handles the write operation with both semaphore and lock.

        :param func: The function to execute (e.g., `db.set_value` or `db.delete_value`).
        :param args: Arguments to pass to the function.
        :return: The result of the function call (bool).
        """
        r_value = False
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

    def get_value(self, key: str) -> object:
        """
        Retrieves a value associated with the given key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key.
        """
        return self.__get_read(self.db.get_value, key)

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets the value associated with the given key.

        :param key: The key to set the value for.
        :param val: The value to associate with the key.
        :return: True if the value was set successfully, False otherwise.
        """
        return self.__get_write(self.db.set_value, key, val)

    def delete_value(self, key: str) -> bool | None:
        """
        Deletes the value associated with the given key.

        :param key: The key whose associated value is to be deleted.
        """
        return self.__get_write(self.db.delete_value, key)