import json
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

    assert MyEnv().MY_KEY == value


def test__env_loader__multiple_keys(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NUM_WORKERS", "4")
    monkeypatch.setenv("DB_URL", "sqlite://")

    class MyEnv(typedenv.EnvLoader):
        NUM_WORKERS: int
        DB_URL: str

    assert MyEnv().NUM_WORKERS == 4
    assert MyEnv().DB_URL == "sqlite://"


def test__env_loader__invalid_type(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: list[str]

    with pytest.raises(TypeError):
        MyEnv()


def test__env_loader__missing_key():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str

    with pytest.raises(ValueError):
        MyEnv()


@pytest.mark.parametrize("type_hint", [int, float, bool])
def test__env_loader__incompatible_types(
    type_hint: typing.Any, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("MY_KEY", "string that cannot be cast")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: type_hint

    with pytest.raises(ValueError):
        MyEnv()


def test__env_loader__union_with_none(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str | None

    assert MyEnv().MY_KEY == "string"


def test__env_loader__unsupported_union(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "string")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str | int

    with pytest.raises(TypeError):
        MyEnv()


def test__env_loader__missing_key_defaults_none():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str | None

    assert MyEnv().MY_KEY is None


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

    assert MyEnv().MY_KEY == default


def test__env_loader__ignore_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "12")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: int = 1

    assert MyEnv().MY_KEY == 12


def test__env_loader__ignore_lower_case(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("my_key", "18")

    class MyEnv(typedenv.EnvLoader):
        my_key: int = 12

    assert MyEnv().my_key == 12


def test__env_loader__creates_singleton(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_STR", "starting string")

    class MyEnv(typedenv.EnvLoader):
        MY_STR: str

    env1 = MyEnv()
    monkeypatch.setenv("MY_STR", "env keys should not reload values for the same class")
    env2 = MyEnv()

    assert env1 is env2
    assert env2.MY_STR == "starting string"


def test__env_loader__multiple_configs(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_STR", "a string")
    monkeypatch.setenv("MY_INT", "14")

    class Foo(typedenv.EnvLoader):
        MY_STR: str

    class Bar(typedenv.EnvLoader):
        MY_INT: int

    foo = Foo()
    bar = Bar()

    assert isinstance(foo, Foo)
    assert isinstance(bar, Bar)
    assert foo.MY_STR == "a string"
    assert bar.MY_INT == 14


def test__env_loader__override_type():
    class Base(typedenv.EnvLoader):
        SOME_KEY: str | None

    class Child(Base):
        SOME_KEY: str

    assert Base().SOME_KEY is None
    with pytest.raises(ValueError):
        Child()


def test__env_loader__override_default():
    class Base(typedenv.EnvLoader):
        SOME_KEY: int

    class Child(Base):
        SOME_KEY = 13

    with pytest.raises(ValueError):
        Base()

    assert Child().SOME_KEY == 13


def test__env_loader__with_inheritance(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BASE_STR", "only the base class shouold see this value")
    monkeypatch.setenv("CHILD_STR", "child-only value")

    class Base(typedenv.EnvLoader):
        BASE_STR: str

    class Child(Base):
        CHILD_STR: str

    base = Base()
    monkeypatch.setenv("BASE_STR", "updated base value for child")
    child = Child()

    assert base.BASE_STR == "only the base class shouold see this value"
    assert child.BASE_STR == "updated base value for child"
    assert child.CHILD_STR == "child-only value"


def test__env_loader__mismatched_types():
    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str = 12  # type: ignore

    with pytest.raises(ValueError):
        MyEnv()


def test__env_loader__frozen(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "env value")

    class MyEnv(typedenv.EnvLoader):
        MY_KEY: str

    with pytest.raises(AttributeError):
        MyEnv().MY_KEY = "new value"


def test__env_loader__mutable(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_KEY", "env value")

    class MyEnv(typedenv.EnvLoader, frozen=False):
        MY_KEY: str

    env = MyEnv()
    env.MY_KEY = "new value"
    assert env.MY_KEY == "new value"


def test__env_loader__regular_attrs_mutable():
    class MyEnv(typedenv.EnvLoader):
        regular_attr: str

    env = MyEnv()
    env.regular_attr = "new value"
    assert env.regular_attr == "new value"


def test__env_loader__inheritance__mutable_parent(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BASE_KEY", "old base value")
    monkeypatch.setenv("CHILD_KEY", "old child value")

    class Base(typedenv.EnvLoader, frozen=False):
        BASE_KEY: str

    class Child(Base):
        CHILD_KEY: str

    base = Base()
    child = Child()

    base.BASE_KEY = "new base value"

    with pytest.raises(AttributeError):
        child.BASE_KEY = "new child value"

    with pytest.raises(AttributeError):
        child.CHILD_KEY = "new child value"

    assert base.BASE_KEY == "new base value"
    assert child.BASE_KEY == "old base value"
    assert child.CHILD_KEY == "old child value"


def test__env_loader__inheritance__mutable_child(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BASE_KEY", "old base value")
    monkeypatch.setenv("CHILD_KEY", "old child value")

    class Base(typedenv.EnvLoader):
        BASE_KEY: str

    class Child(Base, frozen=False):
        CHILD_KEY: str

    base = Base()
    child = Child()

    with pytest.raises(AttributeError):
        base.BASE_KEY = "new base value"

    child.BASE_KEY = "new base value"
    child.CHILD_KEY = "new child value"

    assert base.BASE_KEY == "old base value"
    assert child.BASE_KEY == "new base value"
    assert child.CHILD_KEY == "new child value"


def test__env_loader__custom_converter(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("INT_VALS", "9, 3, 6")

    def get_int_list(value: str) -> list[int]:
        return [int(x) for x in value.split(",")]

    class MyEnv(
        typedenv.EnvLoader, extra_converters=[typedenv.Converter(get_int_list)]
    ):
        INT_VALS: list[int]

    assert MyEnv().INT_VALS == [9, 3, 6]


def test__env_loader__generic_must_be_precise_type(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("INT_VALS", "9, 3, 6")

    def get_int_list(value: str) -> list[int]:
        return [int(x) for x in value.split(",")]

    class MyEnv(
        typedenv.EnvLoader, extra_converters=[typedenv.Converter(get_int_list)]
    ):
        INT_VALS: list[str]

    with pytest.raises(TypeError):
        MyEnv()


def test__env_loader__mixed_conversion(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BASIC_INT", "42")
    monkeypatch.setenv("KEBAB_STR", "default-string-converter-should-be-overridden")
    monkeypatch.setenv("JSON_ENV", '{"config1": "value1", "config2": "value2"}')

    def json_dict_from_str(value: str) -> dict[str, str]:
        return json.loads(value)

    def kebab_to_whitespace(value: str) -> str:
        return value.replace("-", " ")

    class MyEnv(
        typedenv.EnvLoader,
        extra_converters=[
            typedenv.Converter(json_dict_from_str),
            typedenv.Converter(kebab_to_whitespace),
        ],
    ):
        BASIC_INT: int
        KEBAB_STR: str
        JSON_ENV: dict[str, str]

    assert MyEnv().BASIC_INT == 42
    assert MyEnv().KEBAB_STR == "default string converter should be overridden"
    assert MyEnv().JSON_ENV == {"config1": "value1", "config2": "value2"}
