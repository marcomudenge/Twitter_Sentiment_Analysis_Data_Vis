import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import more_itertools as it
from plotly.subplots import make_subplots

import preprocess, hover_template

def get_tweet(date, query=None):
    ''' 
    arg :
        date string yyyy-mm-dd
    return: 
        2 tweet with the most follower
    '''
    from app import tweets
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')
    date_minus_3 = date_obj - timedelta(days=3)
    date_minus_3_str =  date_minus_3.strftime('%Y-%m-%d %H:%M')
    
    mask_date= (tweets['timestamp']<= date ) & (tweets['timestamp']>= date_minus_3_str)
    if query:
        filter_tweets = tweets[tweets['text'].str.contains(query, case=False)]
        tweet = filter_tweets[mask_date].sort_values(by = 'n_followers').head(5)['text'].str.replace(r'\bhttps?:/\S+', '', regex=True).values
        return tweet
    else:
        tweet = tweets[mask_date].sort_values(by = 'n_followers').head(5)['text'].str.replace(r'\bhttps?:/\S+', '', regex=True).values
        return tweet
    

def init_main_figure(df):

    # preprocess data
    df = preprocess.get_main_vis_data(df)

    # create coordinate  pairs
    x_pairs = it.pairwise(df['timestamp'].to_list())
    y_pairs = it.pairwise(df['product'].to_list())
    y_price_pairs = it.pairwise(df['price'].to_list())

    # generate color list
    colors=['red' if any([i < 0 for i in y_values]) else 'green' for y_values in y_pairs]

    # create base figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
    ### build the scatter trace
    scatter = go.Scatter(
    x=df.loc[df.high_variation.isin([1,-1])]['timestamp'],
    y=df.loc[df.high_variation.isin([1,-1])]['index_value'],
    hoverinfo='none',
    mode='markers',
    marker=dict(
        symbol = 'diamond',
        size=9,
        color='black',
        opacity = 0.7
    ))
    
    fig.add_trace(scatter, row=2, col=1)
    
    # add line chart chart trace 
    for x, y, color in zip(x_pairs, y_price_pairs, colors):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y, 
                mode='lines', 
                line={'color': color},
                hovertemplate=hover_template.get_main_vis_line_chart_hover_template()
            )
        )
    
    ### build the bar chart
    bar_chart = px.bar(df, x='timestamp', y='index_value', color='Activity', color_continuous_scale='Teal')
    bar_chart.update_traces(hovertemplate=hover_template.get_main_vis_bar_chart_hover_template())
    
    fig.add_trace(bar_chart.data[0], row = 2, col=1)
    
    fig.update_layout(coloraxis=bar_chart.layout.coloraxis, showlegend=False,
                      title={'text': "EUR/USD Price And Index charts"}   
                      )
    fig.update_yaxes(title_text='Price (EUR/USD)', row=1, col=1)
    fig.update_yaxes(title_text='Index', row=2, col=1)
    fig.update_traces(marker_line_width = 0,selector=dict(type="bar")) ### no space between bar, making the graph more visible with large range of x axis
    fig.update_layout(plot_bgcolor='#F0F0F0')
    
    return fig

