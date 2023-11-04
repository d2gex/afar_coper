import os
from pathlib import Path
from dotenv import load_dotenv

file_path = Path(__file__).resolve()
ROOT_PATH = file_path.parents[1]
DATA_PATH = ROOT_PATH / 'data'
OUTPUT_PATH = DATA_PATH / 'output'
CSV_PATH = OUTPUT_PATH / 'csv'
NC_PATH = OUTPUT_PATH / 'nc'

dot_env = load_dotenv(ROOT_PATH / '.env')
BASE_URL = 'http://my.cmems-du.eu/motu-web/Motu'
COMPERNICUS_USERNAME = os.getenv('COMPERNICUS_USERNAME')
COMPERNICUS_PASSWORD = os.getenv('COMPERNICUS_PASSWORD')


