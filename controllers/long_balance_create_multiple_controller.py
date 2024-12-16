from __future__ import annotations

from config import config  # type: ignore[attr-defined]
from database.models import ResampledPointD1
from database.models.resasmpled_point_d1 import HighLowOrder
from models.long_balance_point import LongBalancePoint
from schemas.instruments_schema import EnabledInstrumentsMismatchError


class NoResampledPointsError(Exception):
    pass


class LongBalanceCreateMultipleController:
    def __init__(self):
        self.resampled_points_by_instrument = ResampledPointD1.query.dict_multi_by_key(
            "instrument"
        )

    def run(self) -> list[LongBalancePoint]:
        self._validate_resampled_points_exist()
        self._validate_instruments_enabled()
        return self._get_long_balance_points()

    def _validate_resampled_points_exist(self):
        if not self.resampled_points_by_instrument:
            err = "No resampled points in db"
            raise NoResampledPointsError(err)

    def _validate_instruments_enabled(self):
        instruments = self.resampled_points_by_instrument.keys()
        if set(config.ENABLED_INSTRUMENTS) != set(instruments):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{config.ENABLED_INSTRUMENTS=}, {instruments=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def _get_long_balance_points(self):
        long_balance_points = []
        for resampled_points in self.resampled_points_by_instrument.values():
            for open_point_index, open_point in enumerate(resampled_points):
                long_balance = self._generate_long_balance(
                    open_point_index=open_point_index,
                    open_point=open_point,
                    resampled_points=resampled_points,
                )

                long_balance_point = LongBalancePoint(
                    instrument=open_point.instrument,
                    datetime=open_point.datetime,
                    balance=long_balance,
                )

                long_balance_points.append(long_balance_point)
        return long_balance_points

    def _generate_long_balance(
        self,
        open_point_index: int,
        open_point: ResampledPointD1,
        resampled_points: list[ResampledPointD1],
    ):
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
        return long_balance

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
