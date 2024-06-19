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


# TODO: Need a more robust approach than using a global variable
__converters = ConverterDict()


def clear_converters() -> None:
    global __converters
    __converters.clear()


def get_converter(type_: type[T]) -> Converter[T]:
    global __converters
    return __converters[type_]


def set_converter(type_: type[T], converter: Converter[T]) -> None:
    global __converters
    __converters[type_] = converter


def can_convert(type_: type) -> bool:
    global __converters
    return type_ in __converters
