import re
from dataclasses import dataclass

import pandas as pd
import pytest

from zhuzi.dataset_template import BadDataFrameException, DataSetTemplate


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


def test_custom_dataset_raises_error_when_df_col_name_does_not_match_attrs_of_point():
    # given
    @dataclass
    class CustomPoint:
        my_argument: int

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    badly_formed_dataframe = pd.DataFrame({"wrong_name": pd.Series(dtype="int")})

    # then
    message = re.escape(
        "DataFrame columns are ['wrong_name'] and they should match CustomPointArguments "
        "['my_argument']"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)


def test_custom_dataset_raises_error_when_df_col_name_does_not_match_attrs_of_point_triangulation():
    # given
    @dataclass
    class CustomPoint:
        another_argument: int

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    badly_formed_dataframe = pd.DataFrame({"another_wrong_name": pd.Series(dtype="int")})

    # then
    message = re.escape(
        "DataFrame columns are ['another_wrong_name'] and they should match CustomPointArguments "
        "['another_argument']"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)


def test_custom_dataset_raises_error_when_df_col_type_does_not_match_attrs_of_point():
    # given
    @dataclass
    class CustomPoint:
        my_argument: int

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    badly_formed_dataframe = pd.DataFrame({"my_argument": pd.Series(dtype="float")})

    # then
    message = (
        "DataFrame columns types are {'my_argument': 'float64'} and they should match "
        "CustomPointArguments {'my_argument': 'int64'}"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)


def test_custom_dataset_raises_error_when_df_col_type_does_not_match_attrs_of_point_triangulation():
    # given
    @dataclass
    class CustomPoint:
        my_argument: float

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    badly_formed_dataframe = pd.DataFrame({"my_argument": pd.Series(dtype="int")})

    # then
    message = (
        "DataFrame columns types are {'my_argument': 'int64'} and they should match "
        "CustomPointArguments {'my_argument': 'float64'}"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)
