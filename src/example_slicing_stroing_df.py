import pandas as pd
from numpy import array_equal
from typing import List, Optional
from pydap.client import open_url

open_url()


def fetch_sequence(df: pd.DataFrame, from_row: int, seq_len: int,
                   columns: Optional[List] = None) -> pd.DataFrame:
    '''
    Fetch a chunk of data off a dataframe from a given offset and return the columns provided as a parameter
    :param df: input dataframe
    :param from_row: row when the sequence starts
    :param seq_len: length of sequence the dataframe will be sliced by each time
    :param columns: array of column names to extract from the dataframe
    :return: Chunk of length from dataframe
    '''
    if from_row >= len(df):  # Are we at the end?
        return pd.DataFrame()

    to_row = from_row + seq_len - 1
    if to_row > len(df):
        to_row = len(df)
    if columns is None:
        ret = df.loc[from_row:to_row, ]
    else:
        ret = df.loc[from_row:to_row, columns]
    return ret.reset_index()


if __name__ == "__main__":
    row_data = [x for x in range(10000)]
    test_df = pd.DataFrame({  # TODO: This should be your dataframe with 160k rows
        'a': row_data,
        'b': reversed(row_data),
        'c': [x + 100 for x in row_data]
    })

    start_row = 0  # Initial row the first sliced chunk starts at
    seq_len = 534  # length of the sequence you want to explore at once. Define the value as appropriate
    columns = ['b', 'c']  # Name of colums you want to fetch from the dataframe
    num_iterations = (len(test_df) // seq_len) + 1  # Ensure the loop doesn't run indefinitely
    fetched_var_name = 'result'  # Replace this variable with the name of the column in your final dataframe
    result_df = pd.DataFrame({fetched_var_name: []})

    for i in range(num_iterations + 1):

        # TODO: Make a call to open your dataset here at each iteration so that a new session is created.
        # By creating a new session, the old one is normally closed as shown by the code of the
        # setup_session here (this could do the trick however terrible it is):
        # https://github.com/pydap/pydap/blob/a330c563c2396c98271fda699c07ab05b7a472b3/src/pydap/cas/get_cookies.py#L14
        # Example: SSH20_22_daily = copernicusmarine_datastore(DATASET_ID, USERNAME, PASSWORD)
        # Example: SSH20_22_daily = xr.open_dataset(SSH20_22_daily)

        fetched_details = []
        df_chunk = fetch_sequence(test_df, start_row, seq_len, columns)
        if df_chunk.empty:
            print("The script has finished")
            break
        print(f"Running iteration : {i + 1} for a chunk of length {len(df_chunk)}")
        try:  # you make your api call here
            for j in range(len(df_chunk)):
                fetched_value = df_chunk.loc[j, 'b']  # TODO: Replace this line with your actual api call
                fetched_details.append(fetched_value)
        except Exception as e:  # this error catch is to show you where the start again the next time
            print(f"The script crashed at offset '{(i * seq_len) + j}', iteration '{i}' and "
                  f"start_row {start_row}.You need this information to start again. Adjust num_iterations too.")
            raise
        else:  # move the start offset forward
            start_row = ((i + 1) * seq_len)
        finally:  # No matter what, append and store the results. "finally" statement guarantees that
            result_df = pd.concat([result_df, pd.DataFrame({fetched_var_name: fetched_details})], ignore_index=True)
            # TODO: Store your result dataframe with result.to_csv here just in case the whole thing crash.
            # There will be ever only one file as you are appending the results.


    # Irrelevant for your script. Just remove it as this is only a test
    assert len(result_df) == len(test_df)
    assert array_equal(result_df[fetched_var_name].values, test_df.b.values)

    # Lastly, attach the column in your result dataframe to your existing one
    test_df = test_df.assign(whatever_name=result_df[fetched_var_name].values)
    assert array_equal(result_df[fetched_var_name].values, test_df.whatever_name.values) # remove this line
