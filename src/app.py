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

from datetime import date
from datetime import datetime, timedelta
import plotly.graph_objects as go #move into viz files ?
import preprocess
import vis1
import pandas as pd

stats = pd.read_csv('assets/df_stats.csv')
tweets = pd.read_csv('assets/df_tweets.csv')
stats_vis1 = preprocess.stats_vis1(stats)
tweets_vis1 = preprocess.tweets_vis1(tweets)

vis_1 = vis1.maquette_1(stats_vis1,'2021-04-03', '2021-04-20')


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
                ], style={'width': '70%', 'display': 'inline-block'}),

                html.Div([
                    html.Table([
                        html.Tr([html.Th('Influencial Tweet', colSpan=2)]),
                        html.Tr(children=[html.Th(id='index_var'),html.Th(id = 'tweet_row')])
                    ])
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'})
        ]),
        html.Div(className='bandeau_dessous', children=[
            html.Div(className='selecteur_viz', children=[
                None
            ]),
            dcc.DatePickerRange(id='my-date-picker-range',  #selecteur de date pour la viz 4
                                min_date_allowed=date(2021, 3, 1),
                                max_date_allowed=date(2021, 8, 1)
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
        date =  ctx.triggered[0]['value']['points'][0]['x'] ### date is a string
        # convert input date string to datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')
        date_minus_3 = date_obj - timedelta(days=3)
        date_minus_3_str =  date_minus_3.strftime('%Y-%m-%d %H:%M')
        
        mask= (tweets['timestamp']<= date ) & (tweets['timestamp']>= date_minus_3_str)
        tweet = tweets[mask].sort_values(by = 'n_followers').head(1)['text'].values
        
        return tweet.tolist(), stats[stats['timestamp']==date]['index_variation'] 
    else:
        return cur_tweet, cur_index