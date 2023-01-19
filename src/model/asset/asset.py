from model.tweakables import tweakables


class Asset(object):
    def __init__(self):
        self.name = ""
        self.raw_path = ""
        self.depot_path = ""
        self.source_path = ""


class AssetTweakable(tweakables.TweakableBase):
    def __init__(self, name="", value=None):
        super(AssetTweakable, self).__init__(name=name,
                                             value=value)


class AssetListTweakable(tweakables.TweakableListBase):
    def __init__(self, name="", value=None, values=()):
        super(AssetListTweakable, self).__init__(name=name,
                                                 value=value,
                                                 values=values)
