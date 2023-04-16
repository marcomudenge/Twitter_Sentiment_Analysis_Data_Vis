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
import dash_bootstrap_components as dbc

from datetime import date, datetime

import preprocess
import main_viz
import bar
from style import *
import radar
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "" #TBD

# Read CSV files
stats = pd.read_csv('assets/df_stats.csv')
tweets = pd.read_csv('assets/df_tweets.csv')

# Preprocess data
stats = preprocess.convert_dates(stats)
tweets = preprocess.convert_dates(tweets)
start,end = preprocess.get_timeframe(stats)

app.layout = html.Div(className='content', children = [
        html.Div([
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.Img(src=profile_image, style={'borderRadius': '50%','height': '100%', 'width': '100%'} ),
                        style={"textAlign": "center","borderRadius": "50%","backgroundColor": "lightgray","height": "100%", "width": "100%",},#"margin-top": "35px", 'margin-left': '25px'},
                    ),
                    width={'size': 2, 'offset':1},),
            ),
            dbc.Row(
                dbc.Col(
                    html.Div([
                            html.H1(username, style={'font-size': '20','margin-top' : '20px','margin-bottom': '10px', 'margin-left' : '25px', 'color': 'black'}),
                            html.P(account, style={'font-size': '14','margin-bottom': '10px', 'margin-left' : '25px', 'color': 'gray'}),
                            html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut ', 
                                    style={'font-size': '18','margin-bottom': '10px', 'margin-left' : '25px', 'color': 'gray'}),
                            html.Div([
                                html.Span(" "),
                                html.Span("12.6M Followers", style={'margin-left' : '25px', 'margin-top' : '35px', 'Font-Weight': 'bold',}),
                                html.Span("1.2K Following", style={'margin-left' : '25px', 'margin-top' : '35px', 'Font-Weight': 'bold'}),
                            ]),
                    ]),
                    width=11),
                justify='center'
            ),
