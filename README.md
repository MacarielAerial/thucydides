# News Article NLP Project
The repository contains code required to execute Natural Language Processing tasks on JSON formatted news article data

Documentation for this project is [here](https://miro.com/app/board/uXjVOQ9HS6k=/?invite_link_id=987441986728)

## Aggregate Multiple Raw Input Objects into One
    pipenv run python -m thucydides.nodes.io \
    -jsons data/01_raw/news-articles/ \
    -jsonl data/01_raw/news-articles.jsonl

## Strongly Type Aggregated Input Object
    pipenv run python -m thucydides.pipeline.news_jsonl_untyped_to_news_jsonl_pipeline \
    -nju data/01_raw/news-article.jsonl \
    -nj data/02_intermediate/news_jsonl.json

## Construct a Graph from Typed and Aggregated Input Object
    pipenv run python -m thucydides.pipeline.graph_construction_pipeline \
    -nj data/02_intermediate/news_jsonl.json \
    -ig data/03_primary/info_graph.json

## Execute Zero Shot Classification
    pipenv run python -m thucydides.pipeline.zero_shot_classification_pipeline \
    -nju data/01_raw/news-articles.jsonl \
    -pj data/07_model_output/pandas_json_zero_shot_classification.json

## Execute Sentiment Analysis
    pipenv run python -m thucydides.pipeline.sentiment_analysis \
    -nju data/01_raw/news-articles.jsonl \
    -pj data/07_model_output/pandas_json_sentiment_analysis.json

## Execute Text Summarisation
    pipenv run python -m thucydides.pipeline.text_summarisation_pipelin \
    -nju data/01_raw/news-articles.jsonl \
    -ts data/07_model/text_summaries.json
    
