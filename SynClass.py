from DatabaseRead import DataBase


class Sync:
    def __init__(self, filepath, sem, read_amount):
        self.semaphore = sem
        self.read_amount = read_amount
        self.writer = False
        self.db = DataBase(filepath)

    def __get_read(self, func, *args):
        with self.semaphore:
            return func(*args)

    def __get_write(self, func, *args):
        for i in range(self.read_amount):
            self.semaphore.acquire()
        func(*args)
        for i in range(self.read_amount):
            self.semaphore.release()

    def get_value(self, key):
        return self.__get_read(self.db.get_value, key)

    def set_value(self, key, val):
        return self.__get_write(self.db.set_value(key, val))

    def delete_value(self, key):
        return self.__get_write(self.db.delete_value(key))
