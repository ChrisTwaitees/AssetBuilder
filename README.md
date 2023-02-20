# AssetBuilder
[![TechStack](https://skillicons.dev/icons?i=python)](https://skillicons.dev)

An implementation of the "Builder" pattern.

AssetBuilder is a framework for configuring the execution order and parameters of a series of scripts to run on a single file.

Scripts are loaded into the session by either the config or through the plugin loader. A class inheriting from "BuildStep" registers the class for configuration.

End users are able to further tweak the execution settings after configured.

Written in Python3, with dependencies on PyQt. Can run headless. 