#                dbc.Col(
#                    html.Div(
#                       [
#                          html.Button("Follow", className="mr-2", ),
#                         html.Button("Message"),
#                    ],
#                   #style={"marginTop": "140px"},
#              ),
#             md=6,
    #        ),
            ],
            style={"marginBottom": "50px"},
        ),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Tabs([
                        dcc.Tab(
                            label="Tweets",
                            children=[
                                dbc.Container([
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("INTRODUCTION HERE. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),               
                                            ], style=graph_box_style)
                                        ], style=tweets_style),                                  
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("Choose the date range of the data to be displayed in the visualisations below using this calendar."), 
                                                dcc.DatePickerRange(id='my-date-picker-range',  
                                                    min_date_allowed=start,
                                                    max_date_allowed=end,
                                                    start_date=start,
                                                    end_date=end
                                                ),
                                            #    html.P("You can also change the date range using drag-and-drop on the horizontal axis of the first visualisation.") #to implement + add some padding w/ calendar above
                                            ], style=graph_box_style)
                                        ], style=tweets_style),                                  
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("The price line is green when the variation of the price and the index goes in the same direction, red otherwise. The activity colorscale represent the sum of tweets weighted by the number of followers, the unit of the activity is million of followers"),
                                                html.Div(className='bandeau_dessous', children=[
                                                    html.Div(className='selecteur_viz', children=[
                                                        None
                                                    ]),
                                                ]),
                                                html.Div(className='main_vis', children=[
                                                    html.Div([
                                                            dcc.Graph(
                                                                id='main_vis',
                                                                figure=main_viz.init_main_figure(stats)
                                                            )
                                                        ], style={'width': '75%', 'display': 'inline-block'}),

                                                        html.Div(
                                                            children=[
                                                                html.Div(id='panel',
                                                                        children=[
                                                                            html.Div(['Influential tweets'], style={
                                                                                'fontSize': '24px'}),
                                                                            html.Div(id='date_row', style={
                                                                                'fontSize': '20px',"margin-top": "6px"}),
                                                                            html.Div(id='index_var', style={
                                                                                'fontSize': '20px',"margin-top": "6px"}),
                                                                            html.Div(id='tweet_row', style={
                                                                                'fontSize': '20px'})])]
                                                            ,style={'width': '23%',
                                                                    'display': 'inline-block',
                                                                    'vertical-align': 'top',
                                                                    'padding': '10px',
                                                                    'border': '1px solid black',
                                                                    'border-radius': '10px'})
                                                ]),            
                                            ], style=graph_box_style)
                                        ], style=tweets_style),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("Some more explanations. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),
              
                                            ], style=graph_box_style)
                                        ], style=tweets_style),                                  
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray', 'font-size': '14'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("Explanations.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),
                                                html.Div(className='bar_vis', children=[
                                                    html.Div([
                                                            dcc.Graph(
                                                                id='bar_vis',
                                                                figure=bar.init_bar_figure(stats)
                                                            )
                                                        ], style={'width': '60%', 'display': 'inline-block'}),
                                                ]),
                                                dbc.Col([
                                                    html.Div([
                                                    ], style={'display':'inline-block', 'vertical-align':'top'}),
                                                ]),               
                                            ], style=graph_box_style)
                                        ], style=tweets_style),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("Explanations.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),
                                                html.Div(className='radar_vis', children=[
                                                    html.Div([
                                                        dcc.Graph(
                                                            id='radar_vis',
                                                            figure=radar.init_radar_figure(stats)
                                                            )]
                                                        )
                                                ]),
                                            ], style=graph_box_style)
                                        ], style=tweets_style),     
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                html.Img(src=profile_image, 
                                                        style={'height':'50px','width':'50px','border-radius':'50%'}),
                                                html.Div([
                                                    html.H5(username, style={'margin':'0px','font-size': '16'}),
                                                    html.Span(account, style={'color':'gray'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("CLOSING. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),               
                                            ], style=graph_box_style)
                                        ], style=tweets_style),                                  
                                    ]),
                                ], style={'margin-top':'40px', 'background-color':'white'}
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Photos",
                            disabled=True,
                            children=[
                                html.Div(
                                    "Photos go here",
                                    style={"marginTop": "20px"},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Videos",
                            disabled=True,
                            children=[
                                html.Div(
                                    "Videos go here",
                                    style={"marginTop": "20px"},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Likes",
                            disabled=True,
                            children=[
                                html.Div(
                                    "Liked tweets go here",
                                    style={"marginTop": "20px"},
                                )
                            ],
                        ),
                    ])
                ]),
                md=12,
            )
        ]),
    ], style={'display':'inline-block', 'width': '100%;', 'vertical-align':'top', 'word-wrap':'break-word',
                                                'border': '1px solid black', 'padding':'10px',
                                                'border-color':'lightgray',
                                                'margin-left':'1%', 'margin-right':'1%'}
)

@app.callback(
    [Output('tweet_row', 'children'),
     Output('index_var', 'children'),
     Output('date_row', 'children')],
    [Input('main_vis', 'clickData')],
    [State('tweet_row', 'children'),
     State('index_var', 'children'),
     State('date_row', 'children')]
    )
def display_tweet(click, cur_tweet, cur_index, cur_date):
    # TODO : Can we hide the panel if a marker is not yet clicked ?
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], [], ['Click on a dark marker to see more information about the tweet that lead to high index variation']
    
    if (ctx.triggered[0]['prop_id'].split('.')[0]=='main_vis') & (ctx.triggered[0]['value']['points'][0]['curveNumber'] == 0):
        date =  ctx.triggered[0]['value']['points'][0]['x'] 
        tweet1, tweet2 = main_viz.get_tweet(date)
        
        output1 = html.Div([
                    html.P(tweet1),
                    html.P(tweet2, style={'margin-top': '0px', 'padding-top': '0px'})
                ], style={'line-height': '80%'})
        index_variation = stats[stats['timestamp']==date]['index_variation'].round(2).values[0]
        output2 = f'Index variation : {index_variation}'
        output3 = 'Date : ' + str(date)
        return output1, output2, output3
    else:
        return cur_tweet, cur_index, cur_date
    
@app.callback(
    [Output('main_vis', 'figure'),
     Output('bar_vis', 'figure'),
     Output('radar_vis', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_figures(start_date, end_date):

    # Select the timeframe from the data set
    df = preprocess.select_timeframe(stats, start_date, end_date)

    main_fig = main_viz.init_main_figure(df)
    bar_fig = bar.init_bar_figure(df)
    radar_fig = radar.init_radar_figure(df)

    return main_fig, bar_fig, radar_fig
