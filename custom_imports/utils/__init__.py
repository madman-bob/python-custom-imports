from typing import Any

__all__ = ["field_required"]


def field_required() -> Any:
    """
    Use as a dataclass field default_factory argument to indicate
    a required, keyword-only field.
    """
    raise TypeError("Missing required keyword-only argument")
