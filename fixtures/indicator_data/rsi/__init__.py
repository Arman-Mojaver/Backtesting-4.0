from fixtures.indicator_data.rsi import (
    AUDCAD_n3,
    AUDCAD_n4,
    AUDUSD_n3,
    AUDUSD_n4,
    EURUSD_n3,
    EURUSD_n4,
    USDCAD_n3,
    USDCAD_n4,
)

rsi_map = {
    "AUDCAD": {
        "n3": {
            "b0": AUDCAD_n3.b0,
        },
        "n4": {
            "b0": AUDCAD_n4.b0,
        },
    },
    "AUDUSD": {
        "n3": {
            "b0": AUDUSD_n3.b0,
        },
        "n4": {
            "b0": AUDUSD_n4.b0,
        },
    },
    "EURUSD": {
        "n3": {
            "b0": EURUSD_n3.b0,
        },
        "n4": {
            "b0": EURUSD_n4.b0,
        },
    },
    "USDCAD": {
        "n3": {
            "b0": USDCAD_n3.b0,
        },
        "n4": {
            "b0": USDCAD_n4.b0,
        },
    },
}
