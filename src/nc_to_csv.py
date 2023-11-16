import logging

import pandas as pd
import xarray as xr
import os
from pathlib import Path

logger = logging.getLogger()


class NcToCsv:

    def __init__(self, nc_path: Path, csv_path: Path):
        self.nc_path = nc_path
        self.csv_path = csv_path

    def _to_csv(self):
        '''Convert all .nc files in a given directory to csv
        '''
        nc_paths = [f for f in Path(self.nc_path).glob(str('*.nc'))]
        for _path in nc_paths:
            ds = xr.open_dataset(_path)
            df = ds.to_dataframe()
            csv_filename = f"{str(_path.stem)}.csv"
            abs_csv_path = self.csv_path / csv_filename
            df.to_csv(abs_csv_path)

    def _amalgamate_csvs(self) -> pd.DataFrame:
        '''Amalgamate all partial csv files in a given directory into a single dataframe
        '''
        csv_paths = [f for f in Path(self.csv_path).glob(str('*.csv'))]
        single_csv_df = pd.DataFrame()
        for _path in csv_paths:
            df = pd.read_csv(_path)
            single_csv_df = single_csv_df.append(df, ignore_index=True)
        return single_csv_df

    def _build_result(self, result: pd.DataFrame):
        '''Amalgamate and delete all csv files from a directory into a dataframe and create a single file
        '''
        single_csv_file_path = f"{str(self.csv_path.parents[0] / self.csv_path.stem)}.csv"
        result.write_csv(single_csv_file_path)
        Path(self.csv_path).rmdir()

    def run(self):
        self._to_csv()
        result = self._amalgamate_csvs()
        self._build_result(result)

