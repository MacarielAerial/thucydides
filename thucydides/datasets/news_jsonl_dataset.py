from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from dataclasses_json import dataclass_json

log = logging.getLogger(__name__)


class NewsJSONLDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def load(self) -> NewsJSONL:
        self._check_file_exist(filepath=self.filepath)
        return self._load(filepath=self.filepath)

    @staticmethod
    def _load(filepath: Path) -> NewsJSONL:
        with open(filepath, "r") as f:
            data = json.load(f)
            news_jsonl = NewsJSONL.from_dict(data)  # type: ignore

            log.info(f"Loaded a {NewsJSONL.__class__} object from {filepath}")

            return news_jsonl  # type: ignore

    def save(self, news_jsonl: NewsJSONL) -> None:
        self._save(filepath=self.filepath, news_jsonl=news_jsonl)

    @staticmethod
    def _save(filepath: Path, news_jsonl: NewsJSONL) -> None:
        with open(filepath, "w") as f:
            data = news_jsonl.to_dict()  # type: ignore
            json.dump(data, f)

            log.info(f"Saved a {NewsJSONL.__class__} object to {filepath}")


@dataclass_json
@dataclass
class NewsJSON:
    id: str
    source: str
    publish_date: str
    title: str
    body: str


@dataclass_json
@dataclass
class NewsJSONL:
    list_news_json: List[NewsJSON]

    @classmethod
    def from_news_jsonl_untyped(
        cls, news_jsonl_untyped: List[Dict[str, Any]]
    ) -> NewsJSONL:
        """Constructs the dataclass from
        a list of arbitrary dictionaries loaded from a jsonl file"""
        # Initiate the result object
        news_jsonl = NewsJSONL(list_news_json=[])

        # Iterate over the list of dictionaries to construct NewsJSON objects
        for news_json_untyped in news_jsonl_untyped:
            news_json = NewsJSON(
                id=news_json_untyped["id"],
                source=news_json_untyped["source"],
                publish_date=news_json_untyped["publishDate"],
                title=news_json_untyped["title"],
                body=news_json_untyped["body"],
            )
            news_jsonl.list_news_json.append(news_json)

        log.info(
            f"Initiated a {NewsJSONL.__class__} object with "
            f"{len(news_jsonl.list_news_json)} {NewsJSON.__class__} objects "
            f"from a list of dictionaries loaded from a jsonl file"
        )

        return news_jsonl
