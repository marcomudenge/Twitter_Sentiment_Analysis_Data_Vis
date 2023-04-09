'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np 
import re


def get_main_vis_data(stats):
    '''
        Prepare the data for the main visualisation.

        Args:
            stats: The stats dataframe to process
        Returns:
            The data frame to use in the main visualisation
            including the formatted columns index values and price 
            variations and product.
    '''   

    # create a copy of the dataframe
    stats_copy = stats.copy(True)

    # Calculate the variation of the index
    stats_copy['price_variation'] = stats_copy['price'].diff()

    # Rename the 'sum_influence_3_days' column to 'Activity'
    stats_copy.rename(columns={'sum_influence_3_days':'Activity'}, inplace=True)

    # Convert scale of the 'Activity' column from units to millions
    stats_copy['Activity']=(stats_copy['Activity']/1e6).round(1)

    # Round the index value to 2 decimals
    stats_copy['index_value']=stats_copy['index_value'].round(2)

    # Calculate the product of the price and index variation
    stats_copy['product'] = stats_copy['price_variation']*stats_copy['index_variation']

    return stats_copy

def get_bar_chart_data(stats):
    '''
        Prepare the data for the bar chart visualisation.

        Args:
            stats: The stats dataframe to process
        Returns:
            The data frame to use in the bar chart visualisation
            with the formatted columns.
    '''  
    # Split DF by index variation
    # TODO : Review the values
    df1 = stats[stats['index_variation'] > 0.5]
    df2 = stats.loc[(stats['index_variation'] >= -0.5) & (stats['index_variation'] <= 0.5)]
    df3 = stats[stats['index_variation'] < -0.5]

    # Group by ranges and count for each range
    # TODO : Can we use the same scale as in the main vis for the x axis? (6M instead of 60000000)
    ranges = [0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000]
    upper_df = df1.groupby(pd.cut(df1.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    middle_df = df2.groupby(pd.cut(df2.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    lower_df = df3.groupby(pd.cut(df3.sum_influence_3_days, ranges)).size().reset_index(name="Count")

    lower_df['Variation'] = 'Bearish'
    middle_df['Variation'] = 'Neutral'
    upper_df['Variation'] = 'Bullish'
    
    merged = pd.concat([lower_df, middle_df, upper_df])
    merged['sum_influence_3_days'] = merged['sum_influence_3_days'].astype(str).str.replace(r'[][()]+', '', regex=True)
    return merged

def get_radar_trend_data(df_tweets):
    '''
        From the given tweets dataframe, get
        the average variation for each hour.

        Args:
            df_tweets: The tweets dataframe to process
        Returns:
            The average variation for each hour including columns
            'hour', 'index_variation' and 'hour_angle'.
    '''

    # Only keep relevant columns
    mean_df = df_tweets.loc[:, ["timestamp", "index_variation"]]

    # Convert the hours from the timestamp
    mean_df['hour'] = mean_df['timestamp'].dt.hour

    # Keep only absolute values reflect movement
    mean_df['index_variation'] = mean_df['index_variation'].abs()

    # Get the average variation for each hour
    mean_df = mean_df.groupby('hour')['index_variation'].mean().reset_index()

    # Convert the hour to an angle
    mean_df['hour_angle'] = mean_df['hour'] * 15

    # Check if there are any missing hours
    missing_hours = [i for i in range(25) if i not in mean_df['hour'].unique()]

    # If there are missing hours, add them to the dataframe
    if 24 in missing_hours and 0 not in missing_hours:
        missing_hours_df = pd.DataFrame({'hour': 0, 
                                         'hour_angle': 0,
                                         'index_variation': mean_df.loc[mean_df['hour'] == 0]['index_variation']})
        mean_df = pd.concat([mean_df, missing_hours_df], ignore_index=True)

    return mean_df

def get_radar_scatter_data(df_tweets):
    '''
        From the given tweets dataframe, get scatter data
        for each non-negligeable variations per hour.

        Args:
            df_tweets: The tweets dataframe to process
        Returns:
            Scatter dataframe for hour variations including columns
            'hour', 'hour_angle', 'variation' and 'count'.
    '''   

    # Only keep relevant columns
    df = df_tweets.loc[:, ["timestamp","index_variation"]]

    # Convert the timestamp
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.date

    # OPTIONAL : consider only variations greater than 0.1
    df = df.loc[(df['index_variation'] > 0.01) | (df['index_variation'] < -0.01)]

    # Regroup by hour and index variation.
    # For instance, values 0.02 and 0.024 will be grouped together.
    # The index variations grouped for each interval of 0.01.
    df['index_range'] = pd.cut(df['index_variation'], bins=[-0.55+i*0.01 for i in range(101)])
    scatter_data = df.groupby(['hour', 'index_range']).size().reset_index(name='count')

    # Convert the hour to an angle
    scatter_data['hour_angle'] = scatter_data['hour'] * 15

    # Give a name to each interval
    scatter_data['variation'] = scatter_data['index_range'].apply(lambda x: x.left)

    # Remove the intervals with no data points
    scatter_data = scatter_data.loc[scatter_data['count'] != 0]
    
    return scatter_data

def convert_dates(df):
    '''
        Converts the dates in the dataframe to datetime objects.
        Creates new columns for the month, day and time.
        
        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d').dt.tz_localize(None)
    return df

def select_timeframe(df, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    df = df[(df['timestamp']<= end ) & (df['timestamp']>= start)]
    return df

def get_timeframe(df):
    '''
        Retrieve the earliest and latest dates in the dataframe.

        Args:
            dataframe: The dataframe to process
        Returns:
            The earliest (start) and latest (end) dates in the dataframe.
    '''
    start = df['timestamp'].min().strftime('%Y-%m-%d')
    end = df['timestamp'].max().strftime('%Y-%m-%d')
    return start,end