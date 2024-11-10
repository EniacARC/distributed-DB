from abc import ABC


class Database(ABC):
    def __init__(self) -> None:
        # self.__filepath = filepath
        # if re.search(r"^\w+\.pickle", filepath) is None:
        #     raise Exception("db file is not not valid!")
        self.db = {}

    # def __do_action(self, func, *args):
    #     with open(self.__filepath, "rb") as f:
    #         func(f, args)
    #     with open(self.__filepath, "wb") as f:
    #         pickle.dump()
    def set_value(self, key: str, val: object) -> bool:
        if not isinstance(key, str):
            return False
        # if key in self.db:
        self.db[key] = val
        return True
        # return False

    def get_value(self, key: str) -> object:
        if not isinstance(key, str):
            return False
        if key in self.db:
            return self.db[key]
        return None

    def delete_value(self, key: str) -> None:
        if not isinstance(key, str):
            return
        if key in self.db:
            del self.db[key]
