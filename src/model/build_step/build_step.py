"""
Abstract build step class.

Used by model.builder.Builder to execute list of ordered build
steps. Must implement "build" method.
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod

from model.asset import asset
from model.tweakables import tweakables


@dataclass
class BuildStepResult:
    """ Data class storing results of a build a run"""
    message: str
    success: bool


@dataclass
class BuildStepTweakable(tweakables.TweakableBase):
    pass


@dataclass
class BuildStepListTweakable(tweakables.TweakableListBase):
    pass


class BuildStep(ABC):
    """
    Abstract build step.

    __step_name__ used within config .jsons to append an instance of the build step to a builder
    __description__ used within UI.
    """
    __step_name__ = ""
    __description__ = ""

    def __init__(self, asset_ref: asset.Asset):
        self.asset = asset_ref

    @abstractmethod
    def build(self, asset: asset.Asset) -> BuildStepResult:
        raise NotImplementedError("build needs to return a BuildResult")

    @property
    def tweakables(self) -> {str: tweakables.TweakableBase}:
        return {attr: value for attr, value in self.__dict__.items()
                if isinstance(value, tweakables.TweakableBase) or isinstance(value, tweakables.TweakableListBase)}
