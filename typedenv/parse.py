import os
import typing


def cast_to_bool(value: str) -> bool:
    if value.lower() in ("true", "1"):
        return True
    if value.lower() in ("false", "0"):
        return False
    raise ValueError(f"Invalid boolean value: {value}")


class EnvParser:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__load_env__()

    @classmethod
    def __load_env__(cls) -> None:
        for env_name, cast_type in typing.get_type_hints(
            cls, include_extras=True
        ).items():
            if cast_type not in (str, int, float, bool):
                raise ValueError(f"Invalid type: {cast_type}")

            value = os.getenv(env_name)
            if value is None:
                raise ValueError(f"Missing environment variable: {env_name}")

            if cast_type is bool:
                setattr(cls, env_name, cast_to_bool(value))
            else:
                setattr(cls, env_name, cast_type(value))
