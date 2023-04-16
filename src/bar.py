import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import more_itertools as it
from plotly.subplots import make_subplots

import preprocess
import hover_template

def init_bar_figure(data):

    # preprocess data
    data = preprocess.get_bar_chart_data(data)

    fig = go.Figure()
    # TODO : Update the template to include our new theme and set the title
    fig.update_layout(
        dragmode=False,
        barmode='relative',
        title={
        'text': 'Number of tweets depending on the sum of followers regarding the index_variation',
        'xanchor': 'center',
        'yanchor': 'top'},
        yaxis_title='Count',
    )
    
    fig = go.Figure(fig)  # conversion back to Graph Object
    
    fig.data = [] 
    colors = ["#FF0000", "#F4D8CE" , "#00FFBC"]
    cat = ['Bearish', 'Neutral', 'Bullish']
    """### ajout de hovertemplate pour prendre en compte l'info-bulle
    fig = px.bar(data, x='sum_influence_3_days', y='Count',
                 color='variation',
                 title='Distribution of activity',
                 height=400)"""    
    # Create the three barcharts with the respective colors
    for i, category in enumerate(cat):
        df = data[data['variation'] == category]
        fig.add_trace(go.Bar(
            x=df['sum_influence_3_days'],
            y=df['Count'],
            name=category,
            marker_color=colors[i],
            hovertemplate= hover_template.get_barchart_hover_template()
        ))
                 
    
    fig.update_layout(legend_title='Type of variation')
    fig.update_xaxes(title='Activity (3-Days Influence)')
    fig.update_yaxes(title='Count')

    return fig