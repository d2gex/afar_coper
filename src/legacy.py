"""
This script runs a loop of motuclient command lines through a list of coordinates,
time and depth ranges via an input file (csv/xlsx).
"""
import os
import getpass
import pandas as pd

# User credentials
USERNAME = input("Enter your username: ")
PASSWORD = getpass.getpass("Enter your password: ")

# /!\ ONLY BLOCK TO MODIFY
# Define parameters
INPUT_FILE = "Black_Sea_2022.csv"
OUTDIR = "BKSEA_2022"
PRODUCT_ID = "BLKSEA_ANALYSISFORECAST_PHY_007_001"
PRODUCT_TYPE = "nrt"
DATASET_ID = "cmems_mod_blk_phy-sal_anfc_2.5km_P1D-m"
VARIABLE = "so"

# Create output directory if does not exist
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

# Read file with coordinates
extension = INPUT_FILE.split('.')[-1]
if extension == 'csv':
    df = pd.read_csv(INPUT_FILE)
elif extension == 'xlsx':
    df = pd.read_excel(INPUT_FILE)
else:
    raise NameError("Your file must be .csv or .xslx format.")

# TEST (optional): Uncoment both lines to do the download with the n first lines
# n = 3
# df = df.iloc[:n]

# Loop through rows of dataframe
for index, row in df.iterrows():
    # Get parameters
    lat = row['LAT']
    lon = row['LON']
    start = row['START']
    end = row['END']
    depth_min = row['DEPTH_MIN']
    depth_max = row['DEPTH_MAX']

    # Generate motuclient command line
    query = f'python -m motuclient --motu https://{PRODUCT_TYPE}.cmems-du.eu/motu-web/Motu --service-id {PRODUCT_ID}-TDS --product-id {DATASET_ID} \
    --longitude-min {lon} --longitude-max {lon} --latitude-min {lat} --latitude-max {lat} \
    --date-min "{start}" --date-max "{end}" --depth-min {depth_min} --depth-max {depth_max} --variable {VARIABLE} \
    --out-dir {OUTDIR} --out-name point{index}_{VARIABLE}.nc --user {USERNAME} --pwd {PASSWORD}'

    # Run the motu command
    os.system(query)