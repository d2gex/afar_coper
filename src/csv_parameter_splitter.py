import pandas as pd
from typing import Dict, Union
from datetime import datetime, timedelta


class CsvParameterSplitter:

    def __init__(self, data: pd.DataFrame, min_year: int, max_year: int):
        self.data = data
        self.min_year = min_year
        self.max_year = max_year

    def _cap_data_frame_by_min_max_date(self, data: pd.DataFrame) -> pd.DataFrame:
        _data = data.copy()
        _data['year'] = data.time.dt.year
        _data = _data[(_data['year'] >= self.min_year) & (_data['year'] <= self.max_year)]
        _data = _data.drop(columns=['year'])
        return _data

    def _split_csv_per_day(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        return {str(_date.strftime('%Y-%m-%d_%H-%M-%S')): df for _date, df in data.groupby('time')}

    def _get_max_bounding_box(self, data: pd.DataFrame) -> Dict[str, float]:
        return {
            'longitude_min': min(data['lon']),
            'longitude_max': max(data['lon']),
            'latitude_min': min(data['lat']),
            'latitude_max': max(data['lat'])
        }

    def _get_min_max_date(self, data: pd.DataFrame) -> Dict[str, datetime]:
        start_date = (set(data.time)).pop()
        end_date = start_date + timedelta(hours=23, minutes=59, seconds=59)
        return {
            'date_min': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'date_max': end_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def _get_min_max_depth(self, data: pd.DataFrame) -> Dict[str, datetime]:
        return {
            'depth_min': min(data['depth']),
            'depth_max': max(data['depth'])
        }

    def get_min_max_boundaries_per_dates(self) -> Dict[str, Dict]:
        _data = self._cap_data_frame_by_min_max_date(self.data)
        df_by_days = self._split_csv_per_day(_data)
        boundaries_data = {}
        for _date, df in df_by_days.items():
            coords = self._get_max_bounding_box(df)
            dates = self._get_min_max_date(df)
            depths = self._get_min_max_depth(df)
            coords.update(**dates, **depths)
            boundaries_data[_date] = coords
        return boundaries_data

    def get_dataframes_split_by_dates(self) -> Dict[str, pd.DataFrame]:
        _data = self._cap_data_frame_by_min_max_date(self.data)
        return self._split_csv_per_day(_data)
