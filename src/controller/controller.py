from view import view
from model import model


class AssetBuilderController(object):

    def __init__(self):
        self.view = view.CharacterBuilderView()
        self.model = model.CharacterBuilderModel()
        self._connect_signals()
        self._initialize()

    def _initialize(self):
        self.get_all_configs()

    def _connect_signals(self):
        self.view.import_tab.get_builders_from_directory_signal.connect(self.get_builders_from_directory)
        self.view.config_tab.refresh_configs.connect(self.get_all_configs)

    def get_builders_from_directory(self, directory):
        builders = list(self.model.get_builders_from_directory(directory))
        self.view.import_tab.set_builders(builders)

    def get_all_configs(self):
        configs = list(self.model.get_all_configs())
        self.view.config_tab.set_configs(configs)

    def run(self):
        self.view.launch_ui()
