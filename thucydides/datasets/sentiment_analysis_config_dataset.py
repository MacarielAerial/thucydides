from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dataclasses_json import dataclass_json


class SentimentAnalysisConfigDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def save(self, sentiment_analysis_config: SentimentAnalysisConfig) -> None:
        raise NotImplementedError  # No need to persist this structure to disc yet

    def load(self) -> None:
        raise NotImplementedError


@dataclass_json
@dataclass
class TransformerTokeniser(Enum):
    BERT: str = "nlptown/bert-base-multilingual-uncased-sentiment"


@dataclass_json
@dataclass
class TransformerModel(Enum):
    BERT: str = "nlptown/bert-base-multilingual-uncased-sentiment"


@dataclass_json
@dataclass
class TokeniserConfig:
    return_tensors: str = "pt"
    trunaction: bool = True


@dataclass_json
@dataclass
class SentimentAnalysisConfig:
    tokeniser_config: TokeniserConfig
    tokeniser: TransformerTokeniser = TransformerTokeniser.BERT
    model: TransformerModel = TransformerModel.BERT
