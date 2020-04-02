from __future__ import annotations

from dataclasses import dataclass, field
from io import IOBase
from pathlib import Path
from typing import Callable, TypeVar

from custom_imports.importer import Module, SimpleLoader
from custom_imports.utils import field_required

__all__ = ["FileModuleLoader"]

MT = TypeVar("MT")  # Module type.


def load_file_module(
    loader: FileModuleLoader[MT], module: Module[Path, MT], path: Path
) -> None:
    with path.open() as file:
        loader.read_module(module, file)


@dataclass(frozen=True)
class FileModuleLoader(SimpleLoader[Path, MT]):
    """
    Loader for file based modules.

    A file based module is a module that is generated from a single file.

    FileModuleLoader(
        module_type=cls,
        module_type_kwargs=kwargs,
        read_module=func,
    )

    This Loader takes a Path to the file to be loaded as its module locator,
    creates an empty module by calling the equivalent of cls(**kwargs),
    and executes it by calling func(module, file).

    The file handle passed to func is closed after func terminates.
    """

    load_module: Callable[[Module[Path, MT], Path], None] = field(
        default=load_file_module, init=False
    )
    read_module: Callable[[Module[Path, MT], IOBase], None] = field(
        default_factory=field_required
    )
