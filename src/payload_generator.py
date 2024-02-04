from typing import Dict, Any


class CpmtbPayloadGenerator:

    def __init__(self, data: Dict, payload: Dict[str, Any], output_filename: str):
        self.data = data
        self.payload = payload
        self.output_filename = output_filename
        self.area_details = []

    def _process_data_dict(self, _date: str, data: Dict) -> Dict[str, Any]:
        tokens = self.output_filename.split(".")
        product_details = {
            'minimum_latitude': data["latitude_min"],
            'minimum_longitude': data["longitude_min"],
            'maximum_latitude': data["latitude_max"],
            'maximum_longitude': data["longitude_max"],
            'minimum_depth': data["depth_min"],
            'maximum_depth': data["depth_max"],
            'output_filename': f"{_date}_{tokens[0]}.{tokens[-1]}",
            'start_datetime': data['date_min'],
            'end_datetime': data['date_max'],
        }
        product_details.update(self.payload)
        return product_details

    def run(self) -> Dict[str, Dict]:
        return {_date: self._process_data_dict(_date, data) for _date, data in self.data.items()}
