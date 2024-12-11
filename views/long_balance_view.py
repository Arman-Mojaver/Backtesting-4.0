from __future__ import annotations

from config import config  # type: ignore[attr-defined]
from database.models import ResampledPointD1
from database.models.resasmpled_point_d1 import HighLowOrder
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from utils.date_utils import datetime_to_string


class NoResampledPointsError(Exception):
    pass


class LongBalanceView:
    def __init__(self):
        self.resampled_points = ResampledPointD1.query.all()

    def run(self) -> dict[str, dict[str, list[float]]]:
        self._validate_resampled_points_exist()
        self._validate_instruments_enabled()
        return self._get_long_balance_by_instrument()

    def _validate_resampled_points_exist(self):
        if not self.resampled_points:
            err = "No resampled points in db"
            raise NoResampledPointsError(err)

    def _validate_instruments_enabled(self):
        instruments = {point.instrument for point in self.resampled_points}
        if set(config.ENABLED_INSTRUMENTS) != set(instruments):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{config.ENABLED_INSTRUMENTS=}, {instruments=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def _get_long_balance_by_instrument(self) -> dict[str, dict[str, list[float]]]:
        resampled_points_by_instrument = ResampledPointD1.query.dict_multi_by_key(
            "instrument"
        )
        long_balance_by_instrument = {}
        for instrument, resampled_points in resampled_points_by_instrument.items():
            long_balance_by_instrument[instrument] = self._calculate_long_balance_by_date(
                resampled_points
            )
        return long_balance_by_instrument

    def _calculate_long_balance_by_date(
        self,
        resampled_points: list[ResampledPointD1],
    ) -> dict[str, list[float]]:
        long_balance_by_date: dict[str, list[float]] = {}
        for open_point_index, open_point in enumerate(resampled_points):
            long_balance: list[float] = []
            for high_low_point in resampled_points[open_point_index:]:
                if self._is_high_or_undefined(point=high_low_point):
                    self._high_first(
                        open_point=open_point,
                        high_low_point=high_low_point,
                        long_balance=long_balance,
                    )
                else:
                    self._low_first(
                        open_point=open_point,
                        high_low_point=high_low_point,
                        long_balance=long_balance,
                    )

            long_balance_by_date[datetime_to_string(open_point.datetime)] = long_balance

        return long_balance_by_date

    @staticmethod
    def _is_high_or_undefined(point: ResampledPointD1) -> bool:
        return point.high_low_order in {HighLowOrder.high_first, HighLowOrder.undefined}

    @staticmethod
    def _low_first(
        open_point: ResampledPointD1,
        high_low_point: ResampledPointD1,
        long_balance: list[float],
    ) -> None:
        long_balance.append(-open_point.open + high_low_point.low)
        long_balance.append(-open_point.open + high_low_point.high)

    @staticmethod
    def _high_first(
        open_point: ResampledPointD1,
        high_low_point: ResampledPointD1,
        long_balance: list[float],
    ) -> None:
        long_balance.append(-open_point.open + high_low_point.high)
        long_balance.append(-open_point.open + high_low_point.low)
