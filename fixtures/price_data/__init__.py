from __future__ import annotations

from typing import TYPE_CHECKING, Any

from config import config  # type: ignore[attr-defined]
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame

if TYPE_CHECKING:
    from datetime import datetime

from .AUDCAD import AUDCAD_D1_RATES, AUDCAD_H1_RATES
from .AUDCHF import AUDCHF_D1_RATES, AUDCHF_H1_RATES
from .AUDJPY import AUDJPY_D1_RATES, AUDJPY_H1_RATES
from .AUDNZD import AUDNZD_D1_RATES, AUDNZD_H1_RATES
from .AUDUSD import AUDUSD_D1_RATES, AUDUSD_H1_RATES
from .CADCHF import CADCHF_D1_RATES, CADCHF_H1_RATES
from .CADJPY import CADJPY_D1_RATES, CADJPY_H1_RATES
from .CHFJPY import CHFJPY_D1_RATES, CHFJPY_H1_RATES
from .EURAUD import EURAUD_D1_RATES, EURAUD_H1_RATES
from .EURCAD import EURCAD_D1_RATES, EURCAD_H1_RATES
from .EURGBP import EURGBP_D1_RATES, EURGBP_H1_RATES
from .EURJPY import EURJPY_D1_RATES, EURJPY_H1_RATES
from .EURNZD import EURNZD_D1_RATES, EURNZD_H1_RATES
from .EURUSD import EURUSD_D1_RATES, EURUSD_H1_RATES
from .GBPAUD import GBPAUD_D1_RATES, GBPAUD_H1_RATES
from .GBPCAD import GBPCAD_D1_RATES, GBPCAD_H1_RATES
from .GBPCHF import GBPCHF_D1_RATES, GBPCHF_H1_RATES
from .GBPJPY import GBPJPY_D1_RATES, GBPJPY_H1_RATES
from .GBPUSD import GBPUSD_D1_RATES, GBPUSD_H1_RATES
from .NZDCAD import NZDCAD_D1_RATES, NZDCAD_H1_RATES
from .NZDCHF import NZDCHF_D1_RATES, NZDCHF_H1_RATES
from .NZDJPY import NZDJPY_D1_RATES, NZDJPY_H1_RATES
from .NZDUSD import NZDUSD_D1_RATES, NZDUSD_H1_RATES
from .USDCAD import USDCAD_D1_RATES, USDCAD_H1_RATES
from .USDCHF import USDCHF_D1_RATES, USDCHF_H1_RATES
from .USDJPY import USDJPY_D1_RATES, USDJPY_H1_RATES

INSTRUMENT_MAPPER = {
    "AUDCAD": {TimeFrame.Day: AUDCAD_D1_RATES, TimeFrame.Hour: AUDCAD_H1_RATES},
    "AUDCHF": {TimeFrame.Day: AUDCHF_D1_RATES, TimeFrame.Hour: AUDCHF_H1_RATES},
    "AUDJPY": {TimeFrame.Day: AUDJPY_D1_RATES, TimeFrame.Hour: AUDJPY_H1_RATES},
    "AUDNZD": {TimeFrame.Day: AUDNZD_D1_RATES, TimeFrame.Hour: AUDNZD_H1_RATES},
    "AUDUSD": {TimeFrame.Day: AUDUSD_D1_RATES, TimeFrame.Hour: AUDUSD_H1_RATES},
    "CADCHF": {TimeFrame.Day: CADCHF_D1_RATES, TimeFrame.Hour: CADCHF_H1_RATES},
    "CADJPY": {TimeFrame.Day: CADJPY_D1_RATES, TimeFrame.Hour: CADJPY_H1_RATES},
    "CHFJPY": {TimeFrame.Day: CHFJPY_D1_RATES, TimeFrame.Hour: CHFJPY_H1_RATES},
    "EURAUD": {TimeFrame.Day: EURAUD_D1_RATES, TimeFrame.Hour: EURAUD_H1_RATES},
    "EURCAD": {TimeFrame.Day: EURCAD_D1_RATES, TimeFrame.Hour: EURCAD_H1_RATES},
    "EURGBP": {TimeFrame.Day: EURGBP_D1_RATES, TimeFrame.Hour: EURGBP_H1_RATES},
    "EURJPY": {TimeFrame.Day: EURJPY_D1_RATES, TimeFrame.Hour: EURJPY_H1_RATES},
    "EURNZD": {TimeFrame.Day: EURNZD_D1_RATES, TimeFrame.Hour: EURNZD_H1_RATES},
    "EURUSD": {TimeFrame.Day: EURUSD_D1_RATES, TimeFrame.Hour: EURUSD_H1_RATES},
    "GBPAUD": {TimeFrame.Day: GBPAUD_D1_RATES, TimeFrame.Hour: GBPAUD_H1_RATES},
    "GBPCAD": {TimeFrame.Day: GBPCAD_D1_RATES, TimeFrame.Hour: GBPCAD_H1_RATES},
    "GBPCHF": {TimeFrame.Day: GBPCHF_D1_RATES, TimeFrame.Hour: GBPCHF_H1_RATES},
    "GBPJPY": {TimeFrame.Day: GBPJPY_D1_RATES, TimeFrame.Hour: GBPJPY_H1_RATES},
    "GBPUSD": {TimeFrame.Day: GBPUSD_D1_RATES, TimeFrame.Hour: GBPUSD_H1_RATES},
    "NZDCAD": {TimeFrame.Day: NZDCAD_D1_RATES, TimeFrame.Hour: NZDCAD_H1_RATES},
    "NZDCHF": {TimeFrame.Day: NZDCHF_D1_RATES, TimeFrame.Hour: NZDCHF_H1_RATES},
    "NZDJPY": {TimeFrame.Day: NZDJPY_D1_RATES, TimeFrame.Hour: NZDJPY_H1_RATES},
    "NZDUSD": {TimeFrame.Day: NZDUSD_D1_RATES, TimeFrame.Hour: NZDUSD_H1_RATES},
    "USDCAD": {TimeFrame.Day: USDCAD_D1_RATES, TimeFrame.Hour: USDCAD_H1_RATES},
    "USDCHF": {TimeFrame.Day: USDCHF_D1_RATES, TimeFrame.Hour: USDCHF_H1_RATES},
    "USDJPY": {TimeFrame.Day: USDJPY_D1_RATES, TimeFrame.Hour: USDJPY_H1_RATES},
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
