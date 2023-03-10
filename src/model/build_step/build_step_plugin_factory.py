import os
from importlib.machinery import SourceFileLoader

from model.utils import files

from model.build_step import build_step
from log import LOG

BUILD_STEPS_DIR = os.path.join(os.path.dirname(__file__), "steps")


class BuildStepPluginFactory(object):
    __plugins__: [build_step.BuildStep] = []
    __scan_directories__ = [BUILD_STEPS_DIR]

    @classmethod
    def get_scan_directories(cls):
        return cls.__scan_directories__

    @classmethod
    def get_build_steps(cls):
        if not cls.__plugins__:
            cls.reload_plugins()
        return cls.__plugins__

    @classmethod
    def get_build_step_by_name(cls, name):
        for plugin in cls.get_build_steps():
            if plugin.__step_name__.lower() == name.lower():
                return plugin

    # PLUGINS
    @classmethod
    def add_scan_directory(cls, scan_directory: str) -> None:
        cls.__scan_directories__.append(scan_directory)
        cls.__scan_directories__ = list(set(cls.__scan_directories__))
        cls.reload_plugins()

    @classmethod
    def reload_plugins(cls):
        # Collect all .py files
        files_to_scan = files.get_filepaths_with_extension(cls.__scan_directories__, ".py")
        # Import all modules
        for file in files_to_scan:
            module_name = os.path.basename(file).removesuffix(".py")
            SourceFileLoader(module_name, file).load_module()

        # Return all subclasses loaded
        cls.__plugins__ = [bld_step for bld_step in build_step.BuildStep.__subclasses__()]
        return cls.__plugins__
