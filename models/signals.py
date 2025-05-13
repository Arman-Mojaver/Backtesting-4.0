from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalGroup:
    long_signals: list[int]
    short_signals: list[int]

    def to_request_format(self) -> dict[str, list[int]]:
        return {
            "long_signals": self.long_signals,
            "short_signals": self.short_signals,
        }
