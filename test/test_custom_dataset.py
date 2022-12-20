from dataclasses import dataclass

import pandas as pd
import pytest

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


# TODO: Maybe the message we are sending isn't the best. Check.
def test_custom_dataset_must_have_an_associated_point():
    message = "Can't declare CustomDataSet with abstract class attribute `point`"
    with pytest.raises(TypeError, match=message):

        class CustomDataSet(DataSetTemplate):
            pass
