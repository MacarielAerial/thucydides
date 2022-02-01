"""
Conducts topic modelling
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from pandas import DataFrame
from transformers import pipeline

from thucydides.datasets.news_jsonl_dataset import NewsJSONL
from thucydides.datasets.pandas_json_dataset import PandasJsonDataSet
from thucydides.datasets.zero_shot_classifiation_config_dataset import (
    ClassifierConfig,
    ZeroShotClassificationConfig,
)

log = logging.getLogger(__name__)


def _zero_shot_classification_pipeline(  # type: ignore[no-any-unimported]
    news_jsonl: NewsJSONL, zero_shot_classifiation_config: ZeroShotClassificationConfig
) -> DataFrame:
    """In-memory handler"""
    # Initiate classifier
    classifier = pipeline(
        zero_shot_classifiation_config.classifier_config.pipeline_task.value
    )

    # Estimate a topic label for each article
    list_id: List[str] = []
    list_text: List[str] = []
    list_topic_label: List[str] = []
    for news_json in news_jsonl.list_news_json:
        # Persist id
        id = news_json.id  # Primary key to identify each article
        list_id.append(id)

        # Persist text
        text = news_json.title  # Only use article title at the moment
        list_text.append(text)

        # Persist label
        result: Dict[str, Any] = classifier(
            text,
            zero_shot_classifiation_config.classifier_config.candidate_labels,
            multi_label=zero_shot_classifiation_config.classifier_config.multi_label,
        )
        topic_label: str = (
            result["labels"][0] if result["scores"][0] > 0.5 else "unclassified"
        )
        list_topic_label.append(topic_label)

    log.info(f"Estimated topic labels for {len(list_topic_label)} entries")

    # Compile output structure
    df: DataFrame = DataFrame(  # type: ignore[no-any-unimported]
        {"id": list_id, "text": list_text, "topic_label": list_topic_label}
    )

    # Post process output structure to encode topic labels
    df = pd.concat([df, pd.get_dummies(df["topic_label"])], axis=1)

    # Log descriptive statistis
    log.info(f"Descriptive statistics for topic labels:\n{df.describe()}")

    return df


def zero_shot_classification_pipeline(
    path_news_jsonl_untyped: Path, path_pandas_json: Path
) -> None:
    """Performs zero shot classification on input articles
    and exports results to a pandas dataframe"""
    # Data Access - Input
    news_jsonl = NewsJSONL.from_path_news_jsonl_untyped(
        path_news_jsonl_untyped=path_news_jsonl_untyped
    )
    zero_shot_classification_config = ZeroShotClassificationConfig(
        classifier_config=ClassifierConfig()
    )  # Use default setting at the moment

    # Task Processing
    df = _zero_shot_classification_pipeline(
        news_jsonl=news_jsonl,
        zero_shot_classifiation_config=zero_shot_classification_config,
    )

    # Data Access - Output
    pandas_json_dataset = PandasJsonDataSet(filepath=path_pandas_json)
    pandas_json_dataset.save(df=df)
