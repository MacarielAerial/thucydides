from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List

from dataclasses_json import dataclass_json


class ZeroShotClassificationDataSet:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @staticmethod
    def _check_file_exist(filepath: Path) -> None:
        if not filepath.is_file():
            raise ValueError(f"{filepath} is not a file")

    def save(
        self, zero_shot_classification_config: ZeroShotClassificationConfig
    ) -> None:
        raise NotImplementedError  # No need to persist this structure to disc yet

    def load(self) -> None:
        raise NotImplementedError


@dataclass_json
@dataclass
class PipelineTask(Enum):
    ZERO_SHOT_CLASSIFICATION: str = "zero-shot-classification"


@dataclass_json
@dataclass
class ClassifierConfig:
    candidate_labels: List[str] = field(
        default_factory=lambda: [
            "accounting",
            "anti-competition",
            "business ethics",
            "consumer complaints",
            "customer health & safety",
            "diversity & opportunity",
            "employee health & safety",
            "environmental",
            "general shareholder rights",
            "human rights",
            "insider dealings",
            "intellectual property",
            "management compensation",
            "management departures",
            "privacy",
            "public health",
            "responsible marketing",
            "tax fraud",
            "wage or working condition",
        ]
    )
    hypothesis_template: str = "The article is about {}."
    multi_label: bool = (
        True  # When False, the NLP model assumes only one of supplied labels is true
    )
    pipeline_task: PipelineTask = PipelineTask.ZERO_SHOT_CLASSIFICATION


@dataclass_json
@dataclass
class ZeroShotClassificationConfig:
    classifier_config: ClassifierConfig
