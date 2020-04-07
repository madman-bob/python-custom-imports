import json
from pathlib import Path

from custom_imports.file_module import FileModuleExtensionFinder, FileModuleLoader
from custom_imports.importer import Importer

__all__ = ["json_importer"]

json_importer = Importer[Path, dict](
    finder=FileModuleExtensionFinder(extension="json"),
    loader=FileModuleLoader[dict](
        module_type=dict,
        read_module=lambda module, file: module.update(json.load(file)),
    ),
)
