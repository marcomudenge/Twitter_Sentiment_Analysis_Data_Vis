import pandas as pd

def stats_vis3(stats):
    # Split DF by index variation
    df1 = stats[stats['index_variation'] > 0.5]
    df2 = stats.loc[(stats['index_variation'] >= -0.5) & (stats['index_variation'] <= 0.5)]
    df3 = stats[stats['index_variation'] < -0.5]

    # Group by ranges and count for each range
    ranges = [0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000]
    upper_df = df1.groupby(pd.cut(df1.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    middle_df = df2.groupby(pd.cut(df2.sum_influence_3_days, ranges)).size().reset_index(name="Count")
    lower_df = df3.groupby(pd.cut(df3.sum_influence_3_days, ranges)).size().reset_index(name="Count")

    lower_df['Variation'] = 'Bearish'
    middle_df['Variation'] = 'Neutral'
    upper_df['Variation'] = 'Bullish'
    
    merged = pd.concat([lower_df, middle_df, upper_df])
    merged['sum_influence_3_days'] = merged['sum_influence_3_days'].astype(str).str.replace(r'[][()]+', '', regex=True)
    print(merged)
    return merged