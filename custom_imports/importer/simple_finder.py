from dataclasses import dataclass, field
from types import ModuleType
from typing import Callable, Iterable, Optional, TypeVar

from custom_imports.importer.types import Finder
from custom_imports.utils import field_required

__all__ = ["SimpleFinder"]

LT = TypeVar("LT")  # Locator type.


@dataclass(frozen=True)
class SimpleFinder(Finder[LT]):
    """
    A basic Finder class.

    SimpleFinder(
        locate_module=func,
    )

    Finds a module locator by calling func(fullname, path, target).
    """

    locate_module: Callable[
        [str, Iterable[str], Optional[ModuleType]], Optional[LT]
    ] = field(default_factory=field_required)

    def find_module_locator(
        self, fullname: str, path: Iterable[str], target: Optional[ModuleType] = None
    ) -> Optional[LT]:
        return self.locate_module(fullname, path, target)
