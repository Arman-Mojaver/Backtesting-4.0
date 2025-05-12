from database.models.indicator import IndicatorList


def test_to_request_format(indicator, indicator_2, indicator_data, indicator_data_2):
    assert IndicatorList([indicator, indicator_2]).to_request_format() == [
        {"id": indicator.id, **indicator_data},
        {"id": indicator_2.id, **indicator_data_2},
    ]
