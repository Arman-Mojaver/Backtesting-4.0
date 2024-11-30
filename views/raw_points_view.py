from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from config import config  # type: ignore[attr-defined]
from schemas.instruments_schema import InstrumentsSchema


class EnabledInstrumentsMismatchError(Exception):
    """
    Error raised when the instruments in the file
    and the enabled instruments do not match.
    """


class RawPointsCreateMultipleView:
    def __init__(self):
        self.directory: Path = Path(Path.cwd()) / config.INSTRUMENT_DATA_PATH
        self.file_names: list[Path] = self._get_file_names()
        self.data: dict[str, Any] = {}
        self.instruments_data: InstrumentsSchema | None = None

    def run(self) -> None:
        self._validate_file_names()
        self.data = self._get_file_data()
        self.instruments_data = self._get_instrument_data()
        self._validate_enabled_instruments()

    def _validate_enabled_instruments(self):
        if set(config.ENABLED_INSTRUMENTS) != set(self.data.keys()):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{config.ENABLED_INSTRUMENTS=}, {self.data.keys()=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def _get_instrument_data(self):
        try:
            return InstrumentsSchema(**self.data)
        except ValidationError:
            raise

    def _get_file_data(self) -> dict[str, Any]:
        file = self.file_names[0]
        with file.open() as f:
            return json.load(f)

    def _validate_file_names(self) -> None:
        if not self.file_names:
            err = f"Directory <{self.directory!s}> did not have instrument_data files"
            raise FileNotFoundError(err)

    def _get_file_names(self) -> list[Path]:
        files_names = [
            file
            for file in self.directory.iterdir()
            if str(file).endswith("_instrument_data.json")
        ]
        return sorted(files_names, key=lambda x: x.name, reverse=True)
