from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OperationItem:
    """Only used to simplify tests."""

    result: int
    tp: int
    sl: int
    risk: float
