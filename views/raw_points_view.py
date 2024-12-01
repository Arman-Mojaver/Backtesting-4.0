from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from config import config  # type: ignore[attr-defined]
from database import session
from database.models import RawPointD1, RawPointH1
from schemas.instruments_schema import InstrumentsSchema


class RawPointsCreateMultipleView:
    def __init__(self):
        self.directory: Path = Path(Path.cwd()) / config.INSTRUMENT_DATA_PATH
        self.file_names: list[Path] = self._get_file_names()
        self.data: dict[str, Any] = {}
        self.instruments_data: InstrumentsSchema = InstrumentsSchema()

    def run(self) -> None:
        self._validate_file_names()
        self.data = self._get_file_data()
        self.instruments_data = self._get_instrument_data()
        self.instruments_data.validate_instruments_enabled(
            enabled_instruments=config.ENABLED_INSTRUMENTS,
        )
        self._create_raw_d1_points()
        self._create_raw_h1_points()
        self._commit()

    def _get_file_names(self) -> list[Path]:
        files_names = [
            file
            for file in self.directory.iterdir()
            if str(file).endswith("_instrument_data.json")
        ]
        return sorted(files_names, key=lambda x: x.name, reverse=True)

    def _validate_file_names(self) -> None:
        if not self.file_names:
            err = f"Directory <{self.directory!s}> did not have instrument_data files"
            raise FileNotFoundError(err)

    def _get_file_data(self) -> dict[str, Any]:
        file = self.file_names[0]
        with file.open() as f:
            return json.load(f)

    def _get_instrument_data(self):
        try:
            return InstrumentsSchema(**self.data)
        except ValidationError:
            raise

    def _create_raw_d1_points(self):
        for raw_point_d1_data in self.instruments_data.raw_points_d1():
            raw_point_d1 = RawPointD1(**raw_point_d1_data.model_dump())
            session.add(raw_point_d1)

    def _create_raw_h1_points(self):
        for raw_point_h1_data in self.instruments_data.raw_points_h1():
            raw_point_h1 = RawPointH1(**raw_point_h1_data.model_dump())
            session.add(raw_point_h1)

    @staticmethod
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()
