from __future__ import annotations

import os
import typing

T = typing.TypeVar("T")


def _unwrap(item: T | None) -> T:
    assert item is not None
    return item


def _prepare_directory(filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
