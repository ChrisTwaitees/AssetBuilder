import os

from PySide2.QtCore import Signal, QObject

from model.director import director

from unit_tests.director_tests import TEST_RESOURCES_DIR


class CharacterBuilderModel(QObject):
    set_builders_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self._director = director.Director()
        # TODO Add this to config
        self._director.add_build_step_scan_directory(TEST_RESOURCES_DIR)
        self._director.add_config_scan_directory(TEST_RESOURCES_DIR)

    def get_builders_from_directory(self, directory):
        builders = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                builder = self._director.get_builder_from_filepath(filepath)
                if builder:
                    builders.append(builder)
        self.set_builders_signal.emit(builders)