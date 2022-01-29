import json
from pathlib import Path
from typing import Any, Dict, List

from tests.data.data_registry import (
    PATH_NEWS_JSONL,
    PATH_NEWS_JSONL_OUTPUT,
    PATH_NEWS_JSONL_UNTYPED,
)
from thucydides.datasets.news_jsonl_dataset import NewsJSONL, NewsJSONLDataSet


def create_news_jsonl_from_news_jsonl_untypd(
    path_news_jsonl_untyped: Path,
) -> NewsJSONL:
    with open(path_news_jsonl_untyped, "r") as f:
        news_jsonl_untyped: List[Dict[str, Any]] = []
        for jline in f.readlines():
            news_jsonl_untyped.append(json.loads(jline))

        news_jsonl = NewsJSONL.from_news_jsonl_untyped(
            news_jsonl_untyped=news_jsonl_untyped
        )

        return news_jsonl


def test_from_news_jsonl_untyped() -> None:
    news_jsonl = create_news_jsonl_from_news_jsonl_untypd(
        path_news_jsonl_untyped=PATH_NEWS_JSONL_UNTYPED
    )

    assert len(news_jsonl.list_news_json) > 0


def test_news_jsonl_dataset_save() -> None:
    if PATH_NEWS_JSONL_OUTPUT.is_file():
        PATH_NEWS_JSONL_OUTPUT.unlink()

    news_jsonl = create_news_jsonl_from_news_jsonl_untypd(
        path_news_jsonl_untyped=PATH_NEWS_JSONL_UNTYPED
    )
    news_jsonl_dataset = NewsJSONLDataSet(filepath=PATH_NEWS_JSONL_OUTPUT)
    news_jsonl_dataset.save(news_jsonl=news_jsonl)

    assert PATH_NEWS_JSONL_OUTPUT.is_file()


def test_news_jsonl_dataset_load() -> None:
    news_jsonl_dataset = NewsJSONLDataSet(filepath=PATH_NEWS_JSONL)
    news_jsonl = news_jsonl_dataset.load()

    assert len(news_jsonl.list_news_json) > 0
