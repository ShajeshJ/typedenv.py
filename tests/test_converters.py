import pytest

import typedenv.converters


@pytest.mark.parametrize("input_str", ["true", "1", "TRUE", "True"])
def test__cast_to_bool__true(input_str: str):
    assert typedenv.converters.cast_to_bool(input_str) == True


@pytest.mark.parametrize("input_str", ["false", "0", "FALSE", "False"])
def test__cast_to_bool__false(input_str: str):
    assert typedenv.converters.cast_to_bool(input_str) == False
