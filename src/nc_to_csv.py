import logging
import pandas as pd
import xarray as xr
from pathlib import Path

logger = logging.getLogger()


class NcToCsv:

    @staticmethod
    def read_and_convert(nc_path: Path, csv_path: Path):
        nc_paths = [f for f in Path(nc_path).glob(str('*.nc'))]
        for _path in nc_paths:
            ds = xr.open_dataset(_path)
            df = ds.to_dataframe()
            df = df.reset_index()
            csv_filename = f"{str(_path.stem)}.csv"
            abs_csv_path = csv_path / csv_filename
            df.to_csv(abs_csv_path)

    @staticmethod
    def read_and_merge(nc_path: Path) -> pd.DataFrame:
        full_df = pd.DataFrame()
        nc_paths = [f for f in Path(nc_path).glob(str('*.nc'))]
        for _path in nc_paths:
            ds = xr.open_dataset(_path)
            df = ds.to_dataframe()
            df = df.reset_index()
            full_df = pd.concat([full_df, df])
        return full_df
