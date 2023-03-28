import pandas as pd

def stats_vis1(stats):
    stats['price_variation'] = stats['price'].diff()
    stats.rename(columns={'sum_influence_3_days':'Activity'}, inplace=True)
    stats['Activity']=(stats['Activity']/1e6).round(1)
    stats['index_value']=stats['index_value'].round(2)
    stats['product'] = stats['price_variation']*stats['index_variation']
    stats.timestamp=pd.to_datetime(stats.timestamp)
    return stats

def tweets_vis1(tweets):
    tweets.timestamp=pd.to_datetime(tweets.timestamp)
    return tweets
    
    
    