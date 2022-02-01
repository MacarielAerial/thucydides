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
PATH_NEWS_JSONL_UNTYPED_SA: Path = (
    Path("tests")
    / "data"
    / "integration"
    / "pipelines"
    / "sentiment_analysis_pipeline"
    / "news_jsonl_untyped_first_10.jsonl"
)
PATH_NEWS_JSONL_UNTYPED_TS: Path = PATH_NEWS_JSONL_UNTYPED_SA  # Identical for now

# NewsJSONL
PATH_NEWS_JSONL_OUTPUT: Path = Path("tests") / "data" / "output" / "news_jsonl.json"
PATH_NEWS_JSONL: Path = Path("tests") / "data" / "unit" / "news_jsonl.json"

# DataFrame
PATH_PANDAS_JSON_OUTPUT: Path = Path("tests") / "data" / "output" / "pandas_json.json"
PATH_PANDAS_JSON: Path = Path("tests") / "data" / "unit" / "pandas_json.json"
PATH_PANDAS_JSON_SA_OUTPUT: Path = (
    Path("tests") / "data" / "output" / "pandas_json_sentiment_analysis.json"
)

# TextSummaries
PATH_TEXT_SUMMARIES_OUTPUT: Path = (
    Path("tests") / "data" / "output" / "text_summaries.json"
)
PATH_TEXT_SUMMARIES: Path = Path("tests") / "data" / "unit" / "text_summaries.json"
PATH_TEXT_SUMMARIES_TS_OUTPUT: Path = (
    Path("tests") / "data" / "output" / "text_summaries_text_summarisation.json"
)
