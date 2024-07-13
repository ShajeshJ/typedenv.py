import json
import typing

import pytest

import typedenv


def str_append_foo(value: str) -> str:
    return value + "foo"


def str_append_bar(value: str) -> str:
    return value + "bar"


def int_add_10(value: str) -> int:
    return int(value) + 10


def float_divide_2(value: str) -> float:
    return float(value) / 2


def bool_negate(value: str) -> bool:
    return not bool(value)


@pytest.mark.parametrize(
    ["value", "actual", "converter"],
    [
        pytest.param(
            "string", "stringfoo", typedenv.Converter(str_append_foo), id="string"
        ),
        pytest.param(1, 11, typedenv.Converter(int_add_10), id="int"),
        pytest.param(1.0, 0.5, typedenv.Converter(float_divide_2), id="float"),
        pytest.param(True, False, typedenv.Converter(bool_negate), id="bool"),
    ],
)
def test__env_loader__primitive_types__annotated(
    value: typing.Any,
    actual: typing.Any,
    converter: typedenv.Converter,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("MY_KEY", str(value))

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[value.__class__, converter]

    assert MyEnv().MY_KEY == actual


def test__env_loader__annotated_mixed(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DB_URL", "sqlite://")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    class MyEnv(typedenv.EnvLoader):
        DB_URL: typing.Annotated[str, typedenv.Converter(str_append_foo)]
        LOG_LEVEL: str

    assert MyEnv().DB_URL == "sqlite://foo"
    assert MyEnv().LOG_LEVEL == "INFO"


def test__env_loader__multiple__annotated(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DB_URL", "sqlite://")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    class MyEnv(typedenv.EnvLoader):
        DB_URL: typing.Annotated[str, typedenv.Converter(str_append_foo)]
        LOG_LEVEL: typing.Annotated[str, typedenv.Converter(str_append_bar)]

    assert MyEnv().DB_URL == "sqlite://foo"
    assert MyEnv().LOG_LEVEL == "INFObar"


def test__env_loader__incompatible__annotated(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[int, typedenv.Converter(str_append_foo)]

    with pytest.raises(TypeError):
        MyEnv()


def test__env_loader__missing_key__annotated():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[str, typedenv.Converter(str_append_foo)]

    with pytest.raises(ValueError):
        MyEnv()


def test__env_loader__union_with_none__annotated(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[str | None, typedenv.Converter(str_append_foo)]

    assert MyEnv().MY_KEY == "stringfoo"


def test__env_loader__multi_union_with_none__annotated(monkeypatch: pytest.MonkeyPatch):
    def str_or_int(value: str) -> str | int:
        return int(value) if value.isdigit() else value

    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[str | int | None, typedenv.Converter(str_or_int)]

    assert MyEnv().MY_KEY == "string"


def test__env_loader__missing_key_defaults_none__annotated():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[str | None, typedenv.Converter(str_append_foo)]

    assert MyEnv().MY_KEY is None


@pytest.mark.parametrize(
    ["type_hint", "default", "converter"],
    [
        pytest.param(int, 1, typedenv.Converter(int_add_10), id="int"),
        pytest.param(float, 1.0, typedenv.Converter(float_divide_2), id="float"),
        pytest.param(bool, True, typedenv.Converter(bool_negate), id="bool"),
        pytest.param(str, "string", typedenv.Converter(str_append_foo), id="str"),
        pytest.param(
            int | None, 1, typedenv.Converter(int_add_10), id="union with None"
        ),
    ],
)
def test__env_loader__fallback_to_default__annotated(
    type_hint: typing.Any, default: typing.Any, converter: typedenv.Converter
):
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[type_hint, converter] = default

    assert MyEnv().MY_KEY == default


def test__env_loader__ignore_default__annotated(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "12")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: typing.Annotated[int, typedenv.Converter(int_add_10)] = 1

    assert MyEnv().MY_KEY == 22


def test__env_loader__custom_converter__and_annotated(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("UPPERCASE", "uppercase")
    monkeypatch.setenv("LOWERCASE", "LOWERCASE")

    def lowercase(value: str) -> str:
        return value.lower()

    def uppercase(value: str) -> str:
        return value.upper()

    class MyEnv(typedenv.EnvLoader, converters=[typedenv.Converter(lowercase)]):
        UPPERCASE: typing.Annotated[str, typedenv.Converter(uppercase)]
        LOWERCASE: str

    assert MyEnv().UPPERCASE == "UPPERCASE"
    assert MyEnv().LOWERCASE == "lowercase"
