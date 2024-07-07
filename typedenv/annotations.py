import types
import typing


def is_union_type(t: typing.Any) -> bool:
    """Check if the given type annotation is a Union type."""
    origin_type = typing.get_origin(t)
    return origin_type is typing.Union or origin_type is types.UnionType


def get_unioned_with_none(t: typing.Any) -> typing.Any:
    """Parses an annotation that Unions 1 type with None and returns that type.

    Example:
    - typing.Union[int, None] -> int
    - typing.Optional[int] -> int
    - int | None -> int

    If the given type is not a Union with None, None is returned instead.
    """
    if not is_union_type(t):
        return None

    match typing.get_args(t):
        case (types.NoneType, x) | (x, types.NoneType):
            return x
        case _:
            return None


def get_annotated_args(t: typing.Any) -> tuple[typing.Any, ...] | None:
    """Parses a typing.Annotated type and returns the inner type and its args.

    If the given type is not an Annotated type, None is returned instead.
    """
    origin_type = typing.get_origin(t)
    if origin_type is not typing.Annotated:
        return None

    return typing.get_args(t)
