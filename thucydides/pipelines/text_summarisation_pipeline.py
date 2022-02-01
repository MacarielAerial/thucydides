"""
Singles out parts to serve as summary of the whole
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from transformers import pipeline

from thucydides.datasets.news_jsonl_dataset import NewsJSONL
from thucydides.datasets.text_summaries_dataset import (
    TextSummaries,
    TextSummariesDataSet,
    TextSummary,
)
from thucydides.datasets.text_summarisation_config_dataset import (
    SummariserConfig,
    TextSummarisationConfig,
)

log = logging.getLogger(__name__)


def _text_summarisation_pipeline(
    news_jsonl: NewsJSONL, text_summarisation_config: TextSummarisationConfig
) -> TextSummaries:
    """In-memory handler"""
    # Initiate summariser
    summariser = pipeline(
        text_summarisation_config.summariser_config.pipeline_task.value
    )

    # Derive a summary for each article
    list_text_summary: List[TextSummary] = []
    for news_json in news_jsonl.list_news_json:
        id = news_json.id  # Primary key to identify each article
        text = news_json.body  # Only use article body at the moment
        result: List[Dict[str, Any]] = summariser(
            text,
            max_length=text_summarisation_config.summariser_config.max_length,
            min_length=text_summarisation_config.summariser_config.min_length,
            do_sample=text_summarisation_config.summariser_config.do_sample,
            truncation=text_summarisation_config.summariser_config.truncation,
        )
        summary: str = result[0][
            "summary_text"
        ]  # Hard coding should be replaced in the future

        text_summary: TextSummary = TextSummary(id=id, summary=summary)
        list_text_summary.append(text_summary)

    log.info(f"Derived summaries for {len(list_text_summary)} entries")

    # Compile output structure
    text_summaries = TextSummaries(list_text_summary=list_text_summary)

    return text_summaries


def text_summarisation_pipeline(
    path_news_jsonl_untyped: Path, path_text_summaries: Path
) -> None:
    """Performs text summarisation on input articles
    and exports results to a serialised dataclass object"""
    # Data Access - Input
    news_jsonl = NewsJSONL.from_path_news_jsonl_untyped(
        path_news_jsonl_untyped=path_news_jsonl_untyped
    )
    text_summarisation_config = TextSummarisationConfig(
        summariser_config=SummariserConfig()
    )  # Use default setting at the moment

    # Task Processing
    text_summaries = _text_summarisation_pipeline(
        news_jsonl=news_jsonl, text_summarisation_config=text_summarisation_config
    )

    # Data Access - Output
    text_summaries_dataset = TextSummariesDataSet(filepath=path_text_summaries)
    text_summaries_dataset.save(text_summaries=text_summaries)
