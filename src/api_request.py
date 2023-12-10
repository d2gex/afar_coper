import logging
import pandas as pd
import xarray as xr
from typing import Dict, Any
from pathlib import Path
from motu_utils import motu_api
from src.motu_options import MotuOptions

logger = logging.getLogger()


class ApiRequest:

    def _request(self, data: Dict[str, Any]):
        success = False
        try:
            motu_api.execute_request(MotuOptions(data))
        except Exception as error:
            logger.error(f"An exception occurred: {type(error).__name__} – {error}")

        else:
            success = True
        return success

    def run(self, api_params: Dict[str, Any]) -> pd.DataFrame:
        is_data = self._request(api_params)
        if is_data is None:
            return None
        downloaded_path = Path(api_params['out_dir']) / api_params['out_name']
        ds = xr.open_dataset(downloaded_path)
        df = ds.to_dataframe()
        return df
