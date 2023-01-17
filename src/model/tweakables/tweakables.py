import typing
from dataclasses import dataclass


@dataclass
class TweakableBase:
    name: str
    value: typing.Any = None


@dataclass
class TweakableListBase(TweakableBase):
    values: list = None
