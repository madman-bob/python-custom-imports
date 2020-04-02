from abc import ABCMeta, abstractmethod
from importlib.abc import Loader as LoaderBase
from importlib.machinery import ModuleSpec as ModuleSpecBase
from types import ModuleType
from typing import Any, Dict, Generic, Iterable, Optional, TypeVar

__all__ = ["ModuleSpec", "Module", "Finder", "Loader"]

LT = TypeVar("LT")  # Locator type.
MT = TypeVar("MT")  # Module type.


class ModuleSpec(ModuleSpecBase, Generic[LT, MT]):
    """
    Typed module specification.

    Contains all the information required to construct a module of type MT.

    The module is constructed using loader `loader`, and locator `loader_state`.

    A module locator is an object that contains sufficient information for
    a corresponding loader to directly load that module.
    """

    name: str
    loader: "Loader[LT, MT]"
    origin: Optional[str]
    loader_state: LT
    submodule_search_locations: Iterable[str]


class Module(Generic[LT, MT], metaclass=ABCMeta):
    """
    Typed abstract base class for modules.

    This class does not actually inherit from ModuleType as that causes
    multiple base lay-out conflict when attempting to use a builtin as a module
    type.
    Instead, __class__ is defined to pretend to inherit from ModuleType.
    """

    __name__: str
    __file__: str
    __dict__: Dict[str, Any]
    __loader__: "Optional[Loader[LT, MT]]"
    __package__: Optional[str]
    __spec__: Optional[ModuleSpec[LT, MT]]

    __class__ = ModuleType


class Finder(Generic[LT], metaclass=ABCMeta):
    """
    Typed abstract base class for module finders.

    Module finders search for a module among the various paths available.
    If it finds a module, it returns a locator for that module of type LT,
    otherwise it returns None.

    Module finders do not attempt to construct the module.
    """

    @abstractmethod
    def find_module_locator(
        self, fullname: str, path: Iterable[str], target: Optional[ModuleType] = None
    ) -> Optional[LT]:
        raise NotImplementedError


class Loader(LoaderBase, Generic[LT, MT], metaclass=ABCMeta):
    """
    Typed abstract base class for module loaders.

    Module loaders construct located modules.

    `create_module` should create an empty module of type MT.

    `exec_module` should take an object of type MT, and execute the contents of
    the module using the passed object as its namespace.
    Note that the locator of the module may be found at this point as
    module.__spec__.loader_state.
    """

    @abstractmethod
    def create_module(self, spec: ModuleSpec[LT, MT]) -> Module[LT, MT]:
        raise NotImplementedError

    @abstractmethod
    def exec_module(self, module: Module[LT, MT]) -> None:
        raise NotImplementedError
