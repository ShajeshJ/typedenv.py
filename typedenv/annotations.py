import types
import typing


def is_union_type(t: typing.Any) -> bool:
    """Check if the given type annotation is a Union type."""
    generic_type = typing.get_origin(t)
    return generic_type is typing.Union or generic_type is types.UnionType


def get_usable_type_args(t: typing.Any) -> tuple[typing.Any, ...]:
    """Get all non-None arguments for a type annotation.
    An empty tuple is returned for type annotations that don't take arguments.
    """
    return tuple(arg for arg in typing.get_args(t) if arg not in (None, type(None)))
