import pandas as pd
from typing import Dict, Any
from datetime import datetime


class MotuPayloadGenerator:

    def __init__(self, data: pd.DataFrame, payload: Dict[str, Any], output_filename: str):
        self.data = data
        self.payload = payload
        self.output_filename = output_filename
        self.area_details = []

    def _process_row(self, row):
        tokens = self.output_filename.split(".")
        product_details = {
            'latitude_min': row["latitude_min"],
            'longitude_min': row["longitude_min"],
            'latitude_max': row["latitude_max"],
            'longitude_max': row["longitude_max"],
            'depth_min': row["depth_min"],
            'depth_max': row["depth_max"],
            'out_name': f"f{tokens[0]}_{row['ID']}.{tokens[-1]}",
            'date_min': datetime.strptime(row["date_min"], '%d/%m/%Y %H:%M'),
            'date_max': datetime.strptime(row["date_max"], '%d/%m/%Y %H:%M'),
        }
        product_details.update(self.payload)
        return product_details

    def run(self):
        return {row['ID']: self._process_row(row) for _, row in self.data.iterrows()}
