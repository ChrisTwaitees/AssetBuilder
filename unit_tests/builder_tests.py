import os
import unittest

from model.builder import builder
from model.builder import builder_config

from model.build_step.build_step_plugin_factory import BuildStepPluginFactory

TEST_RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


class BuilderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        BuildStepPluginFactory.add_scan_directory(TEST_RESOURCES_DIR)

        builder_config_loader = builder_config.BuilderConfigLoader()
        builder_config_loader.add_scan_directory(TEST_RESOURCES_DIR)
        cls.test_build_config = builder_config_loader.get_config_by_name("TestMinimumConfig")
        cls.test_edit_asset_config = builder_config_loader.get_config_by_name("TestEditAssetConfig")

        cls.builder = builder.Builder()

    def test_builder_loads_config(self):
        test_step = BuildStepPluginFactory.get_build_step_by_name("Test Build Step")
        self.builder.load_config(self.test_build_config)
        self.assertIsInstance(self.builder.build_steps[0], test_step)

    def test_builder_get_tweakables(self):
        self.builder.load_config(self.test_build_config)
        print(self.builder.tweakables)

    def test_builder_build(self):
        self.builder.load_config(self.test_build_config)
        print(self.builder.build())

    def test_builder_edit_tweakables(self):
        self.builder.load_config(self.test_build_config)
        # Edit the tweakable
        edited = ["edited", "tags"]
        self.builder.tweakables[0].build_step_tweakables["tags"].values = edited
        self.builder._set_tweakables()
        self.assertEqual(self.builder.build_steps[0].tags.values, edited)

    def test_builder_edit_tweakables_and_build(self):
        self.builder.load_config(self.test_build_config)
        # Edit the tweakable
        edited = ["edited", "tags"]
        self.builder.tweakables[0].build_step_tweakables["tags"].values = edited
        self.builder.tweakables[0].build_step_tweakables["brands"].value = "NewBrand"
        self.builder._set_tweakables()

        self.builder.build()
        self.assertEqual(self.builder.build_steps[0].tags.values, edited)

    def test_builder_edit_asset_during_build(self):
        self.builder.load_config(self.test_edit_asset_config)
        self.builder.build()
        self.assertEqual(self.builder.asset.source_path, "Edited by Test Build Step")


class BuilderConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = builder.Builder()
        builder_config.BuilderConfigLoader.add_scan_directory(TEST_RESOURCES_DIR)

    def test_builder_config_add_directory(self):
        test_builder = builder_config.BuilderConfigLoader()
        test_builder.add_scan_directory(TEST_RESOURCES_DIR)
        self.assertIn(TEST_RESOURCES_DIR,
                      builder_config.BuilderConfigLoader.get_scan_directories())

    def test_load_configs(self):
        """ Check we've loaded atleast the test config"""
        self.assertNotEqual(builder_config.BuilderConfigLoader.get_configs(), [])

    def test_get_config_by_name(self):
        test_config_name = "TestMinimumConfig"
        self.assertIsInstance(builder_config.BuilderConfigLoader.get_config_by_name(test_config_name),
                              builder_config.BuildConfig)

    def test_minimum_config(self):
        test_config_name = "TestMinimumConfig"
        config = builder_config.BuilderConfigLoader.get_config_by_name(test_config_name)

        test = builder_config.BuildConfig()
        test.name = "TestMinimumConfig"
        test.steps = ["Test Build Step"]
        self.assertEqual(config, test)

    def test_nested_config(self):
        test_nested_config = "TestContainsNestedParent"
        config = builder_config.BuilderConfigLoader.get_config_by_name(test_nested_config)

        test = builder_config.BuildConfig()
        test.name = "TestContainsNestedParent"
        test.steps = ['Test Build Step', 'Foo Step', 'A base parent', 'secondary leve', 'Bar Step',
                      'tertiary level', 'Zap Step', 'child step', 'Foxtrot Step']
        test.parent = 'TestContainsParent'
        self.assertEqual(config, test)
