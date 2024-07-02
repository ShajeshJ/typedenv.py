import os
import typing

from typedenv._internals import _MISSING
from typedenv.annotations import get_unioned_with_none
from typedenv.converters import ConverterDict, cast_to_bool


_SINGLETONS: dict[type, typing.Any] = {}


class EnvLoader:
    __converters: ConverterDict

    def __new__(cls, *args, **kwargs):
        if cls in _SINGLETONS:
            return _SINGLETONS[cls]

        instance = super(EnvLoader, cls).__new__(cls, *args, **kwargs)

        instance.__converters = ConverterDict()

        instance.__converters[str] = str
        instance.__converters[int] = int
        instance.__converters[float] = float
        instance.__converters[bool] = cast_to_bool

        instance.__load_env__()

        _SINGLETONS[cls] = instance
        return instance

    def __load_env__(self) -> None:
        for env_name, cast_type in typing.get_type_hints(
            self, include_extras=True
        ).items():
            if not env_name.isupper():
                continue

            default: typing.Literal[_MISSING] | str | typing.Any | None = _MISSING

            unioned_type = get_unioned_with_none(cast_type)
            if is_nullable := unioned_type is not None:
                default = None
                cast_type = unioned_type

            if cast_type not in self.__converters:
                raise TypeError(f"Unsupported type: {cast_type}")

            default = getattr(self, env_name, default)
            value = os.getenv(env_name, default)

            if value is _MISSING:
                raise ValueError(f"Missing environment variable: {env_name}")

            if value is None:
                if not is_nullable:
                    raise ValueError(f"Cannot set {env_name} to None")

                setattr(self, env_name, None)
                continue

            if isinstance(value, cast_type):
                setattr(self, env_name, value)
                continue

            if isinstance(value, str):
                setattr(self, env_name, self.__converters[cast_type](value))
                continue

            raise RuntimeError("Unreachable code was reached")
