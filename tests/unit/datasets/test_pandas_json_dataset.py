from pandas import DataFrame

from tests.data.data_registry import PATH_PANDAS_JSON, PATH_PANDAS_JSON_OUTPUT
from thucydides.datasets.pandas_json_dataset import PandasJsonDataSet


def test_pandas_json_dataset_save() -> None:
    if PATH_PANDAS_JSON_OUTPUT.is_file():
        PATH_PANDAS_JSON_OUTPUT.unlink()

    df = DataFrame({"col_1": [0.0, 1.0, 0.0], "col_2": [1.0, 1.0, 0.0]})

    pandas_json_dataset = PandasJsonDataSet(filepath=PATH_PANDAS_JSON_OUTPUT)
    pandas_json_dataset.save(df=df)

    assert PATH_PANDAS_JSON_OUTPUT.is_file()


def test_pandas_json_dataset_load() -> None:
    pandas_json_dataset = PandasJsonDataSet(filepath=PATH_PANDAS_JSON)
    df = pandas_json_dataset.load()

    assert not df.empty
