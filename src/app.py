#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:14:51 2023

@author: gallou

App initialization file
"""

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess, radar

app = dash.Dash(__name__)
app.title = "" #TBD

df_stats = pd.read_csv('src/assets/df_stats.csv')
df_tweets = pd.read_csv('src/assets/df_tweets.csv')

df_stats = preprocess.convert_dates(df_stats)
df_tweets = preprocess.convert_dates(df_tweets)

radar_fig = radar.get_radar_figure(df_stats)

app.layout = html.Div(className='content', children = [
    html.Header(children=[
        html.H1("Titre de l'app") #TBD
    ]),
    html.Main(className='viz-container-1', children=[
        dcc.Graph(
            id='radar-graph',
            className='graph',
            figure=radar_fig,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ])
])

#callbacks ici
#@app.callback(
#    Output(),
#    Input()
#)