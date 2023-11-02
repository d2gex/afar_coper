import logging
from src import config
from motu_utils import motu_api
from datetime import datetime
from cmemsapi import cmemsapi

class MotuOptions:
    def __init__(self, attrs: dict):
        super().__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None


# motu_payload = {
#     'motu': config.BASE_URL,
#     "auth_mode": 'cas',
#     'out_dir': str(config.DATA_PATH),
#     'user': config.COMPERNICUS_USERNAME,
#     'pwd': config.COMPERNICUS_PASSWORD
# }
#
# product_details = {
#     'latitude_min': 35.875,
#     'longitude_min': -8.9875,
#     'latitude_max': 42.99055556,
#     'longitude_max': 5.98694444,
#     'depth_min': 0.49402499198913574,
#     'depth_max': 0.49402499198913574,
#     'out_name': "result.nc",
#     'date_min': datetime.strptime("2020-11-15 00:00:00", '%Y-%m-%d %H:%M:%S'),
#     'date_max': datetime.strptime("2020-11-16 00:00:00", '%Y-%m-%d %H:%M:%S'),
#     'service_id': 'GLOBAL_MULTIYEAR_PHY_001_030-TDS',
#     'product_id': 'cmems_mod_glo_phy_my_0.083_P1D-m',
#     'variable': ["thetao", "zos"]
# }
#
# # L3 product details: large image of Spanish Mediterrenean
# logging.basicConfig(level=logging.DEBUG)
# motu_payload.update(product_details)
# motu_api.execute_request(MotuOptions(motu_payload))

with open(config.DATA_PATH / 'test.nc') as f:
    cmemsapi.to_csv(f, config.DATA_PATH / 'test.csv')
