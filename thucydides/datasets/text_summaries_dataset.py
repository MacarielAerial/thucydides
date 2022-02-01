from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

from dataclasses_json import dataclass_json

log = logging.getLogger(__name__)


class TextSummariesDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def save(self, text_summaries: TextSummaries) -> None:
        self._save(filepath=self.filepath, text_summaries=text_summaries)

    @staticmethod
    def _save(filepath: Path, text_summaries: TextSummaries) -> None:
        with open(filepath, "w") as f:
            data = text_summaries.to_dict()  # type: ignore
            json.dump(data, f)

            log.info(f"Saved a {type(text_summaries)} object from {filepath}")

    def load(self) -> TextSummaries:
        return self._load(filepath=self.filepath)

    @staticmethod
    def _load(filepath: Path) -> TextSummaries:
        with open(filepath, "r") as f:
            data = json.load(f)
            text_summaries = TextSummaries.from_dict(data)  # type: ignore

            log.info(f"Loaded a {type(text_summaries)} object from {filepath}")

            return text_summaries  # type: ignore[no-any-return]


@dataclass_json
@dataclass
class TextSummary:
    id: str  # Foreign key to access the summary's corresponding text
    summary: str


@dataclass_json
@dataclass
class TextSummaries:
    list_text_summary: List[TextSummary]
