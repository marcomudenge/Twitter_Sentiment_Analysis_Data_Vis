import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import more_itertools as it
from plotly.subplots import make_subplots

def hover_line():
    return '%{x}</br></br> <b>Price :</b> %{y}'+'<extra></extra>'

def hover_bar():
    return '%{x}</br></br><b>Index :</b> %{y} </br><b>Activity :</b> %{marker.color}'+'<extra></extra>'

def get_tweet(date):
    ''' 
    arg :
        date string yyyy-mm-dd
    return: 
        2 tweet with the most follower
    '''
    from app import tweets_vis1
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')
    date_minus_3 = date_obj - timedelta(days=3)
    date_minus_3_str =  date_minus_3.strftime('%Y-%m-%d %H:%M')
    
    mask= (tweets_vis1['timestamp']<= date ) & (tweets_vis1['timestamp']>= date_minus_3_str)
    tweet = tweets_vis1[mask].sort_values(by = 'n_followers').head(2)['text'].values
    return tweet[0], tweet[1]
    

def maquette_1(df, start_date = '2021-07-20', end_date = '2021-08-01'):
    df = df[(df['timestamp']<= end_date ) & (df['timestamp']>= start_date)]
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
        opacity = 0.7,
        
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
                hovertemplate=hover_line()
            )
        )
    
    ### build the bar chart
    bar_chart = px.bar(df, x='timestamp', y='index_value', color='Activity', color_continuous_scale='YlGnBu')
    bar_chart.update_traces(hovertemplate=hover_bar())
    
    fig.add_trace(bar_chart.data[0], row = 2, col=1)
    
    fig.update_layout(coloraxis=bar_chart.layout.coloraxis, showlegend=False)
    fig.update_yaxes(title_text='Price', row=1, col=1)
    fig.update_yaxes(title_text='Index', row=2, col=1)
    fig.update_traces(marker_line_width = 0,selector=dict(type="bar")) ### no space between bar, making the graph more visible with large range of x axis
    
    return fig

