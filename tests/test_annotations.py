import pytest
import typing
import typedenv.annotations


def _dummy_func(x: None) -> None: ...


class _DummyClass: ...


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(typing.Optional[int], id="typing.Optional"),
        pytest.param(typing.Union[None, int, int | None], id="typing.Union"),
        pytest.param(int | None, id="built-in Union"),
        pytest.param(dict[int, None], id="built-in dict"),
        pytest.param(typing.Annotated[None, int], id="typing.Annotated"),
        pytest.param(tuple[None, int], id="built-in tuple"),
    ],
)
def test__get_usable_args__int_and_none(annotations: typing.Any):
    assert typedenv.annotations.get_usable_type_args(annotations) == (int,)


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(typing.Union[None, None], id="typing.Union"),
        pytest.param(dict[None, None], id="built-in dict"),
        pytest.param(list[None], id="built-in list"),
        pytest.param(typing.Annotated[None, None], id="typing.Annotated"),
    ],
)
def test__get_usable_args__only_none(annotations: typing.Any):
    assert typedenv.annotations.get_usable_type_args(annotations) == ()


@pytest.mark.parametrize(
    ("annotations", "expected"),
    [
        pytest.param(typing.Union[int, str], (int, str), id="typing.Union"),
        pytest.param(int | str, (int, str), id="built-in Union"),
        pytest.param(dict[int, str], (int, str), id="built-in dict"),
        pytest.param(typing.Annotated[str, int], (str, int), id="typing.Annotated"),
        pytest.param(list[int], (int,), id="built-in list"),
        pytest.param(
            tuple[str | None, list[None]], (str | None, list[None]), id="Inner None"
        ),
    ],
)
def test__get_usable_args__no_none(annotations: typing.Any, expected: typing.Any):
    assert typedenv.annotations.get_usable_type_args(annotations) == expected


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(str, id="built-in str"),
        pytest.param(_dummy_func, id="function"),
        pytest.param(_DummyClass, id="class"),
    ],
)
def test__get_usable_args__no_args(annotations: typing.Any):
    assert typedenv.annotations.get_usable_type_args(annotations) == ()


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(typing.Optional[int], id="typing.Optional"),
        pytest.param(typing.Union[int, list[str], None], id="typing.Union"),
        pytest.param(None | int, id="built-in Union"),
    ],
)
def test__is_union_type__returns_true(annotations: typing.Any):
    assert typedenv.annotations.is_union_type(annotations) == True


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(str, id="built-in str"),
        pytest.param(typing.Annotated[None, int], id="typing.Annotated"),
        pytest.param(_dummy_func, id="function"),
        pytest.param(_DummyClass, id="class"),
        pytest.param(dict[str, str], id="built-in dict"),
        pytest.param(list[str | int], id="nested Union"),
    ],
)
def test__is_union_type__returns_false(annotations: typing.Any):
    assert typedenv.annotations.is_union_type(annotations) == False


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(None, id="None"),
        pytest.param(int, id="int"),
        pytest.param(list[str | None], id="nested Union"),
    ],
)
def test__parse_unioned_with_none__non_union_types(annotations: typing.Any):
    assert typedenv.annotations.parse_unioned_with_none(annotations) == None


@pytest.mark.parametrize("annotations", [int | list[str], typing.Union[int, str]])
def test__parse_unioned_with_none__union_without_none(annotations: typing.Any):
    assert typedenv.annotations.parse_unioned_with_none(annotations) == None


@pytest.mark.parametrize(
    "annotations",
    [
        str | int | None,
        typing.Union[str, int, None],
        typing.Optional[str | int],
    ],
)
def test__parse_unioned_with_none__multiple_types_with_none(
    annotations: typing.Any,
):
    assert typedenv.annotations.parse_unioned_with_none(annotations) == None


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(str | None, id="built-in Union"),
        pytest.param(None | str, id="reverse built-in Union"),
        pytest.param(typing.Optional[str], id="typing.Optional"),
        pytest.param(typing.Union[None | str, str], id="redundant Union"),
    ],
)
def test__parse_unioned_with_none__one_type_with_none(annotations: typing.Any):
    assert typedenv.annotations.parse_unioned_with_none(annotations) == str
