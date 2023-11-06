import logging
import sys
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
    settings = tomli.load(fp)

INPUT_FILENAME = settings['input_filename']
OUTPUT_FILENAME = settings['output_filename']
COPERNICUS_USERNAME = os.getenv('COPERNICUS_USERNAME')
COPERNICUS_PASSWORD = os.getenv('COPERNICUS_PASSWORD')

# Log to the output and into a file
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler(ROOT_PATH / 'motu_calls.log', mode='w')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
