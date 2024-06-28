import typing
import pytest

import typedenv.converters


@pytest.mark.parametrize("input_str", ["true", "1", "TRUE", "True"])
def test__cast_to_bool__true(input_str: str):
    assert typedenv.converters.cast_to_bool(input_str) == True


@pytest.mark.parametrize("input_str", ["false", "0", "FALSE", "False"])
def test__cast_to_bool__false(input_str: str):
    assert typedenv.converters.cast_to_bool(input_str) == False


def test__cast_to_bool__invalid():
    with pytest.raises(ValueError):
        typedenv.converters.cast_to_bool("invalid")


def test__converter_dict__primitives():
    converters = typedenv.converters.ConverterDict()

    converters[str] = str
    converters[int] = int
    converters[float] = float
    converters[bool] = bool

    assert isinstance(converters[str]("yoyo"), str)
    assert isinstance(converters[int]("42"), int)
    assert isinstance(converters[float]("42"), float)
    assert isinstance(converters[bool]("true"), bool)


def test__converter_dict__can_convert():
    converters = typedenv.converters.ConverterDict()

    converters[bool] = bool

    assert bool in converters
    assert int not in converters


def test__converter_dict__complex():
    def complex_converter(value: str) -> list[str]:
        return value.split(",")

    converters = typedenv.converters.ConverterDict()

    converters[list[str]] = complex_converter
    converters[str] = str

    c = converters[list[str]]
    assert typing.get_type_hints(c) == {"value": str, "return": list[str]}
