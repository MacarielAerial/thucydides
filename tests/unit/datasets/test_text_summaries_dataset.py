from tests.data.data_registry import PATH_TEXT_SUMMARIES, PATH_TEXT_SUMMARIES_OUTPUT
from thucydides.datasets.text_summaries_dataset import (
    TextSummaries,
    TextSummariesDataSet,
    TextSummary,
)


def test_text_summaries_dataset_save() -> None:
    if PATH_TEXT_SUMMARIES_OUTPUT.is_file():
        PATH_TEXT_SUMMARIES_OUTPUT.unlink()

    text_summaries = TextSummaries(
        list_text_summary=[TextSummary(id="dummy_id", summary="dummy_summary")]
    )

    text_summaries_dataset = TextSummariesDataSet(filepath=PATH_TEXT_SUMMARIES_OUTPUT)
    text_summaries_dataset.save(text_summaries=text_summaries)

    assert PATH_TEXT_SUMMARIES_OUTPUT.is_file()


def test_text_summaries_dataset_load() -> None:
    text_summaries_dataset = TextSummariesDataSet(filepath=PATH_TEXT_SUMMARIES)
    text_summaries = text_summaries_dataset.load()

    assert len(text_summaries.list_text_summary) > 0
