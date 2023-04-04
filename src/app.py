#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:14:51 2023

@author: gallou

App initialization file
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from datetime import date, datetime
import plotly.graph_objects as go #move into viz files ?
import preprocess
import vis1
import pandas as pd

stats = pd.read_csv('assets/df_stats.csv')
tweets = pd.read_csv('assets/df_tweets.csv')
stats_vis1 = preprocess.stats_vis1(stats)
tweets_vis1 = preprocess.tweets_vis1(tweets)
start = datetime.strptime('2021-04-03', "%Y-%m-%d")
end = datetime.strptime('2021-04-20', "%Y-%m-%d")

vis_1 = vis1.maquette_1(stats_vis1, start, end)


app = dash.Dash(__name__)
app.title = "" #TBD

app.layout = html.Div(className='content', children = [
    html.Header(children=[
        html.H1("Titre de l'app") #TBD
    ]),
    html.Main(className='', children=[
        html.Div(className='viz1', children=[
            html.Div([
                    dcc.Graph(
                        id='vis_1',
                        figure=vis_1
                    )
                ], style={'width': '75%', 'display': 'inline-block'}),

                html.Div([html.H1('Influencial tweet'),
                    html.Table([
                        html.Tr(children=[html.Th(id='index_var', style={'width': '20%'}),html.Th(id = 'tweet_row',style={'text-align': 'left','width': '70%'})]),
                    ], style={'border-spacing': '10px','width': '90%','height': '30vh'})
                    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top','border': '1px solid black',
                    'padding': '10px','border': '1px solid black','border-radius': '10px','overflow': 'hidden','margin': '10px'})
        ]),
        html.Div(className='bandeau_dessous', children=[
            html.Div(className='selecteur_viz', children=[
                None
            ]),
            dcc.DatePickerRange(id='my-date-picker-range',  #selecteur de date pour la viz 4
                                min_date_allowed=date(2021, 3, 1),
                                max_date_allowed=date(2021, 8, 1),
                                start_date=start,
                                end_date=end
            )
        ])
    ])
])

@app.callback(
    [Output('tweet_row', 'children'), Output('index_var', 'children')],
    [Input('vis_1', 'clickData')],
    [State('tweet_row', 'children'), State('index_var', 'children')]
    )
def display_tweet(click, cur_tweet, cur_index):
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], []
    
    if (ctx.triggered[0]['prop_id'].split('.')[0]=='vis_1') & (ctx.triggered[0]['value']['points'][0]['curveNumber'] == 0):
        date =  ctx.triggered[0]['value']['points'][0]['x'] 
        tweet1, tweet2 = vis1.get_tweet(date)
        
        output1 = html.Div([
                    html.P(tweet1),
                    html.P(tweet2, style={'margin-top': '0px', 'padding-top': '0px'})
                ], style={'line-height': '80%'})
        
        index_variation = stats[stats['timestamp']==date]['index_variation'].round(2).values
        output2 = f'index_var :{index_variation}'
        return output1, output2
    else:
        return cur_tweet, cur_index
    
@app.callback(
    Output('vis_1', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_vis1(start_date, end_date):
    # Create the new figure with the updated x range
    fig = vis1.maquette_1(stats_vis1, start_date, end_date)
    return fig