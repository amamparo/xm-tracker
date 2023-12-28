from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Environment:
    bucket: str = environ.get('BUCKET')
