import pandas as pd


class DataPoint:
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataPoint):
            raise NotImplementedError
        return self.value == other.value


class DataSet:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def __getitem__(self, item: int) -> DataPoint:
        return DataPoint(30)

    def __len__(self) -> int:
        return len(self.dataframe)

    def is_empty(self) -> bool:
        return len(self) == 0
