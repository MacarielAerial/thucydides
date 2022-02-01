import logging
from pathlib import Path

import pandas as pd
from pandas import DataFrame

log = logging.getLogger(__name__)


class PandasJsonDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def load(self) -> DataFrame:  # type: ignore
        self._check_file_exist(filepath=self.filepath)

        return self._load(filepath=self.filepath)

    @staticmethod
    def _load(filepath: Path) -> DataFrame:  # type: ignore
        with open(filepath, "r") as f:
            df = pd.read_json(f)

            log.info(f"Loaded a {type(df)} object from {filepath}")

            return df

    def save(self, df: DataFrame) -> None:  # type: ignore
        self._save(filepath=self.filepath, df=df)

    @staticmethod
    def _save(filepath: Path, df: DataFrame) -> None:  # type: ignore
        df.to_json(filepath)

        log.info(f"Saved a {type(df)} object to {filepath}")
