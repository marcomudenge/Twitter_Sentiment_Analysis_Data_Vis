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

import plotly.graph_objects as go #move into viz files ?
import preprocess
import vis3
import pandas as pd

app = dash.Dash(__name__)
app.title = "" #TBD

stats = pd.read_csv('assets/df_stats.csv')
data_3 = preprocess.stats_vis3(stats)

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
        html.Div(className='viz3', children=[
            html.Div([
                    dcc.Graph(
                        id='vis_3',
                        figure=vis3.init_figure(data=data_3)
                    )
                ], style={'width': '70%', 'display': 'inline-block'}),

        ]),
        
    ])
])

#callbacks ici
#@app.callback(
#    Output(),
#    Input()
#)