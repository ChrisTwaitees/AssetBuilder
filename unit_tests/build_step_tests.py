import os
import unittest
from log import LOG

from model.asset import asset
from model.build_step import build_step
from model.build_step import build_step_plugin_factory

from unit_tests.resources import test_build_step

TEST_BUILD_STEPS_DIR = os.path.join(os.path.dirname(__file__), "resources")


class BuildStepsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.build_step_factory = build_step_plugin_factory.BuildStepPluginFactory()

    def test_build_step_factory_add_directory(self):
        self.build_step_factory.add_scan_directory(TEST_BUILD_STEPS_DIR)
        self.assertIn(TEST_BUILD_STEPS_DIR, self.build_step_factory.get_scan_directories())

    def test_build_step_factory_get_plugins(self):
        self.build_step_factory.add_scan_directory(TEST_BUILD_STEPS_DIR)
        build_steps = self.build_step_factory.get_build_steps()
        self.assertIsInstance(build_steps[0](asset.Asset()), build_step.BuildStep)

    def test_get_build_step_by_name(self):
        test_build_step_name = "Test Build Step"
        build_step = self.build_step_factory.get_build_step_by_name(test_build_step_name)
        self.assertIsInstance(build_step(asset.Asset()), test_build_step.TestBuildStep)

