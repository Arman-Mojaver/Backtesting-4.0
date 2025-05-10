from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalGroup:
    long_signals: list[str]
    short_signals: list[str]

    def to_request_format(self) -> dict[str, list[str]]:
        return {
            "long_signals": self.long_signals,
            "short_signals": self.short_signals,
        }
