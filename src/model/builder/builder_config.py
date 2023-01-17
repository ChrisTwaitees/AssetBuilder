import os
import json
from dataclasses import dataclass

from log import LOG
from model.utils import files

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), "configs")


@dataclass
class BuildConfig:
    name: str = ""
    steps: [str] = ""
    # Optional
    regex: str = ""
    parent: str = ""


class BuilderConfigLoader(object):
    __scan_directories__ = [CONFIGS_DIR]
    __configs__: [BuildConfig] = []

    # PROPERTIES
    @classmethod
    def get_configs(cls) -> [BuildConfig]:
        if not cls.__configs__:
            cls.reload__configs__()
        return cls.__configs__

    @classmethod
    def get_scan_directories(cls):
        return cls.__scan_directories__

    # DIRECTORIES
    @classmethod
    def add_scan_directory(cls, scan_directory: str) -> None:
        cls.__scan_directories__.append(scan_directory)
        cls._scan_directories = list(set(cls.__scan_directories__))
        cls.reload__configs__()

    @classmethod
    def get_config_by_name(cls, config_name):
        for config in cls.get_configs():
            if config.name == config_name:
                return config

    @classmethod
    def reload__configs__(cls):
        # clear configs
        cls.__configs__ = []

        json_paths = files.get_filepaths_with_extension(cls.__scan_directories__, ".json")
        for path in json_paths:
            with open(path) as data:
                data_dict = json.load(data)
            # Create builder config for each valid data dict
            for config_data in data_dict:
                # check for required keys
                required_keys = ["name", "steps"]
                if all([k in config_data.keys() for k in required_keys]):
                    new_config = BuildConfig()
                    for attr, val in config_data.items():
                        if hasattr(new_config, attr):
                            setattr(new_config, attr, val)
                    cls.__configs__.append(new_config)
                else:
                    LOG.warning(f"Config data : {config_data} is missing required keys : 'name' and 'steps'.")

        # Resolve parents
        for config in cls.get_configs():
            config.steps = cls._expand_parent_config_recursive(config, config.steps)

    @classmethod
    def _expand_parent_config_recursive(cls, config, steps_list):
        if config.parent:
            parent_config = cls.get_config_by_name(config.parent)
            if parent_config:
                steps_copy = parent_config.steps
                [steps_copy.append(step) for step in steps_list if step not in steps_copy]
                steps_list = steps_copy
                if parent_config.parent:
                    return cls._expand_parent_config_recursive(parent_config, steps_list)
        return steps_list
