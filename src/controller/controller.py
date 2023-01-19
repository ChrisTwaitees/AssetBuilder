from view import view as asset_builder_view
from model import model as asset_builder_model
from log import LOG


class AssetBuilderController(object):

    def __init__(self, view=True):

        self.view = asset_builder_view.CharacterBuilderView if view else False
        if self.view:
            self._connect_signals()
        self.model = asset_builder_model.CharacterBuilderModel()

    def _connect_signals(self):
        LOG.debug("Connecting view signals.")
        self.view.get_builders_from_directory_signal.connect(self.model.get_builders_from_directory)
        self.model.set_builders_signal.connect(self.view.set_builders_signal)

    def launch_view(self):
        LOG.info("Launching View.")
        if not self.view:
            self.view = asset_builder_view.CharacterBuilderView()
        self.view.launch_ui()
