from Database import Database
import re
import pickle
from typing import BinaryIO


class DataBase(Database):
    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath
        if re.search(r"^\w+\.pickle", filepath) is None:
            raise Exception("db file is not valid!")

    def load_dict(self) -> None:
        with open(self.__filepath, "rb") as f:
            self.db = pickle.load(f)

    def write_to_file(self):
        with open(self.__filepath, "wb") as f:
            pickle.dump(self.db, f)

    def set_value(self, key: str, val: object) -> bool:
        self.load_dict()
        r_val = super().set_value(key, val)
        self.write_to_file()
        return r_val

    def get_value(self, key: str) -> object:
        self.load_dict()
        return super().get_value(key)

    def delete_value(self, key: str) -> None:
        self.load_dict()
        super().delete_value(key)
        self.write_to_file()
