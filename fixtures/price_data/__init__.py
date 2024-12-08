from __future__ import annotations

from typing import TYPE_CHECKING, Any

from config import config  # type: ignore[attr-defined]
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame

if TYPE_CHECKING:
    from datetime import datetime

from .AUDCAD import AUDCAD_D1_RATES, AUDCAD_H1_RATES, AUDCAD_RESAMPLED_D1_POINTS
from .AUDCHF import AUDCHF_D1_RATES, AUDCHF_H1_RATES, AUDCHF_RESAMPLED_D1_POINTS
from .AUDJPY import AUDJPY_D1_RATES, AUDJPY_H1_RATES, AUDJPY_RESAMPLED_D1_POINTS
from .AUDNZD import AUDNZD_D1_RATES, AUDNZD_H1_RATES, AUDNZD_RESAMPLED_D1_POINTS
from .AUDUSD import AUDUSD_D1_RATES, AUDUSD_H1_RATES, AUDUSD_RESAMPLED_D1_POINTS
from .CADCHF import CADCHF_D1_RATES, CADCHF_H1_RATES, CADCHF_RESAMPLED_D1_POINTS
from .CADJPY import CADJPY_D1_RATES, CADJPY_H1_RATES, CADJPY_RESAMPLED_D1_POINTS
from .CHFJPY import CHFJPY_D1_RATES, CHFJPY_H1_RATES, CHFJPY_RESAMPLED_D1_POINTS
from .EURAUD import EURAUD_D1_RATES, EURAUD_H1_RATES, EURAUD_RESAMPLED_D1_POINTS
from .EURCAD import EURCAD_D1_RATES, EURCAD_H1_RATES, EURCAD_RESAMPLED_D1_POINTS
from .EURGBP import EURGBP_D1_RATES, EURGBP_H1_RATES, EURGBP_RESAMPLED_D1_POINTS
from .EURJPY import EURJPY_D1_RATES, EURJPY_H1_RATES, EURJPY_RESAMPLED_D1_POINTS
from .EURNZD import EURNZD_D1_RATES, EURNZD_H1_RATES, EURNZD_RESAMPLED_D1_POINTS
from .EURUSD import EURUSD_D1_RATES, EURUSD_H1_RATES, EURUSD_RESAMPLED_D1_POINTS
from .GBPAUD import GBPAUD_D1_RATES, GBPAUD_H1_RATES, GBPAUD_RESAMPLED_D1_POINTS
from .GBPCAD import GBPCAD_D1_RATES, GBPCAD_H1_RATES, GBPCAD_RESAMPLED_D1_POINTS
from .GBPCHF import GBPCHF_D1_RATES, GBPCHF_H1_RATES, GBPCHF_RESAMPLED_D1_POINTS
from .GBPJPY import GBPJPY_D1_RATES, GBPJPY_H1_RATES, GBPJPY_RESAMPLED_D1_POINTS
from .GBPUSD import GBPUSD_D1_RATES, GBPUSD_H1_RATES, GBPUSD_RESAMPLED_D1_POINTS
from .NZDCAD import NZDCAD_D1_RATES, NZDCAD_H1_RATES, NZDCAD_RESAMPLED_D1_POINTS
from .NZDCHF import NZDCHF_D1_RATES, NZDCHF_H1_RATES, NZDCHF_RESAMPLED_D1_POINTS
from .NZDJPY import NZDJPY_D1_RATES, NZDJPY_H1_RATES, NZDJPY_RESAMPLED_D1_POINTS
from .NZDUSD import NZDUSD_D1_RATES, NZDUSD_H1_RATES, NZDUSD_RESAMPLED_D1_POINTS
from .USDCAD import USDCAD_D1_RATES, USDCAD_H1_RATES, USDCAD_RESAMPLED_D1_POINTS
from .USDCHF import USDCHF_D1_RATES, USDCHF_H1_RATES, USDCHF_RESAMPLED_D1_POINTS
from .USDJPY import USDJPY_D1_RATES, USDJPY_H1_RATES, USDJPY_RESAMPLED_D1_POINTS

