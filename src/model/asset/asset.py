from dataclasses import dataclass

from model.tweakables import tweakables


@dataclass
class Asset:
    name: str = ""
    raw_path: str = ""
    depot_path: str = ""
    source_path: str = ""


@dataclass
class AssetTweakable(tweakables.TweakableBase):
    pass


@dataclass
class AssetListTweakable(tweakables.TweakableListBase):
    pass
