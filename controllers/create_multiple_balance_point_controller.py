from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from config.logging_config.log_decorators import log_on_end
from database.models.resasmpled_point_d1 import HighLowOrder

if TYPE_CHECKING:
    from datetime import date

    from database.models import ResampledPointD1


class BalancePointCreateMultipleController:
    def __init__(self, resampled_points: list[ResampledPointD1]):
        self.resampled_points: list[ResampledPointD1] = resampled_points

    @log_on_end("Creating Balance Points")
    def run(
        self,
    ) -> tuple[dict[date, list[int]], dict[date, list[int]]]:
        open_values = self._get_open_values()
        high_low_values = self._get_high_low_values()
        long_balance_list = self._get_long_balance_list(
            high_low_values,
            open_values,
        )

        return self._get_balance_points_by_date(long_balance_list)

    def _get_balance_points_by_date(
        self,
        long_balance_list,  # noqa: ANN001
    ) -> tuple[dict[date, list[int]], dict[date, list[int]]]:
        long_balance_points_by_date, short_balance_points_by_date = {}, {}
        for point_index, point in enumerate(self.resampled_points):
            long_balance = [
                int(value)
                for value in long_balance_list[point_index]
                if not np.isnan(value)
            ]
            short_balance = [-i for i in long_balance]

            long_balance_points_by_date[point.datetime] = long_balance
            short_balance_points_by_date[point.datetime] = short_balance
        return long_balance_points_by_date, short_balance_points_by_date

    @staticmethod
    def _get_long_balance_list(  # noqa: ANN205
        high_low_values,  # noqa: ANN001
        open_values,  # noqa: ANN001
    ):
        col, row = np.meshgrid(
            np.arange(len(open_values)), np.arange(len(high_low_values))
        )
        mask = row >= 2 * col
        matrix = np.where(
            mask, np.round(10000 * (high_low_values[:, None] - open_values), 0), np.nan
        )
        return matrix.T.tolist()

    def _get_high_low_values(self):
        high_low_list = []
        for point in self.resampled_points:
            if self._is_high_or_undefined(point):
                high_low_list.append(point.high)
                high_low_list.append(point.low)
            else:
                high_low_list.append(point.low)
                high_low_list.append(point.high)
        return np.array(high_low_list)

    def _get_open_values(self):
        return np.array([point.open for point in self.resampled_points])

    @staticmethod
    def _is_high_or_undefined(point: ResampledPointD1) -> bool:
        return point.high_low_order in {HighLowOrder.high_first, HighLowOrder.undefined}
