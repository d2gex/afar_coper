import pandas as pd
from typing import Dict, Any, Optional
from datetime import timedelta


class MotuPayloadGenerator:

    def __init__(self, data: pd.DataFrame, payload: Dict[str, Any], output_filename: str,
                 days_offset: Optional[int] = 1):
        self.data = data
        self.payload = payload
        self.output_filename = output_filename
        self.area_details = []
        self.days_offset = days_offset

    def _process_row(self, row):
        tokens = self.output_filename.split(".")
        product_details = {
            'latitude_min': row["lat"],
            'longitude_min': row["lon"],
            'latitude_max': row["lat"],
            'longitude_max': row["lon"],
            'depth_min': row["depth"],
            'depth_max': row["depth"],
            'out_name': f"{row['ID']}_{tokens[0]}.{tokens[-1]}",
            'date_min': row['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'date_max': (row['time'] + timedelta(days=self.days_offset)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        product_details.update(self.payload)
        return product_details

    def run(self):
        return [self._process_row(row) for _, row in self.data.iterrows()]
