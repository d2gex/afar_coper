import logging
import pandas as pd
import xarray as xr
from typing import Dict, Any
from pathlib import Path
from copernicus_marine_client import subset

logger = logging.getLogger()


class ApiRequest:

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

    def run(self, api_params: Dict[str, Any]) -> pd.DataFrame:
        is_data = self._request(api_params)
        if is_data is None:
            return None
        downloaded_path = Path(api_params['output_directory']) / api_params['output_filename']
        ds = xr.open_dataset(downloaded_path)
        df = ds.to_dataframe()
        df = df.reset_index()
        return df
