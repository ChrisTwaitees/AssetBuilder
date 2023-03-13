import os

from model.director import director

from unit_tests.director_tests import TEST_RESOURCES_DIR


class CharacterBuilderModel(object):

    def __init__(self):
        super().__init__()
        self._director = director.Director()
        # TODO Add this to config
        self._director.add_build_step_scan_directory(TEST_RESOURCES_DIR)
        self._director.add_config_scan_directory(TEST_RESOURCES_DIR)

    def get_builders_from_directory(self, directory):
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                builder = self._director.get_builder_from_filepath(filepath)
                if builder:
                    yield builder

    def get_all_configs(self):
        return self._director.get_all_configs()


