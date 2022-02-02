import logging
from typing import Any, Dict, List, Set, Tuple

from networkx_query import search_nodes

from thucydides.datasets.info_graph_dataset import (
    ArticleNodeAttributes,
    AttributeName,
    DiGraph,
    EdgeType,
    NodeType,
    SourceArticleEdgeAttributes,
    SourceNodeAttributes,
)
from thucydides.datasets.news_jsonl_dataset import NewsJSONL

log = logging.getLogger(__name__)


def news_jsonl_to_info_graph(news_jsonl: NewsJSONL) -> DiGraph:
    """Converts a NewsJSONL object into DiGraph object
    with minimal loss of information"""
    # Initiate a global node id counter
    current_nid: int = 0

    # Initiate a set to contrain the range of nodes of type "source"
    set_name_source_node: Set[str] = set()

    # Initiate intermediary variables that store nodes and edges
    nodes: List[
        Tuple[int, Dict[str, Any]]
    ] = []  # Tuple position 0 is nid and 1 is node attributes
    edges: List[
        Tuple[int, int, Dict[str, Any]]
    ] = []  # Tuple position 0 and 1 are eid and 2 is edge attributes

    # Parse nodes of different types into graph
    source_nodes: List[Tuple[int, Dict[str, Any]]] = []
    article_nodes: List[Tuple[int, Dict[str, Any]]] = []
    for news_json in news_jsonl.list_news_json:
        # Skip this iteration if the source node already exists
        if news_json.source in set_name_source_node:
            continue

        source_node_attributes: SourceNodeAttributes = SourceNodeAttributes(
            node_type=NodeType.source, name=news_json.source
        )  # e.g. "BBC News"
        node_attrs = source_node_attributes.to_attrs()
        source_node: Tuple[int, Dict[str, Any]] = (current_nid, node_attrs)

        # Append to the container
        source_nodes.append(source_node)
        current_nid += 1

        # Record the existance of the name of the current source node
        set_name_source_node.add(source_node_attributes.name)

    log.info(f"Parsed {len(source_nodes)} nodes of type {NodeType.source.value}")

    for news_json in news_jsonl.list_news_json:
        article_node_attributes: ArticleNodeAttributes = ArticleNodeAttributes(
            node_type=NodeType.article,
            title=news_json.title,
            publish_date=news_json.publish_date,
            id=news_json.id,
            body=news_json.body,
        )
        node_attrs = article_node_attributes.to_attrs()
        article_node: Tuple[int, Dict[str, Any]] = (current_nid, node_attrs)

        # Append to the container
        article_nodes.append(article_node)
        current_nid += 1

    log.info(f"Parsed {len(article_nodes)} nodes of type {NodeType.article.value}")

    # Compile nodes of all types
    nodes.extend(source_nodes)
    nodes.extend(article_nodes)

    log.info(f"In total, {len(nodes)} nodes are parsed from {type(news_jsonl)} object")

    # Construct the edgeless graph
    nx_g: DiGraph = DiGraph()
    nx_g.add_nodes_from(nodes)

    # Parse edges of different types into graph
    source_article_edges: List[Tuple[int, int, Dict[str, Any]]] = []
    for news_json in news_jsonl.list_news_json:
        source_article_edge_attributes: SourceArticleEdgeAttributes = (
            SourceArticleEdgeAttributes(edge_type=EdgeType.source_article)
        )
        edge_attrs = source_article_edge_attributes.to_attrs()

        # Search the edgeless graph for corresponding node ids of the current edge

        #
        # Search node of type source
        #
        query_result: List[int] = list(
            search_nodes(
                graph=nx_g,
                query={
                    "and": [
                        {
                            "==": [
                                (AttributeName.node_type.value,),
                                NodeType.source.value,
                            ]
                        },
                        {"==": [(AttributeName.name.value,), news_json.source]},
                    ]
                },
            )
        )
        if len(query_result) != 1:
            raise ValueError(
                f"Query returned {query_result} instead of a length one list"
            )
        else:
            source_nid = query_result[0]

        #
        # Search node of type article
        #
        query = {
            "and": [
                {"==": [(AttributeName.node_type.value,), NodeType.article.value]},
                {"==": [(AttributeName.id.value,), news_json.id]},
            ]
        }
        print(query)
        print(nx_g.nodes.data())
        query_result: List[int] = list(
            search_nodes(
                graph=nx_g,
                query={
                    "and": [
                        {
                            "==": [
                                (AttributeName.node_type.value,),
                                NodeType.article.value,
                            ]
                        },
                        {"==": [(AttributeName.id.value,), news_json.id]},
                    ]
                },
            )
        )
        if len(query_result) != 1:
            raise ValueError(
                f"Query returned {query_result} instead of a length one list"
            )
        else:
            article_nid = query_result[0]

        source_article_edge: Tuple[int, int, Dict[str, Any]] = (
            source_nid,
            article_nid,
            edge_attrs,
        )

        # Append to the container
        source_article_edges.append(source_article_edge)

    # Compile edges of all types
    edges.extend(source_article_edges)

    log.info(f"In total, {len(edges)} edges are parsed from {type(news_jsonl)} object")

    # Populate the edgeless graph with edges
    nx_g.add_edges_from(edges)

    log.info(
        f"The constructed graph has {nx_g.number_of_nodes()} nodes "
        f"and {nx_g.number_of_edges()} edges"
    )

    return nx_g
