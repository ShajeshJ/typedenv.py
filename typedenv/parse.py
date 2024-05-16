import os
import typing

from typedenv.annotations import get_usable_type_args, is_union_type


def cast_to_bool(value: str) -> bool:
    if value.lower() in ("true", "1"):
        return True
    if value.lower() in ("false", "0"):
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


class EnvParser:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__load_env__()

    @classmethod
    def __load_env__(cls) -> None:
        for env_name, cast_type in typing.get_type_hints(
            cls, include_extras=True
        ).items():
            if is_union_type(cast_type):
                cast_type = get_usable_type_args(cast_type)
                cast_type = cast_type[0] if len(cast_type) == 1 else cast_type

            if cast_type not in (str, int, float, bool):
                raise TypeError(f"Unsupported type: {cast_type}")

            value = os.getenv(env_name)
            if value is None:
                raise ValueError(f"Missing environment variable: {env_name}")

            if cast_type is bool:
                setattr(cls, env_name, cast_to_bool(value))
            else:
                setattr(cls, env_name, cast_type(value))
