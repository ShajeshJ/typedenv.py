import os
import typing

from typedenv._internals import _MISSING
from typedenv.annotations import get_unioned_with_none
from typedenv.converters import ConverterDict, cast_to_bool


_T = typing.TypeVar("_T", bound="EnvLoader")
_SINGLETONS: dict[type, typing.Any] = {}


class EnvLoader:
    __frozen: typing.ClassVar[bool]
    __env_keys: typing.ClassVar[set[str]]
    __converters: typing.ClassVar[ConverterDict]

    def __init_subclass__(cls, frozen: bool = True, **kwargs) -> None:
        cls.__frozen = frozen
        cls.__env_keys = set()
        cls.__converters = ConverterDict()

        cls.__converters[str] = str
        cls.__converters[int] = int
        cls.__converters[float] = float
        cls.__converters[bool] = cast_to_bool

        return super().__init_subclass__(**kwargs)

    def __new__(cls: type[_T], *args, **kwargs) -> _T:
        global _SINGLETONS

        if cls in _SINGLETONS:
            return _SINGLETONS[cls]

        instance = super().__new__(cls, *args, **kwargs)
        instance.__load_env__()
        _SINGLETONS[cls] = instance

        return instance

    def __load_env__(self) -> None:
        for env_name, cast_type in typing.get_type_hints(
            type(self), include_extras=True
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
            elif isinstance(value, str):
                value = self.__converters[cast_type](value)
            elif value is None:
                if not is_nullable:
                    raise ValueError(f"Cannot set {env_name} to None")
                else:
                    pass  # no-op; env can be set to None
            elif not isinstance(value, cast_type):
                raise ValueError(f"Could not coerce {env_name} to {cast_type}")

            setattr(self, env_name, value)
            self.__env_keys.add(env_name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if self.__frozen and name in self.__env_keys:
            raise AttributeError(f"{name} is frozen and cannot be modified")

        return super().__setattr__(name, value)
