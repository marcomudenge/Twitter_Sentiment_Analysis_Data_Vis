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

import plotly.graph_objects as go #move into viz files ?

app = dash.Dash(__name__)
app.title = "" #TBD

app.layout = html.Div(className='content', children = [
    html.Header(children=[
        html.H1("Titre de l'app") #TBD
    ]),
    html.Main(className='', children=[
        None
    ])
])

#callbacks ici
#@app.callback(
#    Output(),
#    Input()
#)