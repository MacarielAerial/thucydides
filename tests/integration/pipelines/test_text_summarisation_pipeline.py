from tests.data.data_registry import (
    PATH_NEWS_JSONL_UNTYPED_TS,
    PATH_TEXT_SUMMARIES_TS_OUTPUT,
)
from thucydides.pipelines.text_summarisation_pipeline import text_summarisation_pipeline


def test_sentiment_analysis_pipeline() -> None:
    if PATH_TEXT_SUMMARIES_TS_OUTPUT.is_file():
        PATH_TEXT_SUMMARIES_TS_OUTPUT.unlink()

    text_summarisation_pipeline(
        path_news_jsonl_untyped=PATH_NEWS_JSONL_UNTYPED_TS,
        path_text_summaries=PATH_TEXT_SUMMARIES_TS_OUTPUT,
    )

    assert PATH_TEXT_SUMMARIES_TS_OUTPUT
