import types
import typing

def is_union_type(t: typing.Any) -> bool:
    """Check if the given type annotation is a Union type."""
    generic_type = typing.get_origin(t)
    return generic_type is typing.Union or generic_type is types.UnionType

def allows_none_type(t: typing.Any) -> bool:
    """Check if the given type annotation allows None as a value."""
    if t is None:
        return True

    generic_type = typing.get_origin(t)
    generic_args = typing.get_args(t)

    if generic_type is not typing.Union and generic_type is not types.UnionType:
        return False

    return types.NoneType in generic_args
