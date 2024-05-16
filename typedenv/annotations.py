import types
import typing

def allows_none_type(t: typing.Any) -> bool:
    """Check if the given type annotation allows None as a value."""
    if t is None:
        return True

    generic_type = typing.get_origin(t)
    generic_args = typing.get_args(t)

    if generic_type is not typing.Union and generic_type is not types.UnionType:
        return False

    return types.NoneType in generic_args
