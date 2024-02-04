import logging
from pathlib import Path
from typing import Dict, List, Optional
from src.api_request import DataRequest
from src.nearest_point_finder import NearestDataframePointFinder
from src.nc_to_csv import NcToCsv

logger = logging.getLogger()


class DataProcessor:

    def __init__(self, nc_folder: Path, csv_folder: Path, payloads: Dict[str, Dict],
                 years_to_remove: Optional[List[int]] = None):
        self.nc_folder = nc_folder
        self.csv_folder = csv_folder
        self.payloads = payloads
        self.years_to_remove = years_to_remove

    def _delete_year_files(self):
        for year in self.years_to_remove:
            paths_to_delete = list(Path(self.nc_folder).glob(f"{year}*.nc"))
            if paths_to_delete:
                logger.warning(f"Deleting all previously downloaded files for year {year}")
                for p in paths_to_delete:
                    p.unlink()

    def fetch_all_data(self):

        # Delete all file from within the given yearly interval if given so
        if self.years_to_remove is not None:
            self._delete_year_files()

        data_request = DataRequest()
        for _date, payload_data in self.payloads.items():
            logger.info(
                f"------> Processing date = {_date} delimited by ({payload_data['minimum_longitude']},"
                f"{payload_data['minimum_latitude']}) and "
                f"({payload_data['maximum_longitude']},{payload_data['minimum_latitude']})")
            ret_api_data = data_request.fetch_from_net(
                payload_data)
            if ret_api_data is None:
                logger.error("No data was returned. See log for further details")
