from typing import Optional

import numpy as np
import pandas as pd


class DataSetTemplate:
    # point is an "abstract class attribute". The checking implementation is in `__init_subclass__`
    # check https://stackoverflow.com/questions/49022656/
    # /python-create-abstract-static-property-within-class
    point = None

    def __init_subclass__(cls):
        if not any("point" in base.__dict__ for base in cls.__mro__ if base is not DataSetTemplate):
            raise TypeError(f"Can't declare {cls.__name__} with abstract class attribute `point`")

    def __init__(self, dataframe: Optional[pd.DataFrame] = None):
        if dataframe is None:
            values = {arg: pd.Series(dtype=argtype) for arg, argtype in self._point_args_and_types}
            self.dataframe = pd.DataFrame(values)
        else:
            self._validate_columns_and_point(dataframe)

    def _validate_columns_and_point(self, dataframe):
        if sorted(dataframe.columns) != self._point_args:
            raise BadDataFrameException(
                f"DataFrame columns are {sorted(dataframe.columns)} and they should match "
                f"CustomPointArguments {self._point_args}"
            )
        if sorted(dataframe.dtypes.items()) != self._point_args_and_types:
            columns_types = {k: str(v) for k, v in dataframe.dtypes.items()}
            point_types = {arg: str(argtype) for arg, argtype in self._point_args_and_types}
            raise BadDataFrameException(
                f"DataFrame columns types are {columns_types} and they should match "
                f"CustomPointArguments {point_types}"
            )

    @property
    def _point_args_and_types(self):
        sorted_annotations = sorted(self.point.__annotations__.items())
        return ((arg, np.dtype(argtype)) for arg, argtype in sorted_annotations)

    @property
    def _point_args(self):
        return sorted(self.point.__annotations__.keys())


class BadDataFrameException(Exception):
    pass
