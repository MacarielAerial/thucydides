import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict

import networkx as nx
from dataclasses_json import dataclass_json
from networkx import DiGraph

log = logging.getLogger(__name__)


@dataclass_json
@dataclass
class NodeType(Enum):
    source: str = "source"
    article: str = "article"


@dataclass_json
@dataclass
class AttributeName(Enum):
    node_type: str = "node_type"
    name: str = "name"
    publish_date: str = "publish_date"
    id: str = "id"
    title: str = "title"
    body: str = "body"

    edge_type: str = "edge_type"


@dataclass_json
@dataclass
class SourceNodeAttributes:
    node_type: NodeType
    name: str

    def to_attrs(self) -> Dict[str, Any]:
        return {
            AttributeName.node_type.value: self.node_type.value,
            AttributeName.name.value: self.name,
        }


@dataclass_json
@dataclass
class ArticleNodeAttributes:
    node_type: NodeType
    title: str
    publish_date: str
    id: str  # Unique identifier for nodes of type "article"
    body: str

    def to_attrs(self) -> Dict[str, Any]:
        return {
            AttributeName.node_type.value: self.node_type.value,
            AttributeName.id.value: self.id,
            AttributeName.title.value: self.title,
            AttributeName.publish_date.value: self.publish_date,
            AttributeName.body.value: self.body,
        }


@dataclass_json
@dataclass
class EdgeType(Enum):
    source_article: str = "source_article"  # a.k.a "publish"


@dataclass_json
@dataclass
class SourceArticleEdgeAttributes:
    edge_type: EdgeType

    def to_attrs(self) -> Dict[str, Any]:
        return {AttributeName.edge_type.value: self.edge_type.value}


@dataclass_json
@dataclass
class GraphAttributes:
    source_node_attributes: SourceNodeAttributes
    article_node_attributes: ArticleNodeAttributes
    source_article_edge_attributes: SourceArticleEdgeAttributes


class InfoGraphDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def load(self) -> DiGraph:
        return self._load(filepath=self.filepath)

    @staticmethod
    def _load(filepath: Path) -> DiGraph:
        with open(filepath, "r") as f:
            data = json.load(f)
            nx_g: DiGraph = nx.node_link_graph(data)

            log.info(f"Loaded a {type(nx_g)} object from {filepath}")

            return nx_g

    def save(self, nx_g: DiGraph) -> None:
        self._save(filepath=self.filepath, nx_g=nx_g)

    @staticmethod
    def _save(filepath: Path, nx_g: DiGraph) -> None:
        with open(filepath, "w") as f:
            data = nx.node_link_data(nx_g)

            json.dump(data, f)

            log.info(f"Saved a {type(nx_g)} object to {filepath}")
