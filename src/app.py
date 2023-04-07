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
import pandas as pd

from datetime import date

import preprocess as pp
import n_3

df = pd.read_csv('../src/assets/df_stats.csv')
df = pp.convert_dataframe(df)

fig = n_3.polar_chart(df)
fig.show()

app = dash.Dash(__name__)
app.title = ""  # TBD

app.layout = html.Div(className='content', children = [
    html.Header(children=[
        html.H1("Titre de l'app") #TBD
    ]),
    html.Main(className='', children=[
        html.Div(className='viz1', children=[
            None  # viz numero 1 en haut ?
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
