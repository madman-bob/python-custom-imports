from dataclasses import dataclass, field
from types import ModuleType
from typing import Callable, Type, TypeVar

from more_properties import cached_property

from custom_imports.importer.types import Loader, Module, ModuleSpec
from custom_imports.utils import field_required

__all__ = ["SimpleLoader"]

LT = TypeVar("LT")  # Locator type.
MT = TypeVar("MT")  # Module type.


@dataclass(frozen=True)
class SimpleLoader(Loader[LT, MT]):
    """
    A basic Loader class.

    SimpleLoader(
        module_type=cls,
        module_type_kwargs=kwargs,
        load_module=func,
    )

    Creates an empty module by calling the equivalent of cls(**kwargs),
    and executes it by calling func(module, module_locator).
    """

    module_type: Type[MT]
    module_type_kwargs: dict = field(default_factory=dict)
    load_module: Callable[[Module[LT, MT], LT], None] = field(
        default_factory=field_required
    )

    @cached_property
    def _module_type(self) -> Type[Module[LT, MT]]:
        if issubclass(self.module_type, (Module, ModuleType)):
            return self.module_type

        class _Module(Module, self.module_type):
            pass

        return _Module

    def create_module(self, spec: ModuleSpec[LT, MT]) -> Module[LT, MT]:
        return self._module_type(**self.module_type_kwargs)

    def exec_module(self, module: Module[LT, MT]) -> None:
        self.load_module(module, module.__spec__.loader_state)
