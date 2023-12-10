import logging
import pandas as pd
import time
from motu_utils import motu_api
from src import config
from src.motu_options import MotuOptions
from src.motu_payload import MotuPayloadGenerator
from src.csv_parameter_splitter import CsvParameterSplitter
from src.api_request import ApiRequest
from src.nearest_point_finder import NearestDataframePointFinder

logger = logging.getLogger()

if __name__ == "__main__":

    start_time = time.time()

    # (1) Read input parameters
    input_data = pd.read_csv(config.DATA_PATH / config.INPUT_FILENAME)
    input_data['time'] = pd.to_datetime(input_data['time'], format='%d/%m/%Y %H:%M')

    # (2) Split inputs into daily records
    csv_proc = CsvParameterSplitter(input_data)
    api_params_by_dates = csv_proc.get_max_area_per_dates()
    df_by_dates = csv_proc.get_dataframes_split_by_dates()

    # (3) Create product folder and sub-folders
    ret_root_folder = config.OUTPUT_PATH / config.settings['service_id']
    ret_nc_folder = ret_root_folder / 'nc'
    ret_csv_folder = ret_root_folder / 'csv'
    ret_root_folder.mkdir(parents=True, exist_ok=True)
    ret_nc_folder.mkdir(parents=True, exist_ok=True)
    ret_csv_folder.mkdir(parents=True, exist_ok=True)

    # (3) Generate all payloads required to fetch the desired data
    common_payload = {
        'motu': config.settings['base_url'],
        "auth_mode": 'cas',
        'out_dir': str(ret_nc_folder),
        'user': config.COPERNICUS_USERNAME,
        'pwd': config.COPERNICUS_PASSWORD,
        'service_id': config.settings['service_id'],
        'product_id': config.settings['product_id'],
        'variable': config.settings['variables']
    }
    payload_generators = MotuPayloadGenerator(api_params_by_dates, common_payload, config.OUTPUT_FILENAME)
    motu_payloads = payload_generators.run()

    # (4) Fetch the actual data from Copernicus and merge into input parameters
    motu_requester = ApiRequest()
    full_results = pd.DataFrame()
    for _date, payload_data in motu_payloads.items():
        logger.info(
            f"------> Processing date = {_date} delimited by ({payload_data['longitude_min']},{payload_data['latitude_min']}) and "
            f"({payload_data['longitude_max']},{payload_data['latitude_max']})")
        ret_api_data = motu_requester.run(payload_data)
        if ret_api_data is None:
            logger.error("No data was returned. See log for further details")
        else:
            input_data = df_by_dates[_date]
            npf = NearestDataframePointFinder(input_data, ret_api_data, var_names=config.settings['variables'])
            partial_results = npf.find_and_merge()
            full_results = pd.concat([full_results, partial_results])
        logger.info("-------> END")
    full_results.to_csv(ret_csv_folder / 'results.csv')

    end_time = time.time()
    execution_time = start_time - end_time
    print("Data reading, api-fetching and processing time:", execution_time)
