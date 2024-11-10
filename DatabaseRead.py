import os

from Database import Database
import re
import pickle
from typing import BinaryIO


class DataBase(Database):
    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.__filepath = filepath
        self.change = True
        if re.search(r"\w+\.pickle$", filepath) is None:
            raise Exception("db file is not valid!")

        if not os.path.exists(filepath):
            # Create the file if it doesn't exist
            with open(filepath, 'wb') as f:
                # Optionally write an initial value or leave it empty
                pickle.dump(self.db, f)

    # file logic
    def __load_dict(self) -> None:
        if self.change:
            with open(self.__filepath, "rb") as f:
                self.db = pickle.load(f)
            self.change = False

    def __write_to_file(self):
        with open(self.__filepath, "wb") as f:
            pickle.dump(self.db, f)
        self.change = True

    # need read perms
    def get_value(self, key: str) -> object:
        self.__load_dict()
        return super().get_value(key)

    # need write permissions
    def set_value(self, key: str, val: object) -> bool:
        self.__load_dict()
        r_val = super().set_value(key, val)
        self.__write_to_file()
        return r_val

    def delete_value(self, key: str) -> None:
        self.__load_dict()
        super().delete_value(key)
        self.__write_to_file()
