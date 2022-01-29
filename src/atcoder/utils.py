import typing

T = typing.TypeVar("T")


def unwrap(item: typing.Optional[T]) -> T:
    assert item is not None
    return item
