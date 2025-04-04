from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import config


class LoadFileData:
    def __init__(self):
        self.directory: Path = Path(Path.cwd()) / config.INSTRUMENT_DATA_PATH

    def _get_file_names(self) -> list[Path]:
        files_names = [
            file
            for file in self.directory.iterdir()
            if str(file).endswith("_instrument_data.json")
        ]
        return sorted(files_names, key=lambda x: x.name, reverse=True)

    def _validate_file_names(self, file_names: list[Path]) -> None:
        if not file_names:
            err = f"Directory <{self.directory!s}> did not have instrument_data files"
            raise FileNotFoundError(err)

    @staticmethod
    def _get_file_data(file: Path) -> dict[str, Any]:
        with file.open() as f:
            return json.load(f)

    def run(self) -> dict[str, Any]:
        file_names = self._get_file_names()
        self._validate_file_names(file_names)
        return self._get_file_data(file_names[0])
