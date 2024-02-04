import logging
import pandas as pd
import xarray as xr
from typing import Dict, Any
from pathlib import Path
from copernicusmarine import subset

logger = logging.getLogger()


class DataRequest:

    def _request(self, data: Dict[str, Any], force_download=True):
        success = False
        data.update({'force_download': force_download})
        try:
            subset(**data)
        except Exception as error:
            logger.error(f"An exception occurred: {type(error).__name__} – {error}")

        else:
            success = True
        return success

    def fetch_from_net(self, api_params: Dict[str, Any]) -> pd.DataFrame:
        is_data = self._request(api_params)
        if is_data is False:
            return None
        downloaded_path = Path(api_params['output_directory']) / api_params['output_filename']
        ds = xr.open_dataset(downloaded_path)
        df = ds.to_dataframe()
        df = df.reset_index()
        return df

    def fetch_from_disk(self, api_params: Dict[str, Any]) -> pd.DataFrame:
        read_path = Path(api_params['output_directory']) / api_params['output_filename']
        try:
            ds = xr.open_dataset(read_path)
        except Exception as error:  # Not best solution. Exception should be highly specific
            df = None
            logger.error(f"An exception occurred: {type(error).__name__} – {error}")
        else:
            df = ds.to_dataframe()
            df = df.reset_index()
        return df
