from abc import ABC
from typing import Optional


class Database(ABC):
    def __init__(self) -> None:
        """
        Initializes an empty database dictionary.
        """
        self.db: dict[str, object] = {}

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets a value in the database for the specified key.

        :param key: The key associated with the value.
        :param val: The value to associate with the key.
        :return: True if the value was set successfully, otherwise False.
        """
        if not isinstance(key, str):
            return False
        self.db[key] = val
        return True

    def get_value(self, key: str) -> Optional[object]:
        """
        Retrieves the value associated with the given key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key or None if the key doesn't exist.
        """
        if not isinstance(key, str):
            return None
        return self.db.get(key)

    def delete_value(self, key: str) -> None:
        """
        Deletes the value associated with the given key.

        :param key: The key whose associated value is to be deleted.
        """
        if not isinstance(key, str):
            return
        if key in self.db:
            del self.db[key]
