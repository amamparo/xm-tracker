from abc import ABC, abstractmethod
from os import path, makedirs
from typing import List

import boto3
import ujson
from botocore.exceptions import ClientError
from injector import inject

from src.environment import Environment


class Bucket(ABC):
    @abstractmethod
    def write_lines(self, key: str, data: List[dict]) -> None:
        pass

    @abstractmethod
    def read_lines(self, key: str) -> List[dict]:
        pass


def _to_jsonl(data: List[dict]) -> str:
    return '\n'.join([ujson.dumps(x) for x in data])


def _from_jsonl(jsonl: str) -> List[dict]:
    return [ujson.loads(x) for x in jsonl.split('\n') if x.strip()]


class LocalBucket(Bucket):
    def write_lines(self, key: str, data: List[dict]) -> None:
        full_path = self.__get_full_path(key)
        makedirs(path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(_to_jsonl(data))

    def read_lines(self, key: str) -> List[dict]:
        full_path = self.__get_full_path(key)
        if not path.exists(full_path):
            return []
        with open(full_path, 'r') as f:
            return _from_jsonl(f.read())

    @staticmethod
    def __get_full_path(key: str) -> str:
        return path.join(path.dirname(__file__), '..', '.localbucket', key)


class S3Bucket(Bucket):
    @inject
    def __init__(self, environment: Environment):
        self.__client = boto3.client('s3')
        self.__bucket = environment.bucket

    def write_lines(self, key: str, data: List[dict]) -> None:
        self.__client.put_object(Bucket=self.__bucket, Key=key, Body=_to_jsonl(data))

    def read_lines(self, key: str) -> List[dict]:
        if not self.__exists(key):
            return []
        body = self.__client.get_object(Bucket=self.__bucket, Key=key)['Body'].read().decode('utf-8')
        return _from_jsonl(body)

    def __exists(self, key: str):
        try:
            self.__client.head_object(Bucket=self.__bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise
