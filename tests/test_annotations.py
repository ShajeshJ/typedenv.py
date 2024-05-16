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
    assert typedenv.annotations.get_usable_args(annotations) == (int,)


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(typing.Union[None, None], id="typing.Union"),
        pytest.param(dict[None, None], id="built-in dict"),
        pytest.param(tuple[None], id="built-in tuple"),
        pytest.param(list[None], id="built-in list"),
        pytest.param(set[None], id="built-in set"),
        pytest.param(typing.Annotated[None, None], id="typing.Annotated"),
    ],
)
def test__get_usable_args__only_none(annotations: typing.Any):
    assert typedenv.annotations.get_usable_args(annotations) == ()


@pytest.mark.parametrize(
    ("annotations", "expected"),
    [
        pytest.param(typing.Union[int, str, int | str], (int, str), id="typing.Union"),
        pytest.param(int | str, (int, str), id="built-in Union"),
        pytest.param(dict[int, str], (int, str), id="built-in dict"),
        pytest.param(typing.Annotated[str, int], (str, int), id="typing.Annotated"),
        pytest.param(tuple[int, str], (int, str), id="built-in tuple"),
        pytest.param(list[int], (int,), id="built-in list"),
        pytest.param(set[int], (int,), id="built-in set"),
        pytest.param(typing.Callable[..., int], (Ellipsis, int), id="typing.Callable"),
        pytest.param(
            tuple[str | None, list[None]], (str | None, list[None]), id="Inner None"
        ),
    ],
)
def test__get_usable_args__no_none(annotations: typing.Any, expected: typing.Any):
    assert typedenv.annotations.get_usable_args(annotations) == expected


@pytest.mark.parametrize(
    "annotations",
    [
        pytest.param(str, id="built-in str"),
        pytest.param(_dummy_func, id="function"),
        pytest.param(_DummyClass, id="class"),
    ],
)
def test__get_usable_args__no_args(annotations: typing.Any):
    assert typedenv.annotations.get_usable_args(annotations) == ()


@pytest.mark.parametrize(
    "annotations",
    [
        typing.Optional[int],
        typing.Union[int, list[str], None],
        None | int,
    ],
)
def test__is_union_type__true_cases(annotations: typing.Any):
    assert typedenv.annotations.is_union_type(annotations) == True


@pytest.mark.parametrize(
    "annotations",
    [
        str,
        typing.Callable[[None], None],
        typing.Annotated[None, int],
        _dummy_func,
        _DummyClass,
        dict[str, str],
        list[str | int],
    ],
)
def test__is_union_type__false_cases(annotations: typing.Any):
    assert typedenv.annotations.is_union_type(annotations) == False
