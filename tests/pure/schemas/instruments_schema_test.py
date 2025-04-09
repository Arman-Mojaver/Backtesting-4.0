from schemas.instruments_schema import InstrumentsSchema


def test_valid_instruments_schema(file_data):
    instruments_data = InstrumentsSchema(**file_data)

    assert instruments_data.model_dump() == file_data
