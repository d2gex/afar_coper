import pandas as pd
from typing import Dict, Any
from pathlib import Path
from motu_utils import motu_api
from src import config
from src.motu_payload import MotuPayloadGenerator
from src.motu_options import MotuOptions
from src.nc_to_csv import NcToCsv


class ApiRequest:

    def __init__(self, data: Dict[str, pd.DataFrame], common_payload: Dict[str, Any], output_filename: str):
        self.data = data
        self.common_payload = dict(common_payload)
        self.output_filename = output_filename
        self.year = self.data.keys()[0]

    def _create_dest_folder(self) -> Path:
        root_folder = Path(self.common_payload['out_dir'])
        dest_folder = root_folder / self.year
        dest_folder.mkdir(parents=True, exist_ok=True)
        return dest_folder

    def _build_result(self):
        # Convert all nc files to csv
        nc_folder = (config.NC_PATH / self.year)
        csv_folder = (config.CSV_PATH / self.year)
        nc_to_csv_processor = NcToCsv(nc_folder, csv_folder)
        nc_to_csv_processor.run()

    def _download_data(self):
        motu_payload_gen = MotuPayloadGenerator(self.data[self.year], self.common_payload, self.output_filename)
        motu_payloads = motu_payload_gen.run()
        for _id, payload_data in motu_payloads.items():
            motu_api.execute_request(MotuOptions(payload_data))

    def run(self):
        dest_folder = self._create_dest_folder()
        self.common_payload['out_dir'] = str(dest_folder)
        self._download_data()
        self._build_result()
