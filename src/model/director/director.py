"""
Character Setup Director Class.

The design pattern picked for Character Setup is the Builder
Creation pattern.

https://sourcemaking.com/design_patterns/builder

The Director interprets what build steps (builder.build_step.BuildStep)
from the given filepath and parses them to the builder
(builder.builder.Builder)

"""
import os
import re

from model.builder import builder
from model.builder.builder_config import BuilderConfigLoader
from model.build_step.build_step_plugin_factory import BuildStepPluginFactory


class Director(object):
    @staticmethod
    def add_config_scan_directory(directory):
        BuilderConfigLoader.add_scan_directory(directory)

    @staticmethod
    def add_build_step_scan_directory(directory):
        BuildStepPluginFactory.add_scan_directory(directory)

    @staticmethod
    def get_builder_config_from_filepath(filepath: str):
        filename = os.path.basename(filepath)
        for config in BuilderConfigLoader.get_configs():
            if config.regex:
                if re.match(config.regex, filename):
                    return config

    @classmethod
    def get_builder_from_filepath(cls, filepath: str):
        config = cls.get_builder_config_from_filepath(filepath)
        if config:
            new_builder = builder.Builder()
            new_builder.asset.raw_path = filepath
            new_builder.load_config(config)
            return new_builder
