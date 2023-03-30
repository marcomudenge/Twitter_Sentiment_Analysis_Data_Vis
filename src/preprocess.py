import pandas as pd
stats = pd.read_csv('assets/df_stats.csv')
tweets = pd.read_csv('assets/df_tweets.csv')

def stats_vis3(stats):
    # Split DF by index value
    df1 = stats[stats['index_value'] > 0.5]
    df2 = stats[stats['index_value'] < -0.5]
    df3 = stats.loc[(stats['index_value'] >= -0.5) & (stats['index_value'] <= 0.5)]

    # Group by ranges and count for each range
    ranges = [0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000]
    upper_df = df1.groupby(pd.cut(df1.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    middle_df = df2.groupby(pd.cut(df2.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    lower_df = df3.groupby(pd.cut(df3.sum_influence_3_days, ranges)).size().reset_index(name="Count")

    lower_df['Variation'] = 'Bearish'
    middle_df['Variation'] = 'Neutral'
    upper_df['Variation'] = 'Bullish'
    return pd.concat([lower_df, middle_df, upper_df])