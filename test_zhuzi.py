import pandas as pd


class DataSet:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def __len__(self) -> int:
        return len(self.dataframe)

    def is_empty(self) -> bool:
        return len(self) == 0


def test_create_empty_dataset_from_empty_dataframe():
    # given
    empty_dataframe = pd.DataFrame()
    dataset = DataSet(empty_dataframe)
    # then
    assert dataset.is_empty()


def test_create_nonempty_dataset_from_nonempty_dataframe():
    # given
    non_empty_dataframe = pd.DataFrame([1])
    dataset = DataSet(non_empty_dataframe)
    # then
    assert not dataset.is_empty()


def test_dataset_keeps_length_of_the_original_dataframe():
    # given
    a_length_3_dataframe = pd.DataFrame([[10], [20], [30]])
    dataset = DataSet(a_length_3_dataframe)
    # then
    assert len(dataset) == 3
