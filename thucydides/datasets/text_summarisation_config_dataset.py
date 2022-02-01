from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dataclasses_json import dataclass_json


class TextSummarisationConfigDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def save(self, text_summarisation_config: TextSummarisationConfig) -> None:
        raise NotImplementedError  # No need to persist this structure to disc yet

    def load(self) -> None:
        raise NotImplementedError


@dataclass_json
@dataclass
class PipelineTask(Enum):
    SUMMARISATION: str = "summarization"


@dataclass_json
@dataclass
class SummariserConfig:
    pipeline_task: PipelineTask = PipelineTask.SUMMARISATION
    truncation: bool = True
    max_length: int = 130
    min_length: int = 30
    do_sample: bool = False


@dataclass_json
@dataclass
class TextSummarisationConfig:
    summariser_config: SummariserConfig
