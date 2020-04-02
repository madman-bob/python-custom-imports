import sys
from dataclasses import dataclass
from importlib.abc import MetaPathFinder
from types import ModuleType
from typing import Generic, Iterable, Optional, TypeVar

from custom_imports.importer.types import Finder, Loader, ModuleSpec

__all__ = ["Importer"]

LT = TypeVar("LT")  # Locator type.
MT = TypeVar("MT")  # Module type.


@dataclass(frozen=True)
class Importer(MetaPathFinder, Generic[LT, MT]):
    """
    A basic Importer class.

    Importer(
        finder=finder,
        loader=loader,
    )

    When registered, this Importer overloads `import` syntax to additionally
    attempt to use finder to find modules, and loader to load them.

    Register an Importer with importer.register()
    Deregister an Importer with importer.deregister()

    May also be used as a context manager:

    with foo_importer:
        import foo

    with the importer registering itself at the start of the block, and
    deregistering itself at the end.
    """

    finder: Finder[LT]
    loader: Loader[LT, MT]

    def find_spec(
        self, fullname: str, path: Iterable[str], target: Optional[ModuleType] = None
    ) -> Optional[ModuleSpec[LT, MT]]:
        module_locator = self.finder.find_module_locator(fullname, path, target)

        if module_locator is None:
            return None

        return ModuleSpec(fullname, self.loader, loader_state=module_locator)

    def register(self):
        sys.meta_path.append(self)

    def deregister(self):
        sys.meta_path.remove(self)

    def __enter__(self):
        self.register()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deregister()
