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

from datetime import date

import plotly.graph_objects as go #move into viz files ?
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
    html.Main(className='', children=[
        html.Div(className='viz1', children=[
            None #viz numero 1 en haut ?
        ]),
        html.Div(className='bandeau_dessous', children=[
            html.Div(className='selecteur_viz', children=[
                None
            ]),
            dcc.DatePickerRange(id='my-date-picker-range',  #selecteur de date pour la viz 4
                                min_date_allowed=date(2021, 3, 1),
                                max_date_allowed=date(2021, 8, 1)
            )
        ]),
        html.Div(className='viz-container-1', children=[
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
])

#callbacks ici
#@app.callback(
#    Output(),
#    Input()
#)