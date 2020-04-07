from typing import Any

__all__ = ["AttrDict"]


class AttrDict(dict):
    """
    Wrapper of dict class, to allow usage of attribute notation (instance.key)
    in place of index notation (instance["key"]).

    Can be used as a mixin for Mappings.
    """

    def __getattr__(self, item: str) -> Any:
        if item in self:
            return self[item]

        return getattr(super(), item)
