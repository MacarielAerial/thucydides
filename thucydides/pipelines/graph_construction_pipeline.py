"""
Constructs a static graph
"""

from pathlib import Path

from thucydides.datasets.info_graph_dataset import InfoGraphDataSet
from thucydides.datasets.news_jsonl_dataset import NewsJSONLDataSet
from thucydides.nodes.graph_construction import news_jsonl_to_info_graph


def graph_construction_pipeline(path_news_jsonl: Path, path_info_graph: Path) -> None:
    """Constructs a static graph from news articles
    and exports result to a networkx graph"""
    # Data Access - Input
    news_jsonl_dataset = NewsJSONLDataSet(filepath=path_news_jsonl)
    news_jsonl = news_jsonl_dataset.load()

    # Task Processing
    nx_g = news_jsonl_to_info_graph(news_jsonl=news_jsonl)

    # Data Access - Output
    info_graph_dataset = InfoGraphDataSet(filepath=path_info_graph)
    info_graph_dataset.save(nx_g=nx_g)


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Constructs a static graph from news articles"
    )
    parser.add_argument(
        "-nj",
        "--path_news_jsonl",
        help="Path to a serialised JSONL object",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-ig",
        "--path_info_graph",
        help="Path to a serialised networkx graph object",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    graph_construction_pipeline(
        path_news_jsonl=args.path_news_jsonl, path_info_graph=args.path_info_graph
    )
