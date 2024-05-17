import typedenv
import typedenv.parse
import pytest
import typing


@pytest.mark.parametrize(
    ["value", "type_hint"],
    [
        pytest.param("string", str, id="string"),
        pytest.param(1, int, id="int"),
        pytest.param(1.0, float, id="float"),
        pytest.param(False, bool, id="bool"),
    ],
)
def test__env_parser__primitive_types(
    value: typing.Any, type_hint: typing.Any, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("MY_KEY", str(value))

    class MyEnv(typedenv.EnvParser):
        MY_KEY: type_hint

    assert MyEnv.MY_KEY == value


def test__env_parser__multiple_keys(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NUM_WORKERS", "4")
    monkeypatch.setenv("DB_URL", "sqlite://")

    class MyEnv(typedenv.EnvParser):
        NUM_WORKERS: int
        DB_URL: str

    assert MyEnv.NUM_WORKERS == 4
    assert MyEnv.DB_URL == "sqlite://"


def test__env_parser__invalid_type(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    with pytest.raises(TypeError):

        class _(typedenv.EnvParser):
            MY_KEY: list[str]


def test__env_parser__missing_key():
    with pytest.raises(ValueError):

        class _(typedenv.EnvParser):
            MY_KEY: str


@pytest.mark.parametrize("type_hint", [int, float, bool])
def test__env_parser__incompatible_types(
    type_hint: typing.Any, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("MY_KEY", "string that cannot be cast")
    with pytest.raises(ValueError):

        class _(typedenv.EnvParser):
            MY_KEY: type_hint


def test__env_parser__union_with_none(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvParser):
        MY_KEY: str | None

    assert MyEnv.MY_KEY == "string"


def test__env_parser__unsupported_union(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    with pytest.raises(TypeError):

        class _(typedenv.EnvParser):
            MY_KEY: str | int


def test__env_parser__missing_key_defaults_none():
    class MyEnv(typedenv.EnvParser):
        MY_KEY: str | None

    assert MyEnv.MY_KEY is None


@pytest.mark.parametrize("input_str", ["true", "1", "TRUE", "True"])
def test__cast_to_bool__true(input_str: str):
    assert typedenv.parse.cast_to_bool(input_str) == True


@pytest.mark.parametrize("input_str", ["false", "0", "FALSE", "False"])
def test__cast_to_bool__false(input_str: str):
    assert typedenv.parse.cast_to_bool(input_str) == False
