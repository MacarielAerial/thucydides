from tests.data.data_registry import (
    PATH_NEWS_JSON_UNTYPED_1,
    PATH_NEWS_JSON_UNTYPED_2,
    PATH_NEWS_JSONL_UNTYPED_OUTPUT,
)
from thucydides.nodes.io import jsons_to_jsonl


def test_jsons_to_jsonl() -> None:
    if PATH_NEWS_JSONL_UNTYPED_OUTPUT.is_file():
        PATH_NEWS_JSONL_UNTYPED_OUTPUT.unlink()  # Remove existing output file if any

    jsons_to_jsonl(
        paths_json=[PATH_NEWS_JSON_UNTYPED_1, PATH_NEWS_JSON_UNTYPED_2],
        path_jsonl=PATH_NEWS_JSONL_UNTYPED_OUTPUT,
    )

    assert PATH_NEWS_JSONL_UNTYPED_OUTPUT.is_file()
