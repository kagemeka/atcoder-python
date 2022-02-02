import os
import typing

T = typing.TypeVar("T")


def unwrap(item: typing.Optional[T]) -> T:
    assert item is not None
    return item


def prepare_directory(filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
