import numpy as np
import pytest
import pandas as pd
from src.nearest_point_finder import NearestDataframePointFinder
from unittest.mock import Mock


@pytest.fixture
def input_data():
    return pd.DataFrame(data={
        'ID': ['ah1', 'ah2'],
        'lon': [-8.72160104, -8.87530272],
        'lat': [41.13403419, 40.90328471],
    })


@pytest.fixture
def result_data():
    ''' Dataframe representing the results obtained from Copernicus. The closest point in the resulted dataset to those
    in the inputs is point = (-8.75, 40.416668)
    '''
    return pd.DataFrame(data={
        'variable1': ['value_1', 'value_2', 'value_3'],
        'variable2': ['value_11', 'value_22', 'value_33'],
        'longitude': [-8.75, -8.75, -16.666666],
        'latitude': [32.666668, 40.416668, 40.416668],
    })


def test__build_array_of_coordinates(result_data):
    npf = NearestDataframePointFinder(Mock(), Mock(), Mock())
    ret = npf._build_array_of_coordinates(result_data, col_lon='longitude', col_lat='latitude')
    expected = np.array([[-8.75, 32.666668], [-8.75, 40.416668], [-16.666666, 40.416668]])
    np.testing.assert_array_equal(ret, expected)


def test__calculate_distances_between_arrays(input_data, result_data):
    npf = NearestDataframePointFinder(Mock(), Mock(), Mock())
    input_array = npf._build_array_of_coordinates(input_data, col_lon='lon', col_lat='lat')
    result_array = npf._build_array_of_coordinates(result_data, col_lon='longitude', col_lat='latitude')
    ret = npf._calculate_distances_between_arrays(input_array, result_array)
    assert len(ret) == 2
    assert all(len(x) == 3 for x in ret)


def test__find_offset_closest_coordinates(input_data, result_data):
    npf = NearestDataframePointFinder(Mock(), Mock(), Mock())
    input_array = npf._build_array_of_coordinates(input_data, col_lon='lon', col_lat='lat')
    result_array = npf._build_array_of_coordinates(result_data, col_lon='longitude', col_lat='latitude')
    distances = npf._calculate_distances_between_arrays(input_array, result_array)
    ret = npf._find_offset_closest_coordinates(distances)
    assert len(input_data) == len(ret)
    np.testing.assert_array_equal(ret, np.array([1, 1]))


def test_find_and_merge(input_data, result_data):
    npf = NearestDataframePointFinder(input_data, result_data, var_names=['variable1', 'variable2'])
    ret = npf.find_and_merge()
    expected_df = pd.DataFrame(data={
        'ID': ['ah1', 'ah2'],
        'lon': [-8.721601, -8.875303],
        'lat': [41.134034, 40.903285],
        'variable1': ['value_2', 'value_2'],
        'variable2': ['value_22', 'value_22']
    })
    pd.testing.assert_frame_equal(ret, expected_df)
