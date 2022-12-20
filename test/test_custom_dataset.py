import re
from dataclasses import dataclass

import pandas as pd
import pytest

from zhuzi.dataset import BadDataFrameException
from zhuzi.dataset_template import DataSetTemplate

LEN_3_DATAFRAME = pd.DataFrame({"my_argument": pd.Series([10.0, 20.0, 30.0], dtype="float")})


@pytest.fixture
def custom_1d_dataset():
    @dataclass
    class CustomPoint:
        my_argument: float

    class CustomDataSet(DataSetTemplate):
        point = CustomPoint

    return CustomDataSet, CustomPoint


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
        "DataFrame columns are ['wrong_name'] and they should match CustomPoint arguments "
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
        "DataFrame columns are ['another_wrong_name'] and they should match CustomPoint arguments "
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
        "CustomPoint arguments {'my_argument': 'int64'}"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)


def test_custom_dataset_raises_error_when_df_col_type_does_not_match_attrs_of_point_triangulation(
    custom_1d_dataset,
):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset

    badly_formed_dataframe = pd.DataFrame({"my_argument": pd.Series(dtype="int")})

    # then
    message = (
        "DataFrame columns types are {'my_argument': 'int64'} and they should match "
        "CustomPoint arguments {'my_argument': 'float64'}"
    )

    with pytest.raises(BadDataFrameException, match=message):
        CustomDataSet(badly_formed_dataframe)


def test_custom_dataset_dataframe_can_be_accessed(custom_1d_dataset):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    dataframe = pd.DataFrame({"my_argument": pd.Series(dtype="float")})
    custom_dataset = CustomDataSet(dataframe)
    # then
    custom_dataset.dataframe
    pd.testing.assert_frame_equal(custom_dataset.dataframe, dataframe)


def test_custom_dataset_keeps_length_of_the_original_dataframe(custom_1d_dataset):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    custom_dataset = CustomDataSet(LEN_3_DATAFRAME)
    # then
    assert len(custom_dataset) == 3


def test_an_item_of_the_custom_dataset_is_the_expected_datapoint(custom_1d_dataset):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    custom_dataset = CustomDataSet(LEN_3_DATAFRAME)
    # when
    datapoint_accessed_by_index = custom_dataset[2]
    # then
    assert datapoint_accessed_by_index == CustomPoint(30.0)


def test_column_names_can_be_accessed_as_attributes_of_dataset(custom_1d_dataset):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    custom_dataset = CustomDataSet(LEN_3_DATAFRAME)
    # then
    pd.testing.assert_series_equal(custom_dataset.my_argument, LEN_3_DATAFRAME["my_argument"])


def test_custom_dataset_dataframe_can_have_extra_columns(custom_1d_dataset):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    longer_dataframe = pd.DataFrame([[0, 1.0], [1, 2.0]], columns=["a_new_argument", "my_argument"])
    custom_dataset = CustomDataSet(longer_dataframe)
    # then
    pd.testing.assert_frame_equal(custom_dataset.dataframe, longer_dataframe)


def test_custom_dataset_raises_error_when_hotplugging_badly_formed_dataframe(
    custom_1d_dataset,
):
    # given
    CustomDataSet, CustomPoint = custom_1d_dataset
    dataset = CustomDataSet(LEN_3_DATAFRAME)

    badly_formed_dataframe = pd.DataFrame({"my_argument": pd.Series(dtype="int")})
    # then
    message = (
        "DataFrame columns types are {'my_argument': 'int64'} and they should match "
        "CustomPoint arguments {'my_argument': 'float64'}"
    )

    with pytest.raises(BadDataFrameException, match=message):
        dataset.dataframe = badly_formed_dataframe
