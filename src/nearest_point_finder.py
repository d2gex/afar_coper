import pandas as pd
import numpy as np
from scipy.spatial import distance
from typing import Optional, List


class NearestDataframePointFinder:

    def __init__(self, input_points: pd.DataFrame, result_points: pd.DataFrame, var_names: List[str],
                 dist_type: Optional[str] = 'euclidean'):
        self.input_points = input_points
        self.result_points = result_points
        self.var_names = var_names
        self.dist_type = dist_type

    def _build_array_of_coordinates(self, data: pd.DataFrame, col_lon, col_lat) -> np.ndarray:
        '''Build an array of coordinates with the longitude and latitude columns of a dataframe. The
        length is that of the dataframe
        '''
        return np.array(list(zip(data[col_lon], data[col_lat])))

    def _calculate_distances_between_arrays(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        '''Calculate the distance between the coordinates in a and those in b. The resulting array will
        have len(a) sub-arrays and each sub-array will hold len(b) values. Each value represents the distance
        between an element in a and all elements in b.
        '''
        return distance.cdist(a, b, self.dist_type)

    def _find_offset_closest_coordinates(self, distances: np.ndarray) -> np.ndarray:
        '''Given an array of sub-arrays, it builds an array which dimension is the number of sub-arrays. Each
        value of the resulting array is the index of the shortest distance found in each sub-array, relative to its
        dimension, i.e, if sub-array has 10 elements and the shortest distance is the 8th, the value returned for that
        sub-array will be 7.
        '''
        df = pd.DataFrame(list(zip(*distances)))
        df.ID = [x for x in range(len(df))]
        return df.idxmin().values

    def find_and_merge(self) -> pd.DataFrame:
        '''Find the closest points between two dataframes a and b, and merge all columns from b into a. The number of
        rows of the resulting dataframes is len(a); the columns though, is all that are in a + those in b that are not
        coordinates.
        '''
        self.result_points['min_idx'] = [x for x in range(len(self.result_points))]
        input_array = self._build_array_of_coordinates(self.input_points, col_lon='lon', col_lat='lat')
        result_array = self._build_array_of_coordinates(self.result_points, col_lon='longitude', col_lat='latitude')
        distances = self._calculate_distances_between_arrays(input_array, result_array)
        min_distance_offsets = self._find_offset_closest_coordinates(distances)
        self.input_points['min_idx'] = min_distance_offsets
        closest_point_variables = pd.merge(self.input_points, self.result_points[self.var_names + ['min_idx']],
                                           on=['min_idx'])
        closest_point_variables = closest_point_variables.drop('min_idx', axis=1)
        return closest_point_variables
