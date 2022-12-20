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

    def __getitem__(self, item: int) -> DataPoint:
        if self._dataframe_has_named_columns():
            return DataPoint(**dict(self.dataframe.iloc[item]))
        return DataPoint(*self._raw_items_in_row_at(item))

    def _dataframe_has_named_columns(self):
        return not isinstance(self.dataframe.columns, pd.RangeIndex)

    def _raw_items_in_row_at(self, item):
        return self.dataframe.iloc[item].values

    def __len__(self) -> int:
        return len(self.dataframe)

    def is_empty(self) -> bool:
        return len(self) == 0


class DataSetTemplate:
    # point is an "abstract class attribute". The checking implementation is in `__init_subclass__`
    # check https://stackoverflow.com/questions/49022656/
    # /python-create-abstract-static-property-within-class
    point = None

    def __init_subclass__(cls):
        if not any("point" in base.__dict__ for base in cls.__mro__ if base is not DataSetTemplate):
            raise TypeError(f"Can't declare {cls.__name__} with abstract class attribute `point`")

    def __init__(self):
        values = {
            arg: pd.Series(dtype=argtype) for arg, argtype in self.point.__annotations__.items()
        }
        self.dataframe = pd.DataFrame(values)
