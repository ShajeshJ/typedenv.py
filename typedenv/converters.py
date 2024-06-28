import typing


T = typing.TypeVar("T")
Converter = typing.Callable[[str], T]


class ConverterDict(dict[type, Converter]):
    def __setitem__(self, key: type[T], value: Converter[T]) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key: type[T]) -> Converter[T]:
        return super().__getitem__(key)

    def __missing__(self, key: type[T]) -> Converter[T]:
        raise KeyError(key)


def cast_to_bool(value: str) -> bool:
    if value.lower() in ("true", "1"):
        return True
    if value.lower() in ("false", "0"):
        return False
    raise ValueError(f"Unsupported boolean value: {value}")
