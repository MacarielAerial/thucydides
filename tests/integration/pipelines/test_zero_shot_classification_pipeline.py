from tests.data.data_registry import (
    PATH_NEWS_JSONL_UNTYPED_ZC,
    PATH_PANDAS_JSON_ZC_OUTPUT,
)
from thucydides.pipelines.zero_shot_classification_pipeline import (
    zero_shot_classification_pipeline,
)


def test_zero_shot_classification_pipeline() -> None:
    if PATH_PANDAS_JSON_ZC_OUTPUT.is_file():
        PATH_PANDAS_JSON_ZC_OUTPUT.unlink()

    zero_shot_classification_pipeline(
        path_news_jsonl_untyped=PATH_NEWS_JSONL_UNTYPED_ZC,
        path_pandas_json=PATH_PANDAS_JSON_ZC_OUTPUT,
    )

    assert PATH_PANDAS_JSON_ZC_OUTPUT.is_file()
