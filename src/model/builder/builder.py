from dataclasses import dataclass

from log import LOG

from model.asset import asset

from model.build_step import build_step
from model.build_step import build_step_plugin_factory

from model.builder import builder_config


@dataclass
class BuilderTweakable:
    build_step_ref: build_step.BuildStep
    build_step_tweakables: dict


class Builder(object):
    def __init__(self, config=None):
        self._asset = asset.Asset()
        self._build_steps: [build_step.BuildStep] = []
        self._tweakables: [BuilderTweakable] = []
        self._current_config: builder_config.BuildConfig = config
        self._compatible_configs: [builder_config.BuildConfig] = []

    @property
    def config(self):
        return self._current_config

    @config.setter
    def config(self, value: builder_config.BuildConfig):
        self._current_config = value
        self.load_config(self._current_config)

    @property
    def compatible_configs(self):
        return self._compatible_configs

    @compatible_configs.setter
    def compatible_configs(self, value: [builder_config.BuildConfig]):
        self._compatible_configs = value

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        if isinstance(value, asset.Asset):
            self._asset = asset
            for step in self._build_steps:
                step.asset = self._asset
            self._initialize_tweakables()

    @property
    def build_steps(self):
        return self._build_steps

    @property
    def tweakables(self) -> [BuilderTweakable]:
        return self._tweakables

    def build(self):
        build_results = []
        self._set_tweakables()
        for step in self._build_steps:
            build_result = step.build(self._asset)
            build_results.append(build_result)

    def load_config(self, build_config: builder_config.BuildConfig):
        self._build_steps = []
        for step in build_config.steps:
            # Get a reference to the build step's class
            step_cls = build_step_plugin_factory.BuildStepPluginFactory.get_build_step_by_name(step)
            if step_cls:
                # Add an instance of the step
                self._build_steps.append(step_cls(self._asset))
            else:
                LOG.warning(f"Could not find Build Step : {step}, has it been implemented "
                            f"and within a scan directory?")
        # Load tweakables
        self._initialize_tweakables()

    def _initialize_tweakables(self):
        """ Collects references to build steps and any tweakables set within them. """
        self._tweakables = []

        for step in self._build_steps:
            if step.tweakables:
                new_tweakable = BuilderTweakable(build_step_ref=step,
                                                 build_step_tweakables=step.tweakables)
                self._tweakables.append(new_tweakable)

    def _set_tweakables(self):
        """ Iterates over build steps, re-setting tweakables. """
        for tweakable in self._tweakables:
            for step in self._build_steps:
                if tweakable.build_step_ref == step:
                    for tweak_attr, tweak_val in tweakable.build_step_tweakables.items():
                        setattr(step, tweak_attr, tweak_val)
