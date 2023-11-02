from pathlib import Path

file_path = Path(__file__).resolve()
ROOT_PATH = file_path.parents[1]
DATA_PATH = file_path.parents[3] / 'repos_data' / 'Points_habitat_time_position2.csv'


