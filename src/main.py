import logging
import pandas as pd
import time
import shutil
from src import config
from src.payload_generator import CpmtbPayloadGenerator
from src.csv_parameter_splitter import CsvParameterSplitter
from src.data_grabber_processor import DataGrabberAndProcessor

logger = logging.getLogger()

if __name__ == "__main__":

    start_time = time.time()

    # (1) Read input parameters
    input_data = pd.read_csv(config.DATA_PATH / config.INPUT_FILENAME)
    input_data['time'] = pd.to_datetime(input_data['time'], format='%d/%m/%Y %H:%M')

    # (2) Split inputs into daily records
    csv_proc = CsvParameterSplitter(input_data,
                                    min_year=config.settings['years'][0],
                                    max_year=config.settings['years'][-1],
                                    time_offset=config.settings['time_offset'])
    api_params_by_dates = csv_proc.get_min_max_boundaries_per_dates()
    df_by_dates = csv_proc.get_dataframes_split_by_dates()

    # (3) Create product folder and sub-folders
    ret_root_folder = config.OUTPUT_PATH / config.settings['dataset_id']
    ret_nc_folder = ret_root_folder / 'nc'
    ret_csv_folder = ret_root_folder / 'csv'

    if ret_root_folder.exists() and config.settings['start_mode'] == 0:
        shutil.rmtree(ret_root_folder)
    ret_root_folder.mkdir(parents=True, exist_ok=True)
    ret_nc_folder.mkdir(parents=True, exist_ok=True)
    ret_csv_folder.mkdir(parents=True, exist_ok=True)

    # (3) Generate all payloads required to fetch the desired data
    common_payload = {
        'output_directory': str(ret_nc_folder),
        'dataset_id': config.settings['dataset_id'],
        'variables': config.settings['variables']
    }

    payload_generators = CpmtbPayloadGenerator(api_params_by_dates, common_payload, config.OUTPUT_FILENAME)
    payloads = payload_generators.run()
    start_mode = config.settings['start_mode']
    params = {
        'input_by_dates': df_by_dates,
        'variables': config.settings['variables'],
        'nc_folder': ret_nc_folder,
        'csv_folder': ret_csv_folder,
        'payloads': payloads,
    }
    if start_mode == 1:
        year_sequence = [x for x in range(config.settings['years'][0], config.settings['years'][-1] + 1)]
        params.update({'pattern_to_remove': year_sequence})

    processor = DataGrabberAndProcessor(**params)
    # Fetch all data first if we do not have them yet in the hard disk
    if start_mode != 2:
        processor.fetch_all_data()
    # ... The process it ...
    data = processor.process_all_data()
    # ... And finfally store it.
    data.to_csv(ret_csv_folder / f"{config.settings['dataset_id']}.csv")

    end_time = time.time()
    execution_time = start_time - end_time
    print("Data reading, api-fetching and processing time:", execution_time)
