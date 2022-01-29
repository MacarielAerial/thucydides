from pathlib import Path

# Raw
PATH_NEWS_JSON_UNTYPED_1: Path = Path("tests") / "data" / "unit" / "a-52104029.json"
PATH_NEWS_JSON_UNTYPED_2: Path = Path("tests") / "data" / "unit" / "a-67488720.json"

# news_jsonl_untyped
PATH_NEWS_JSONL_UNTYPED: Path = (
    Path("tests") / "data" / "unit" / "news_jsonl_untyped.jsonl"
)
PATH_NEWS_JSONL_UNTYPED_OUTPUT: Path = (
    Path("tests") / "data" / "output" / "news_jsonl_untyped.jsonl"
)

# NewsJSONL
PATH_NEWS_JSONL_OUTPUT: Path = Path("tests") / "data" / "output" / "news_jsonl.json"
PATH_NEWS_JSONL: Path = Path("tests") / "data" / "unit" / "news_jsonl.json"
