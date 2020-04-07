from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from custom_imports.file_module import FileModuleExtensionFinder, FileModuleLoader
from custom_imports.importer import Finder, Importer, Loader
from custom_imports.utils import field_required

__all__ = ["CSVImporter"]


@dataclass(frozen=True)
class CSVImporter(Importer[Path, list]):
    """
    An Importer class for CSV files.

    CSVImporter(
        csv_reader=csv_reader,
        csv_reader_kwargs=kwargs,
    )

    This file based module importer finds a CSV file by the extension .csv, and
    loads it as a module, using the result of csv_reader(file, **kwargs).

    `csv_reader` should be a CSV reader class (for example, csv.reader, or
    csv.DictReader).
    """

    finder: Finder[Path] = field(
        default=FileModuleExtensionFinder(extension="csv"), init=False
    )
    loader: Loader[Path, list] = field(
        default=property(
            lambda self: FileModuleLoader[list](
                module_type=list,
                read_module=lambda module, file: module.extend(
                    self.csv_reader(file, **self.csv_reader_kwargs)
                ),
            )
        ),
        init=False,
    )
    csv_reader: Callable = field(default_factory=field_required)
    csv_reader_kwargs: dict = field(default_factory=dict)
