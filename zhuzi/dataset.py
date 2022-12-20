from typing import Any, Type

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
    point: Type = DataPoint

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe
        if self._dataframe_has_named_columns():
            self.validate_column_names()

    def validate_column_names(self):
        invalid_columns = sorted(
            [f'"{column}"' for column in self.dataframe.columns if not str(column).isidentifier()]
        )
        if invalid_columns:
            raise ValueError(
                f'{", ".join(invalid_columns)} not allowed as column name(s): invalid identifier(s)'
            )

    def __getitem__(self, item: int) -> Any:
        if self._dataframe_has_named_columns():
            return self.point(**dict(self.dataframe.iloc[item]))
        return self.point(*self._raw_items_in_row_at(item))

    def _dataframe_has_named_columns(self):
        return not isinstance(self.dataframe.columns, pd.RangeIndex)

    def _raw_items_in_row_at(self, item):
        return self.dataframe.iloc[item].values

    def __len__(self) -> int:
        return len(self.dataframe)

    def is_empty(self) -> bool:
        return len(self) == 0
