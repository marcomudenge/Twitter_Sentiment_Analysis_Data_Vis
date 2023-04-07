
import pandas as pd

"""
    Density: Split index_variation (-1 to +1) into regions. The density is number of times we get a value within each 
    boundary divided by total number of values for each hour. 
"""

def convert_dataframe(dataframe):
    df = dataframe.loc[:, ["timestamp", "index_variation"]]
    df['timestamp'] = df['timestamp'].apply(lambda x: pd.to_datetime(x).strftime('%H'))
    return df
