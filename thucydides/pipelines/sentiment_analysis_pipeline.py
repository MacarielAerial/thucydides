import logging
from pathlib import Path
from typing import List

import torch
from pandas import DataFrame
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers.models.bert.modeling_bert import BertForSequenceClassification
from transformers.models.bert.tokenization_bert_fast import BertTokenizerFast

from thucydides.datasets.news_jsonl_dataset import NewsJSONL, NewsJSONLDataSet
from thucydides.datasets.pandas_json_dataset import PandasJsonDataSet

log = logging.getLogger(__name__)


def _sentiment_analysis_pipeline(news_jsonl: NewsJSONL) -> DataFrame:
    """In memory handler"""
    # Initiate tokeniser and model
    tokeniser: BertTokenizerFast = AutoTokenizer.from_pretrained(
        "nlptown/bert-base-multilingual-uncased-sentiment"
    )
    log.info(f"Loaded tokeniser of class {tokeniser.__class__}")

    model: BertForSequenceClassification = (
        AutoModelForSequenceClassification.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment"
        )
    )
    log.info(f"Loaded model of class {model.__class__}")

    # Gather input structure
    list_text: List[str] = [news_json.body for news_json in news_jsonl.list_news_json]

    # Compute sentiment scores for each article
    sentiment_scores: List[int] = []
    for text in list_text:
        tokens = tokeniser.encode(text, return_tensors="pt")
        result = model(tokens)
        sentiment_score = int(torch.argmax(result.logits)) + 1
        sentiment_scores.append(sentiment_score)
    log.info(f"Computed sentiment scores for {len(sentiment_scores)} entries")

    # Compile output structure
    df: DataFrame = DataFrame({"text": list_text, "sentiment_score": sentiment_scores})

    return df


def sentiment_analysis_pipeline(path_news_jsonl: Path, path_pandas_json: Path) -> None:
    """Performs sentiment analysis on news articles
    and exports result to a pandas dataframe"""
    # Data Access - Input
    news_jsonl_dataset = NewsJSONLDataSet(filepath=path_news_jsonl)
    news_jsonl = news_jsonl_dataset.load()

    # Task Processing
    df = _sentiment_analysis_pipeline(news_jsonl=news_jsonl)

    # Data Access - Output
    pandas_json_dataset = PandasJsonDataSet(filepath=path_pandas_json)
    pandas_json_dataset.save(df=df)
