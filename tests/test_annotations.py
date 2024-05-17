import pytest
import typing
import typedenv.annotations


def _dummy_func(x: None) -> None: ...


class _DummyClass: ...


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
    assert typedenv.annotations.parse_unioned_with_none(annotations) is None


def test__parse_union_with_none__only_none():
    assert (
        typedenv.annotations.parse_unioned_with_none(typing.Union[None, None]) is None
    )


@pytest.mark.parametrize("annotations", [int | list[str], typing.Union[int, str]])
def test__parse_unioned_with_none__union_without_none(annotations: typing.Any):
    assert typedenv.annotations.parse_unioned_with_none(annotations) is None


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
    assert typedenv.annotations.parse_unioned_with_none(annotations) is None


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
