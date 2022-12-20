from typing import Optional, Type

import numpy as np
import pandas as pd

from zhuzi.dataset import BadDataFrameException, DataPoint, DataSet


class DataSetTemplate(DataSet):
    # point is an "abstract class attribute". The checking implementation is in `__init_subclass__`
    # check https://stackoverflow.com/questions/49022656/
    # /python-create-abstract-static-property-within-class
    point: Type = DataPoint

    def __init_subclass__(cls):
        if not any(
            "point" in base.__dict__
            for base in cls.__mro__
            if base not in (DataSetTemplate, DataSet)
        ):
            raise TypeError(f"Can't declare {cls.__name__} with abstract class attribute `point`")

    def __init__(self, dataframe: Optional[pd.DataFrame] = None):
        if dataframe is None:
            values = {arg: pd.Series(dtype=argtype) for arg, argtype in self._point_args_and_types}
            dataframe = pd.DataFrame(values)
        else:
            self._validate_columns_and_point(dataframe)
        super().__init__(dataframe)

    def _validate_columns_and_point(self, dataframe):
        if not set(self._point_args).issubset(dataframe.columns):
            raise BadDataFrameException(
                f"DataFrame columns are {sorted(dataframe.columns)} and they should match "
                f"CustomPointArguments {self._point_args}"
            )
        if not set(self._point_args_and_types).issubset(sorted(dataframe.dtypes.items())):
            columns_types = {k: str(v) for k, v in dataframe.dtypes.items()}
            point_types = {arg: str(argtype) for arg, argtype in self._point_args_and_types}
            raise BadDataFrameException(
                f"DataFrame columns types are {columns_types} and they should match "
                f"CustomPointArguments {point_types}"
            )

    @property
    def _point_args_and_types(self):
        sorted_annotations = sorted(self.point.__annotations__.items())
        return [(arg, np.dtype(argtype)) for arg, argtype in sorted_annotations]

    @property
    def _point_args(self):
        return sorted(self.point.__annotations__.keys())
