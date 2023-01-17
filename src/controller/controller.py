from view import view
from model import model


class AssetBuilderController(object):

    def __init__(self):
        self.view = view.CharacterBuilderView()
        self.model = model.CharacterBuilderModel()
        self._connect_signals()

    def _connect_signals(self):
        self.view.get_builders_from_directory_signal.connect(self.model.get_builders_from_directory)
        self.model.set_builders_signal.connect(self.view.set_builders_signal)

    def run(self):
        self.view.launch_ui()
