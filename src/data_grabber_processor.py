import logging
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional
from src.api_request import DataRequest
from src.nearest_point_finder import NearestDataframePointFinder

logger = logging.getLogger()


class DataGrabberAndProcessor:

    def __init__(self, input_by_dates: pd.DataFrame, variables: List[str], nc_folder: Path, csv_folder: Path,
                 payloads: Dict[str, Dict],
                 pattern_to_remove: Optional[List[int]] = None):
        self.input_by_dates = input_by_dates
        self.variables = variables
        self.nc_folder = nc_folder
        self.csv_folder = csv_folder
        self.payloads = payloads
        self.pattern_to_remove = pattern_to_remove
        self.data_request = DataRequest()

    def _delete_pattern_files(self):
        for pattern in self.pattern_to_remove:
            paths_to_delete = list(Path(self.nc_folder).glob(f"{pattern}*.nc"))
            if paths_to_delete:
                logger.warning(f"Deleting all previously downloaded files for year {pattern}")
                for p in paths_to_delete:
                    p.unlink()

    def fetch_all_data(self):

        # Delete all file from within the given yearly interval if given so
        if self.pattern_to_remove is not None:
            self._delete_pattern_files()

        for _date, payload_data in self.payloads.items():
            logger.info(
                f"------> Fetching date = {_date} delimited by ({payload_data['minimum_longitude']},"
                f"{payload_data['minimum_latitude']}) and "
                f"({payload_data['maximum_longitude']},{payload_data['minimum_latitude']})")
            ret_api_data = self.data_request.fetch_from_net(
                payload_data)
            if ret_api_data is None:
                logger.error("No data was returned. See log for further details")

    def process_all_data(self):
        full_results = pd.DataFrame()
        for _date, payload_data in self.payloads.items():
            logger.info(
                f"------> Processing date = {_date} delimited by ({payload_data['minimum_longitude']},"
                f"{payload_data['minimum_latitude']}) and "
                f"({payload_data['maximum_longitude']},{payload_data['minimum_latitude']})")
            ret_api_data = self.data_request.fetch_from_disk(
                payload_data)
            if ret_api_data is None:
                logger.error("No data was read. See log for further details")
            else:
                input_data = self.input_by_dates[_date]
                npf = NearestDataframePointFinder(input_data, ret_api_data, var_names=self.variables)
                try:
                    partial_results = npf.find_and_merge()
                except KeyError:
                    logger.exception(f"File{Path(payload_data['output_directory']) / payload_data['output_filename']} "
                                     f"did not have the expected structure")
                else:
                    full_results = pd.concat([full_results, partial_results])
        return full_results
