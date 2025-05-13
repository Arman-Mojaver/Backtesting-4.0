from __future__ import annotations

from models.signals import SignalGroup
from testing_utils.finance_utils.utils import get_lists_evenly_spaced_samples


class SignalGroupFactory:
    INDICATOR_ID_GAP = 400

    def __init__(self, dates: tuple[int], count: int, sample_count: int):
        self.dates: tuple[int] = dates
        self.count: int = count
        self.sample_count: int = sample_count

        self.signal_groups = self._generate_signal_groups()

    def _generate_signal_groups(self):
        signal_groups = []
        for _ in range(self.count):
            long_signals, short_signals = get_lists_evenly_spaced_samples(
                self.dates,
                int(self.sample_count / 2),
                int(self.sample_count / 2),
            )
            signal_group = SignalGroup(
                long_signals=long_signals,
                short_signals=short_signals,
            )
            signal_groups.append(signal_group)

        return signal_groups

    def to_request_format(self) -> dict[int, dict[str, list[int]]]:
        return {
            index + self.INDICATOR_ID_GAP: signal_group.to_request_format()
            for index, signal_group in enumerate(self.signal_groups)
        }
