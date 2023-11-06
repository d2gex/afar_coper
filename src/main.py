import logging
import pandas as pd
import xarray as xr
from src import config
from src.motu_options import MotuOptions
from src.motu_payload import MotuPayloadGenerator
from motu_utils import motu_api

if __name__ == "__main__":
    input_data = pd.read_csv(config.DATA_PATH / config.INPUT_FILENAME)
    common_payload = {
        'motu': config.BASE_URL,
        "auth_mode": 'cas',
        'out_dir': str(config.NC_PATH),
        'user': config.COMPERNICUS_USERNAME,
        'pwd': config.COMPERNICUS_PASSWORD
    }
    payload_generators = MotuPayloadGenerator(input_data, common_payload, config.INPUT_FILENAME)
    motu_payloads = payload_generators.run()
    for paylod in motu_payloads:
        print("")
        motu_api.execute_request(MotuOptions(motu_payloads))
        print("")
#
#
# product_details = {
#     'latitude_min': 35.875,
#     'longitude_min': -8.9875,
#     'latitude_max': 42.99055556,
#     'longitude_max': 5.98694444,
#     'depth_min': 0.49402499198913574,
#     'depth_max': 0.49402499198913574,
#     'out_name': "result.nc",
#     'date_min': datetime.strptime("2020-12-31 00:00:00", '%Y-%m-%d %H:%M:%S'),
#     'date_max': datetime.strptime("2020-12-31 23:59:59", '%Y-%m-%d %H:%M:%S'),
#     'service_id': 'GLOBAL_MULTIYEAR_PHY_001_030-TDS',
#     'product_id': 'cmems_mod_glo_phy_my_0.083_P1D-m',
#     'variable': ["thetao", "zos"]
# }
#
# # L3 product details: large image of Spanish Mediterrenean
# logging.basicConfig(level=logging.DEBUG)
# motu_payload.update(product_details)
# motu_api.execute_request(MotuOptions(motu_payload))
#
# ds = xr.open_dataset(config.DATA_PATH / 'result.nc')
# df = ds.to_dataframe()
# df.to_csv(config.DATA_PATH / 'result.csv')