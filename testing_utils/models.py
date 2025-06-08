from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IndicatorValue:
    timestamp: int
    value: float


@dataclass
class IndicatorValues:
    items: list[IndicatorValue]

    def to_fixture_format(self) -> str:
        rows = [
            """from __future__ import annotations

b0 = ["""
        ]
        opening_bracket, closing_bracket = "{", "}"

        for item in self.items:
            string = (
                f'    {opening_bracket}"timestamp": {item.timestamp}, '
                f'"value": {item.value}{closing_bracket},'
            )
            rows.append(string)

        rows.append("]")

        return "\n".join(rows)
