"""
Types a JSONL object with the corresponding dataclass
"""

from pathlib import Path

from thucydides.datasets.news_jsonl_dataset import NewsJSONL, NewsJSONLDataSet


def news_jsonl_untyped_to_news_jsonl_pipeline(
    path_news_jsonl_untyped: Path, path_news_jsonl: Path
) -> None:
    """Loads untyped news articles, types them
    and exports the result as a serialised dataclass object"""
    # Task Processing
    news_jsonl = NewsJSONL.from_path_news_jsonl_untyped(
        path_news_jsonl_untyped=path_news_jsonl_untyped
    )

    # Data Access - Output
    news_jsonl_dataset = NewsJSONLDataSet(filepath=path_news_jsonl)
    news_jsonl_dataset.save(news_jsonl=news_jsonl)


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Types a news article jsonl object and exports as a dataclass"
    )
    parser.add_argument(
        "-nju",
        "--path_news_jsonl_untyped",
        help="Path to a untyped news jsonl object",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-nj",
        "--path_news_jsonl",
        help="Path to a news jsonl object",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    news_jsonl_untyped_to_news_jsonl_pipeline(
        path_news_jsonl_untyped=args.path_news_jsonl_untyped,
        path_news_jsonl=args.path_news_jsonl,
    )
