from DatabaseRead import DataBase


class Sync:
    def __init__(self, filepath, sem_read, lock_write, read_amount):
        self.semaphore = sem_read
        self.lock_write = lock_write
        self.read_amount = read_amount
        self.writer = False
        self.db = DataBase(filepath)

    def __get_read(self, func, *args):
        r_value = None
        try:
            self.semaphore.acquire()
            r_value = func(*args)
        except Exception as ex:
            print(ex)
        finally:
            self.semaphore.release()
            return r_value

    def __get_write(self, func, *args):
        r_value = None
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

    def get_value(self, key):
        return self.__get_read(self.db.get_value, key)

    def set_value(self, key, val):
        return self.__get_write(self.db.set_value, key, val)

    def delete_value(self, key):
        return self.__get_write(self.db.delete_value, key)
