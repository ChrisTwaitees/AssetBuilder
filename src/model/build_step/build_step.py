"""
Abstract build step class.

Used by model.builder.Builder to execute list of ordered build
steps. Must implement "build" method.
"""
from abc import ABCMeta, abstractmethod

from model.tweakables import tweakables


class BuildStepResult:
    """ Data class storing results of a build a run"""
    def __init__(self, message="", success=False):
        self.message = message
        self.success = success


class BuildStepTweakable(tweakables.TweakableBase):
    def __init__(self, name="", value=None):
        super(BuildStepTweakable, self).__init__(name=name,
                                                 value=value)


class BuildStepListTweakable(tweakables.TweakableListBase):
    def __init__(self, name="", value=None, values=()):
        super(BuildStepListTweakable, self).__init__(name=name,
                                                     value=value,
                                                     values=values)


class BuildStep:
    __metaclass__ = ABCMeta
    """
    Abstract build step.

    __step_name__ used within config .jsons to append an instance of the build step to a builder
    __description__ used within UI.
    """
    __step_name__ = ""
    __description__ = ""

    def __init__(self, asset_ref):
        self.asset = asset_ref

    @abstractmethod
    def build(self, asset):
        raise NotImplementedError("build needs to return a BuildResult")

    @property
    def tweakables(self):
        return {attr: value for attr, value in self.__dict__.items()
                if isinstance(value, tweakables.TweakableBase) or isinstance(value, tweakables.TweakableListBase)}