INSTRUMENT_MAPPER = {
    "AUDCAD": {
        TimeFrame.Day: AUDCAD_D1_RATES,
        TimeFrame.Hour: AUDCAD_H1_RATES,
        "resampled_d1": AUDCAD_RESAMPLED_D1_POINTS,
    },
    "AUDCHF": {
        TimeFrame.Day: AUDCHF_D1_RATES,
        TimeFrame.Hour: AUDCHF_H1_RATES,
        "resampled_d1": AUDCHF_RESAMPLED_D1_POINTS,
    },
    "AUDJPY": {
        TimeFrame.Day: AUDJPY_D1_RATES,
        TimeFrame.Hour: AUDJPY_H1_RATES,
        "resampled_d1": AUDJPY_RESAMPLED_D1_POINTS,
    },
    "AUDNZD": {
        TimeFrame.Day: AUDNZD_D1_RATES,
        TimeFrame.Hour: AUDNZD_H1_RATES,
        "resampled_d1": AUDNZD_RESAMPLED_D1_POINTS,
    },
    "AUDUSD": {
        TimeFrame.Day: AUDUSD_D1_RATES,
        TimeFrame.Hour: AUDUSD_H1_RATES,
        "resampled_d1": AUDUSD_RESAMPLED_D1_POINTS,
    },
    "CADCHF": {
        TimeFrame.Day: CADCHF_D1_RATES,
        TimeFrame.Hour: CADCHF_H1_RATES,
        "resampled_d1": CADCHF_RESAMPLED_D1_POINTS,
    },
    "CADJPY": {
        TimeFrame.Day: CADJPY_D1_RATES,
        TimeFrame.Hour: CADJPY_H1_RATES,
        "resampled_d1": CADJPY_RESAMPLED_D1_POINTS,
    },
    "CHFJPY": {
        TimeFrame.Day: CHFJPY_D1_RATES,
        TimeFrame.Hour: CHFJPY_H1_RATES,
        "resampled_d1": CHFJPY_RESAMPLED_D1_POINTS,
    },
    "EURAUD": {
        TimeFrame.Day: EURAUD_D1_RATES,
        TimeFrame.Hour: EURAUD_H1_RATES,
        "resampled_d1": EURAUD_RESAMPLED_D1_POINTS,
    },
    "EURCAD": {
        TimeFrame.Day: EURCAD_D1_RATES,
        TimeFrame.Hour: EURCAD_H1_RATES,
        "resampled_d1": EURCAD_RESAMPLED_D1_POINTS,
    },
    "EURGBP": {
        TimeFrame.Day: EURGBP_D1_RATES,
        TimeFrame.Hour: EURGBP_H1_RATES,
        "resampled_d1": EURGBP_RESAMPLED_D1_POINTS,
    },
    "EURJPY": {
        TimeFrame.Day: EURJPY_D1_RATES,
        TimeFrame.Hour: EURJPY_H1_RATES,
        "resampled_d1": EURJPY_RESAMPLED_D1_POINTS,
    },
    "EURNZD": {
        TimeFrame.Day: EURNZD_D1_RATES,
        TimeFrame.Hour: EURNZD_H1_RATES,
        "resampled_d1": EURNZD_RESAMPLED_D1_POINTS,
    },
    "EURUSD": {
        TimeFrame.Day: EURUSD_D1_RATES,
        TimeFrame.Hour: EURUSD_H1_RATES,
        "resampled_d1": EURUSD_RESAMPLED_D1_POINTS,
    },
    "GBPAUD": {
        TimeFrame.Day: GBPAUD_D1_RATES,
        TimeFrame.Hour: GBPAUD_H1_RATES,
        "resampled_d1": GBPAUD_RESAMPLED_D1_POINTS,
    },
    "GBPCAD": {
        TimeFrame.Day: GBPCAD_D1_RATES,
        TimeFrame.Hour: GBPCAD_H1_RATES,
        "resampled_d1": GBPCAD_RESAMPLED_D1_POINTS,
    },
    "GBPCHF": {
        TimeFrame.Day: GBPCHF_D1_RATES,
        TimeFrame.Hour: GBPCHF_H1_RATES,
        "resampled_d1": GBPCHF_RESAMPLED_D1_POINTS,
    },
    "GBPJPY": {
        TimeFrame.Day: GBPJPY_D1_RATES,
        TimeFrame.Hour: GBPJPY_H1_RATES,
        "resampled_d1": GBPJPY_RESAMPLED_D1_POINTS,
    },
    "GBPUSD": {
        TimeFrame.Day: GBPUSD_D1_RATES,
        TimeFrame.Hour: GBPUSD_H1_RATES,
        "resampled_d1": GBPUSD_RESAMPLED_D1_POINTS,
    },
    "NZDCAD": {
        TimeFrame.Day: NZDCAD_D1_RATES,
        TimeFrame.Hour: NZDCAD_H1_RATES,
        "resampled_d1": NZDCAD_RESAMPLED_D1_POINTS,
    },
    "NZDCHF": {
        TimeFrame.Day: NZDCHF_D1_RATES,
        TimeFrame.Hour: NZDCHF_H1_RATES,
        "resampled_d1": NZDCHF_RESAMPLED_D1_POINTS,
    },
    "NZDJPY": {
        TimeFrame.Day: NZDJPY_D1_RATES,
        TimeFrame.Hour: NZDJPY_H1_RATES,
        "resampled_d1": NZDJPY_RESAMPLED_D1_POINTS,
    },
    "NZDUSD": {
        TimeFrame.Day: NZDUSD_D1_RATES,
        TimeFrame.Hour: NZDUSD_H1_RATES,
        "resampled_d1": NZDUSD_RESAMPLED_D1_POINTS,
    },
    "USDCAD": {
        TimeFrame.Day: USDCAD_D1_RATES,
        TimeFrame.Hour: USDCAD_H1_RATES,
        "resampled_d1": USDCAD_RESAMPLED_D1_POINTS,
    },
    "USDCHF": {
        TimeFrame.Day: USDCHF_D1_RATES,
        TimeFrame.Hour: USDCHF_H1_RATES,
        "resampled_d1": USDCHF_RESAMPLED_D1_POINTS,
    },
    "USDJPY": {
        TimeFrame.Day: USDJPY_D1_RATES,
        TimeFrame.Hour: USDJPY_H1_RATES,
        "resampled_d1": USDJPY_RESAMPLED_D1_POINTS,
    },
}


