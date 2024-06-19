import typing
import pytest

import typedenv.converters


@pytest.fixture(autouse=True)
def clear_converters():
    yield
    typedenv.converters.clear_converters()


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
    typedenv.converters.set_converter(str, str)
    typedenv.converters.set_converter(int, int)
    typedenv.converters.set_converter(float, float)
    typedenv.converters.set_converter(bool, bool)

    assert isinstance(typedenv.converters.get_converter(str)("yoyo"), str)
    assert isinstance(typedenv.converters.get_converter(int)("42"), int)
    assert isinstance(typedenv.converters.get_converter(float)("42"), float)
    assert isinstance(typedenv.converters.get_converter(bool)("true"), bool)


def test__converter_dict__can_convert():
    typedenv.converters.set_converter(bool, bool)

    assert typedenv.converters.can_convert(bool) == True
    assert typedenv.converters.can_convert(int) == False


def test__converter_dict__complex():
    def complex_converter(value: str) -> list[str]:
        return value.split(",")

    typedenv.converters.set_converter(list[str], complex_converter)
    typedenv.converters.set_converter(str, str)

    converter = typedenv.converters.get_converter(list[str])
    assert typing.get_type_hints(converter) == {"value": str, "return": list[str]}
