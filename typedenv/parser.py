import os
import typing

from typedenv._internals import _MISSING
from typedenv.annotations import parse_unioned_with_none
from typedenv.converters import (
    can_convert,
    cast_to_bool,
    clear_converters,
    get_converter,
    set_converter,
)


class EnvParser:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        clear_converters()
        set_converter(str, str)
        set_converter(int, int)
        set_converter(float, float)
        set_converter(bool, cast_to_bool)

        cls.__load_env__()

    @classmethod
    def __load_env__(cls) -> None:
        for env_name, cast_type in typing.get_type_hints(
            cls, include_extras=True
        ).items():
            default: typing.Literal[_MISSING] | str | typing.Any | None = _MISSING

            unioned_type = parse_unioned_with_none(cast_type)
            if is_nullable := unioned_type is not None:
                default = None
                cast_type = unioned_type

            if not can_convert(cast_type):
                raise TypeError(f"Unsupported type: {cast_type}")

            default = getattr(cls, env_name, default)
            value = os.getenv(env_name, default)

            if value is _MISSING:
                raise ValueError(f"Missing environment variable: {env_name}")

            if value is None:
                if not is_nullable:
                    raise ValueError(f"Cannot set {env_name} to None")

                setattr(cls, env_name, None)
                continue

            if isinstance(value, cast_type):
                setattr(cls, env_name, value)
                continue

            if isinstance(value, str):
                setattr(cls, env_name, get_converter(cast_type)(value))
                continue

            raise RuntimeError("Unreachable code was reached")
