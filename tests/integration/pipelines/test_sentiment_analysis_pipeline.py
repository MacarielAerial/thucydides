from tests.data.data_registry import (
    PATH_NEWS_JSONL_UNTYPED_SA,
    PATH_PANDAS_JSON_SA_OUTPUT,
)
from thucydides.pipelines.sentiment_analysis_pipeline import sentiment_analysis_pipeline


def test_sentiment_analysis_pipeline() -> None:
    if PATH_PANDAS_JSON_SA_OUTPUT.is_file():
        PATH_PANDAS_JSON_SA_OUTPUT.unlink()

    sentiment_analysis_pipeline(
        path_news_jsonl_untyped=PATH_NEWS_JSONL_UNTYPED_SA,
        path_pandas_json=PATH_PANDAS_JSON_SA_OUTPUT,
    )

    assert PATH_PANDAS_JSON_SA_OUTPUT.is_file()
