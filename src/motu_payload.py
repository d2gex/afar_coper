from typing import Dict, Any
from datetime import datetime


class MotuPayloadGenerator:

    def __init__(self, data: Dict, payload: Dict[str, Any], output_filename: str):
        self.data = data
        self.payload = payload
        self.output_filename = output_filename
        self.area_details = []

    def _process_data_dict(self, _date: str, data: Dict) -> Dict[str, Any]:
        tokens = self.output_filename.split(".")
        product_details = {
            'latitude_min': data["latitude_min"],
            'longitude_min': data["longitude_min"],
            'latitude_max': data["latitude_max"],
            'longitude_max': data["longitude_max"],
            'depth_min': data["depth_min"],
            'depth_max': data["depth_max"],
            'out_name': f"{_date}_{tokens[0]}.{tokens[-1]}",
            'date_min': data['date_min'],
            'date_max': data['date_max'],
        }
        product_details.update(self.payload)
        return product_details

    def run(self):
        return {year: self._process_data_dict(year, data) for year, data in self.data.items()}
