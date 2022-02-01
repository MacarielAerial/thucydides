"""
Detects sentiments (i.e. positive | negative)
"""

import logging
from pathlib import Path
from typing import List

import torch
from pandas import DataFrame  # pandas has no typing stub
from transformers import (  # transformers has no typing stub
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from transformers.models.bert.modeling_bert import BertForSequenceClassification
from transformers.models.bert.tokenization_bert_fast import BertTokenizerFast

from thucydides.datasets.news_jsonl_dataset import NewsJSONL
from thucydides.datasets.pandas_json_dataset import PandasJsonDataSet
from thucydides.datasets.sentiment_analysis_config_dataset import (
    SentimentAnalysisConfig,
    TokeniserConfig,
)

log = logging.getLogger(__name__)


def _sentiment_analysis_pipeline(  # type: ignore[no-any-unimported]
    news_jsonl: NewsJSONL, sentiment_analysis_config: SentimentAnalysisConfig
) -> DataFrame:
    """In memory handler"""
    # Initiate tokeniser and model
    tokeniser: BertTokenizerFast = AutoTokenizer.from_pretrained(
        sentiment_analysis_config.tokeniser.value,
    )
    log.info(f"Loaded tokeniser of class {tokeniser.__class__}")

    model: BertForSequenceClassification = (
        AutoModelForSequenceClassification.from_pretrained(
            sentiment_analysis_config.model.value
        )
    )
    log.info(f"Loaded model of class {model.__class__}")

    # Compute a sentiment score for each article
    list_id: List[str] = []
    list_text: List[str] = []
    list_sentiment_score: List[int] = []
    for news_json in news_jsonl.list_news_json:
        # Persist id
        id = news_json.id  # Primary key to identify each article
        list_id.append(id)

        # Persist text
        text = news_json.body  # Only use article body at the moment
        list_text.append(text)

        # Persist score
        tokens = tokeniser.encode(text, return_tensors="pt", truncation=True)
        result = model(tokens)
        sentiment_score = int(torch.argmax(result.logits)) + 1
        list_sentiment_score.append(sentiment_score)

    log.info(f"Computed sentiment scores for {len(list_sentiment_score)} entries")

    # Compile output structure
    df: DataFrame = DataFrame(  # type: ignore[no-any-unimported]
        {"id": list_id, "text": list_text, "sentiment_score": list_sentiment_score}
    )

    # Log descriptive statistis
    log.info(f"Descriptive statistics for sentiment scores:\n{df.describe()}")

    return df


def sentiment_analysis_pipeline(
    path_news_jsonl_untyped: Path, path_pandas_json: Path
) -> None:
    """Performs sentiment analysis on news articles
    and exports result to a pandas dataframe"""
    # Data Access - Input
    news_jsonl = NewsJSONL.from_path_news_jsonl_untyped(
        path_news_jsonl_untyped=path_news_jsonl_untyped
    )
    sentiment_analysis_config = SentimentAnalysisConfig(
        tokeniser_config=TokeniserConfig()
    )  # Use default setting at the moment

    # Task Processing
    df = _sentiment_analysis_pipeline(
        news_jsonl=news_jsonl, sentiment_analysis_config=sentiment_analysis_config
    )

    # Data Access - Output
    pandas_json_dataset = PandasJsonDataSet(filepath=path_pandas_json)
    pandas_json_dataset.save(df=df)
