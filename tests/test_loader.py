import typedenv
import pytest
import typing


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("string", id="string"),
        pytest.param(1, id="int"),
        pytest.param(1.0, id="float"),
        pytest.param(False, id="bool"),
    ],
)
def test__env_loader__primitive_types(
    value: typing.Any, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("MY_KEY", str(value))

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: value.__class__

    assert MyEnv.MY_KEY == value


def test__env_loader__multiple_keys(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NUM_WORKERS", "4")
    monkeypatch.setenv("DB_URL", "sqlite://")

    class MyEnv(typedenv.EnvLoader):
        NUM_WORKERS: int
        DB_URL: str

    assert MyEnv.NUM_WORKERS == 4
    assert MyEnv.DB_URL == "sqlite://"


def test__env_loader__invalid_type(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    with pytest.raises(TypeError):

        class _(typedenv.EnvLoader):
            MY_KEY: list[str]


def test__env_loader__missing_key():
    with pytest.raises(ValueError):

        class _(typedenv.EnvLoader):
            MY_KEY: str


@pytest.mark.parametrize("type_hint", [int, float, bool])
def test__env_loader__incompatible_types(
    type_hint: typing.Any, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("MY_KEY", "string that cannot be cast")
    with pytest.raises(ValueError):

        class _(typedenv.EnvLoader):
            MY_KEY: type_hint


def test__env_loader__union_with_none(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str | None

    assert MyEnv.MY_KEY == "string"


def test__env_loader__unsupported_union(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    with pytest.raises(TypeError):

        class _(typedenv.EnvLoader):
            MY_KEY: str | int


def test__env_loader__missing_key_defaults_none():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str | None

    assert MyEnv.MY_KEY is None


@pytest.mark.parametrize(
    ["type_hint", "default"],
    [
        pytest.param(int, 1, id="int"),
        pytest.param(float, 1.0, id="float"),
        pytest.param(bool, False, id="bool"),
        pytest.param(str, "string", id="str"),
        pytest.param(int | None, 1, id="union with None"),
    ],
)
def test__env_loader__fallback_to_default(type_hint: typing.Any, default: typing.Any):
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: type_hint = default

    assert MyEnv.MY_KEY == default


def test__env_loader__ignore_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "12")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: int = 1

    assert MyEnv.MY_KEY == 12


def test__env_loader__ignore_lower_case(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("my_key", "18")

    class MyEnv(typedenv.EnvLoader):
        my_key: int = 12

    assert MyEnv.my_key == 12
