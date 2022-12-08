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
