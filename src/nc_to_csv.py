import logging
import xarray as xr
from pathlib import Path

logger = logging.getLogger()


class NcToCsv:

    def __init__(self, nc_path: Path, csv_path: Path):
        self.nc_path = nc_path
        self.csv_path = csv_path

    def __call__(self, *args, **kwargs):
        nc_paths = [f for f in Path(self.nc_path).glob(str('*.nc'))]
        for _path in nc_paths:
            ds = xr.open_dataset(_path)
            df = ds.to_dataframe()
            csv_filename = f"{str(_path.stem)}.csv"
            abs_csv_path = self.csv_path / csv_filename
            df.to_csv(abs_csv_path)
