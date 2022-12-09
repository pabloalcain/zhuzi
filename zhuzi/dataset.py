from typing import Any

import pandas as pd


class DataPoint:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.__dict__.update(kwargs)

    def __getitem__(self, item: int) -> Any:
        return self.args[item]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataPoint):
            raise NotImplementedError
        return self.args == other.args


class DataSet:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def __getitem__(self, item: int) -> DataPoint:
        return DataPoint(*self._raw_items_in_row_at(item))

    def _raw_items_in_row_at(self, item):
        return self.dataframe.iloc[item].values

    def __len__(self) -> int:
        return len(self.dataframe)

    def is_empty(self) -> bool:
        return len(self) == 0
