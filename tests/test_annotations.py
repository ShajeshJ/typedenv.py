import typing

import pytest

import typedenv.annotations


def _dummy_func(x: None) -> None: ...


class _DummyClass: ...


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(int, id="int"),
        pytest.param(str, id="built-in str"),
        pytest.param(None, id="None"),
        pytest.param(_dummy_func, id="function"),
        pytest.param(_DummyClass, id="class"),
        pytest.param(typing.Annotated[None, int], id="typing.Annotated"),
        pytest.param(dict[str, None], id="built-in dict"),
        pytest.param(list[str | None], id="nested Union"),
    ],
)
def test__get_unioned_with_none__non_union_types(annotations: typing.Any):
    assert typedenv.annotations.get_unioned_with_none(annotations) is None


def test__get_unioned_with_none__only_none():
    assert typedenv.annotations.get_unioned_with_none(typing.Union[None, None]) is None


@pytest.mark.parametrize("annotations", [int | list[str], typing.Union[int, str]])
def test__get_unioned_with_none__union_without_none(annotations: typing.Any):
    assert typedenv.annotations.get_unioned_with_none(annotations) is None


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(str | None, id="built-in Union"),
        pytest.param(None | str, id="reverse built-in Union"),
        pytest.param(typing.Optional[str], id="typing.Optional"),
        pytest.param(typing.Union[None | str, str], id="redundant Union"),
    ],
)
def test__get_unioned_with_none__one_type_with_none(annotations: typing.Any):
    assert typedenv.annotations.get_unioned_with_none(annotations) == str


@pytest.mark.parametrize(
    ["annotations", "expected"],
    [
        pytest.param(str | int | None, str | int, id="built-in union"),
        pytest.param(
            typing.Union[str, int, None], typing.Union[str, int], id="typing.Union"
        ),
        pytest.param(
            typing.Optional[str | int], typing.Union[str, int], id="typing.Optional"
        ),
        pytest.param(
            typing.Union[int, list[str], None],
            typing.Union[int, list[str]],
            id="nested args",
        ),
    ],
)
def test__get_unioned_with_none__multiple_types_with_none(
    annotations: typing.Any, expected: typing.Any
):
    actual = typedenv.annotations.get_unioned_with_none(annotations)
    assert type(actual) == type(expected)
    assert actual == expected


def test__get_annotations__not_annotated():
    assert typedenv.annotations.get_annotated_args(str) is None
    assert typedenv.annotations.get_annotated_args(typing.Optional[str]) is None
    assert typedenv.annotations.get_annotated_args(typing.Union[str, int]) is None


def test__get_annotations__annotated():
    args = typedenv.annotations.get_annotated_args(typing.Annotated[str, int])
    assert args == (str, int)


def test__get_annotations_complex_annotations():
    class Metadata:
        def __eq__(self, other):
            return isinstance(other, Metadata)

    args = typedenv.annotations.get_annotated_args(
        typing.Annotated[str, "some random metadata", Metadata()]
    )
    assert args == (str, "some random metadata", Metadata())
