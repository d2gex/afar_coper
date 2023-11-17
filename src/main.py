import logging
import pandas as pd
from src import config
from src.csv_processor import CsvProcessor
from src.api_request import ApiRequestMultipleThreads

logger = logging.getLogger()

if __name__ == "__main__":
    # Build common payload for motu client
    common_payload = {
        'motu': config.settings['base_url'],
        "auth_mode": 'cas',
        'out_dir': str(config.NC_PATH),
        'user': config.COPERNICUS_USERNAME,
        'pwd': config.COPERNICUS_PASSWORD,
        'service_id': config.settings['service_id'],
        'product_id': config.settings['product_id'],
        'variable': config.settings['variables'],
        'socket_timeout': config.settings['socket_timeout']
    }

    # Read input csv with details for the API requests
    input_data = pd.read_csv(config.DATA_PATH / config.INPUT_FILENAME)
    input_data['time'] = pd.to_datetime(input_data['time'], format='%Y-%m-%d %H:%M:%S')
    c_processor = CsvProcessor(input_data)
    dfs = c_processor.run()

    # Delete csvs from any run earlier on
    for filename in config.CSV_PATH.glob("*.csv"):
        filename.unlink()

    # Fetch all details by years and by a batch of a number of requests at once
    for year, year_details in dfs['yearly_data'].items():
        data = {year: year_details}
        message = f"############### Fetching all details for year {year}"
        print(message)
        logger.info(message)
        a_request = ApiRequestMultipleThreads(data, common_payload, config.OUTPUT_FILENAME, batch_num_calls=200)
        a_request.run(max_iterations=200)
        message = f"############### End ({year})"
        print(message)
        logger.info(message)
