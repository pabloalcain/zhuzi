from dataclasses import dataclass

import pandas as pd

from zhuzi.dataset import DataSetTemplate


def test_custom_dataset_with_defined_point_generates_empty_dataframe_with_point_args_as_columns():
    # given
    @dataclass
    class CustomPoint:
        my_argument: int

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    # when
    dataset = CustomDataSet()
    # then
    pd.testing.assert_frame_equal(
        dataset.dataframe, pd.DataFrame({"my_argument": pd.Series(dtype="int")})
    )


def test_custom_dataset_with_another_point_generates_empty_dataframe_with_point_args_as_columns():
    # given
    @dataclass
    class CustomPoint:
        another_argument: float

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    # when
    dataset = CustomDataSet()
    # then
    pd.testing.assert_frame_equal(
        dataset.dataframe,
        pd.DataFrame({"another_argument": pd.Series(dtype="float64")}),
    )
