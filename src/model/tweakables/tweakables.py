class TweakableBase(object):
    def __init__(self, name="", value=None):
        self.name = name
        self.value = value


class TweakableListBase(TweakableBase):
    def __init__(self, name="", value=None, values=()):
        super(TweakableListBase, self).__init__(name=name,
                                                value=value)
        self.values = values
