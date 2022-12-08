import pandas as pd


class DataSet:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        pass

    def is_empty(self) -> bool:
        return True


def test_create_empty_dataset_from_empty_dataframe():
    # given
    empty_dataframe = pd.DataFrame()
    dataset = DataSet(empty_dataframe)
    # then
    assert dataset.is_empty()
