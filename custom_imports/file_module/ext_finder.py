import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Iterable, Optional

from custom_imports.importer import Finder

__all__ = ["FileModuleExtensionFinder"]


@dataclass(frozen=True)
class FileModuleExtensionFinder(Finder[Path]):
    """
    Finder for file based modules by file extensions.

    FileModuleExtensionFinder(ext)

    This Finder interprets a module's name as a filename, with extension ext.
    Parent modules are interpreted as directories.

    This provides a relative path, which is searched for on the standard module
    search path. If a file with that relative path is found, then the absolute
    Path of that file is returned as its module locator.
    """

    extension: str

    def find_path(self, fullname: str, search_paths: Iterable[str]) -> Optional[Path]:
        rel_file_path = Path(fullname.replace(".", "/") + "." + self.extension)

        for path in search_paths:
            abs_file_path = path / rel_file_path
            if abs_file_path.is_file():
                return abs_file_path

    def find_module_locator(
        self, fullname: str, path: Iterable[str], target: Optional[ModuleType] = None
    ) -> Optional[Path]:
        return self.find_path(fullname, sys.path)
