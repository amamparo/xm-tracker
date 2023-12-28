from os import path, makedirs
from typing import List
import ujson


class LocalS3:
    def write_lines(self, key: str, data: List[dict]) -> None:
        full_path = self.__get_full_path(key)
        makedirs(path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write('\n'.join([ujson.dumps(x) for x in data]))

    def read_lines(self, key: str) -> List[dict]:
        full_path = self.__get_full_path(key)
        if not path.exists(full_path):
            return []
        with open(full_path, 'r') as f:
            return [ujson.loads(x) for x in f.readlines() if x.strip()]

    @staticmethod
    def __get_full_path(key: str) -> str:
        return path.join(path.dirname(__file__), '..', '.localbucket', key)
