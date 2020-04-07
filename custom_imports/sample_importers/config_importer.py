import configparser
from dataclasses import replace
from pathlib import Path

from custom_imports.file_module import FileModuleExtensionFinder, FileModuleLoader
from custom_imports.importer import Importer
from custom_imports.utils.attr_dict import AttrDict

__all__ = ["ini_importer", "cfg_importer"]


class ConfigParser(configparser.ConfigParser, AttrDict):
    """
    Wrapper for ConfigParser to allow attribute notation for sections.

    For section names that clash with ConfigParser attributes, the ConfigParser
    version is used. For example, a section called `items`.
    """


class SectionProxy(configparser.SectionProxy, AttrDict):
    """
    Wrapper for SectionProxy to allow attribute notation for properties.

    For property names that clash with SectionProxy attributes, the SectionProxy
    version is used. For example, a property called `name`.
    """


class BasicInterpolation(configparser.Interpolation):
    def before_read(self, parser, section, option, value):
        for func in [int, float, parser._convert_to_boolean]:
            try:
                return func(value)
            except ValueError:
                pass

        return value


configparser.ConfigParser = ConfigParser
configparser.SectionProxy = SectionProxy

ini_importer = Importer[Path, ConfigParser](
    finder=FileModuleExtensionFinder(extension="ini"),
    loader=FileModuleLoader[ConfigParser](
        module_type=ConfigParser,
        module_type_kwargs={"interpolation": BasicInterpolation()},
        read_module=lambda module, file: module.read_file(file),
    ),
)

cfg_importer = replace(ini_importer, finder=FileModuleExtensionFinder(extension="cfg"))