FORMAT_MAPPER = {
    TimeFrame.Day: config.DATE_FORMAT,
    TimeFrame.Hour: config.DATETIME_FORMAT,
}


def get_points_data(
    instrument: str,
    time_frame: TimeFrame,
    from_date: datetime,
    to_date: datetime,
) -> list[dict[str, Any]]:
    rates = INSTRUMENT_MAPPER[instrument][time_frame]
    sorted_dates = sorted(rates.keys())

    data = []
    for date in sorted_dates:
        data_obj = string_to_datetime(date, format=FORMAT_MAPPER[time_frame])
        if from_date > data_obj or data_obj > to_date:
            continue

        open_, high, low, close, volume = rates[date][1:6]

        point_data = {
            "instrument": instrument,
            "datetime": date,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
        data.append(point_data)

    return data


def get_resampled_d1_data(
    instrument: str,
    from_date: datetime,
    to_date: datetime,
) -> list[dict[str, Any]]:
    points = INSTRUMENT_MAPPER[instrument]["resampled_d1"]
    sorted_dates = sorted(points.keys())

    data = []
    for date in sorted_dates:
        data_obj = string_to_datetime(date)
        if from_date > data_obj or data_obj > to_date:
            continue

        point_data = points[date]
        data.append(point_data)

    return data
