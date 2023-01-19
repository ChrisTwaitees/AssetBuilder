import os
import unittest

from model.director import director

TEST_RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


class DirectorUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.director = director.Director()
        cls.test_psd_filepath = r"C:\Users\ChrisThwaites\Desktop\CharacterBuilder\test_assets\ThisisIsATestFile.psd"
        cls.director.add_config_scan_directory(TEST_RESOURCES_DIR)
        cls.director.add_build_step_scan_directory(TEST_RESOURCES_DIR)

    def test_director_gets_config_from_path(self):
        config = self.director.get_builder_config_from_filepath(self.test_psd_filepath)
        self.assertEqual(config.name, "TestContainsRegex")

    def test_director_gets_builder_from_path(self):
        builder = self.director.get_builder_from_filepath(self.test_psd_filepath)
        print(builder.build_steps)

