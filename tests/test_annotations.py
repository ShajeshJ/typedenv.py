import pytest
import typing
import typedenv.annotations


def _dummy_func(x: None) -> None:
    ...

class _DummyClass:
    ...

@pytest.mark.parametrize("annotations", [
    typing.Optional[int],
    typing.Union[int, list[str], None],
    None | int,
    None,
])
def test__allow_annotations_none__true_cases(annotations: typing.Any):
    assert typedenv.annotations.allows_none_type(annotations) == True

@pytest.mark.parametrize("annotations", [
    str,
    typing.Callable[[int], None],
    typing.Annotated[None, int],
    typing.Union[str, int],
    str | int,
    _dummy_func,
    _DummyClass,
])
def test__allow_annotations_none__false_cases(annotations: typing.Any):
    assert typedenv.annotations.allows_none_type(annotations) == False
