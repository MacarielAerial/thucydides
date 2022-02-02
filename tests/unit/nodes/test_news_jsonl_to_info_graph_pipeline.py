from tests.data.data_registry import PATH_NEWS_JSONL_NTI
from thucydides.datasets.news_jsonl_dataset import NewsJSONLDataSet
from thucydides.nodes.graph_construction import news_jsonl_to_info_graph


def test_news_jsonl_to_info_graph() -> None:
    news_jsonl_dataset = NewsJSONLDataSet(filepath=PATH_NEWS_JSONL_NTI)
    news_jsonl = news_jsonl_dataset.load()

    info_graph = news_jsonl_to_info_graph(news_jsonl=news_jsonl)

    assert info_graph.number_of_nodes() > 0
    assert info_graph.number_of_edges() > 0
