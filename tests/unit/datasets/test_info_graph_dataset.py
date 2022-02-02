from networkx import DiGraph

from tests.data.data_registry import PATH_INFO_GRAPH, PATH_INFO_GRAPH_OUTPUT
from thucydides.datasets.info_graph_dataset import InfoGraphDataSet


def test_info_graph_dataset_save() -> None:
    if PATH_INFO_GRAPH_OUTPUT.is_file():
        PATH_INFO_GRAPH_OUTPUT.unlink()

    nx_g = DiGraph()
    nx_g.add_nodes_from([(0, {"dummy_attr_1": "dummy_value"})])

    info_graph_dataset = InfoGraphDataSet(filepath=PATH_INFO_GRAPH_OUTPUT)
    info_graph_dataset.save(nx_g=nx_g)

    assert PATH_INFO_GRAPH_OUTPUT.is_file()


def test_info_graph_dataset_load() -> None:
    info_graph_dataset = InfoGraphDataSet(filepath=PATH_INFO_GRAPH)
    info_graph = info_graph_dataset.load()

    assert info_graph.number_of_nodes() > 0
