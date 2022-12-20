import re

import pandas as pd
import pytest

from zhuzi.dataset import DataPoint, DataSet

A_LENGTH_3_DATAFRAME = pd.DataFrame([[10], [20], [30]])


def test_create_empty_dataset_from_empty_dataframe():
    # given
    empty_dataframe = pd.DataFrame()
    dataset = DataSet(empty_dataframe)
    # then
    assert dataset.is_empty()


def test_create_nonempty_dataset_from_nonempty_dataframe():
    # given
    non_empty_dataframe = pd.DataFrame([1])
    dataset = DataSet(non_empty_dataframe)
    # then
    assert not dataset.is_empty()


def test_dataset_keeps_length_of_the_original_dataframe():
    # given
    dataset = DataSet(A_LENGTH_3_DATAFRAME)
    # then
    assert len(dataset) == 3


def test_comparing_datapoints_with_another_class_raises_an_error():
    # given
    one_datapoint = DataPoint(10)
    # then
    with pytest.raises(NotImplementedError):
        one_datapoint == object()


def test_two_datapoints_with_the_same_value_are_equal():
    # given
    one_datapoint = DataPoint(10)
    another_datapoint = DataPoint(10)
    # then
    assert one_datapoint == another_datapoint


def test_two_datapoints_with_different_values_are_not_equal():
    # given
    one_datapoint = DataPoint(10)
    another_datapoint = DataPoint(20)
    # then
    assert one_datapoint != another_datapoint


def test_an_item_of_the_dataset_is_the_expected_datapoint():
    # given
    dataset = DataSet(A_LENGTH_3_DATAFRAME)
    # when
    datapoint_accessed_by_index = dataset[2]
    # then
    assert datapoint_accessed_by_index == DataPoint(30)


def test_another_item_of_the_dataset_is_the_expected_datapoint():
    # given
    dataset = DataSet(A_LENGTH_3_DATAFRAME)
    # when
    datapoint_accessed_by_index = dataset[0]
    # then
    assert datapoint_accessed_by_index == DataPoint(10)


def test_iterate_on_dataset_returns_all_expected_datapoints_in_order():
    # given
    dataset = DataSet(A_LENGTH_3_DATAFRAME)
    expected_datapoints = [DataPoint(10), DataPoint(20), DataPoint(30)]
    # when
    dataset_iterated_as_list = [dataset_point for dataset_point in dataset]
    # then
    assert dataset_iterated_as_list == expected_datapoints


def test_two_datapoints_with_equal_and_multiple_values_are_equal():
    # given
    first_datapoint = DataPoint(1, 2)
    second_datapoint = DataPoint(1, 2)
    # then
    assert first_datapoint == second_datapoint


def test_two_datapoints_with_different_and_multiple_values_are_different():
    # given
    first_datapoint = DataPoint(1, 2)
    second_datapoint = DataPoint(10, 2)
    third_datapoint = DataPoint(1, 20)
    # then
    assert first_datapoint != second_datapoint
    assert first_datapoint != third_datapoint
    assert second_datapoint != third_datapoint


def test_item_from_dataframe_with_multiple_columns_equals_datapoint():
    # given
    dataframe = pd.DataFrame([[1, 10], [2, 20], [3, 30]])
    dataset = DataSet(dataframe)
    # when
    datapoint = dataset[1]
    # then
    assert datapoint == DataPoint(2, 20)


def test_datapoint_element_can_be_accessed_by_index():
    # given
    datapoint = DataPoint(1, 2, 3)
    # then
    assert datapoint[0] == 1


def test_all_datapoint_elements_can_be_accessed_by_index():
    # given
    datapoint = DataPoint(1, 2, 3)
    # then
    assert datapoint[:] == (1, 2, 3)


def test_datapoint_keyword_arguments_are_preserved_as_attributes():
    # given
    datapoint = DataPoint(one_value=1)
    # then
    assert datapoint.one_value == 1


def test_item_from_dataframe_with_named_column_preserves_attribute_name():
    # given
    dataframe = pd.DataFrame([[1]], columns=["one_value"])
    dataset = DataSet(dataframe)
    # when
    datapoint = dataset[0]
    # then
    assert datapoint.one_value == 1


def test_dataframes_on_datasets_cannot_have_columns_with_names_with_spaces():
    # given
    forbidden_name_with_spaces = "a b"
    dataframe = pd.DataFrame([[1]], columns=[forbidden_name_with_spaces])
    message = re.escape(
        f'"{forbidden_name_with_spaces}" not allowed as column name(s): ' f"invalid identifier(s)"
    )
    with pytest.raises(ValueError, match=message):
        DataSet(dataframe)


def test_dataframes_on_datasets_cannot_have_columns_with_names_with_spaces_or_numbers():
    # given
    forbidden_name_with_spaces = "a b"
    forbidden_name_is_an_int = 0
    dataframe = pd.DataFrame(
        [[1, 2]], columns=[forbidden_name_with_spaces, forbidden_name_is_an_int]
    )
    message = re.escape(
        f'"{forbidden_name_is_an_int}", "{forbidden_name_with_spaces}" not allowed as column '
        f"name(s): invalid identifier(s)"
    )
    with pytest.raises(ValueError, match=message):
        DataSet(dataframe)


def test_column_names_can_be_accessed_as_attributes_of_dataset():
    # given
    dataframe = pd.DataFrame([[1], [2], [3]], columns=["one_value"])
    dataset = DataSet(dataframe)
    # then
    pd.testing.assert_series_equal(dataset.one_value, pd.Series([1, 2, 3], name="one_value"))
