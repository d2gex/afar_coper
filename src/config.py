import os
import tomli
from pathlib import Path
from dotenv import load_dotenv

file_path = Path(__file__).resolve()
ROOT_PATH = file_path.parents[1]
DATA_PATH = ROOT_PATH / 'data'
OUTPUT_PATH = DATA_PATH / 'output'
CSV_PATH = OUTPUT_PATH / 'csv'
NC_PATH = OUTPUT_PATH / 'nc'

dot_env = load_dotenv(ROOT_PATH / '.env')
with open(ROOT_PATH / 'setup.toml', mode="rb") as fp:
    config = tomli.load(fp)

BASE_URL = config['base_url']
INPUT_FILENAME = config['input_file']
OUTPUT_FILENAME = config['output_file']
COMPERNICUS_USERNAME = os.getenv('COMPERNICUS_USERNAME')
COMPERNICUS_PASSWORD = os.getenv('COMPERNICUS_PASSWORD')


