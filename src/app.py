import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc

from datetime import date, datetime

import preprocess
import main_viz
import bar
from style import *
import radar
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css', dbc.icons.BOOTSTRAP]) #force to load css in this order
app.title = "Les Datavores — Data Analysis"
server = app.server

# Read CSV files
stats = pd.read_csv('assets/df_stats.csv')
tweets = pd.read_csv('assets/df_tweets.csv')

# Preprocess data
stats = preprocess.convert_dates(stats)
tweets = preprocess.convert_dates(tweets)
start,end,display = preprocess.get_timeframe(stats)

app.layout = html.Div(className='content', children = [
        dbc.Toast(children = [
            dcc.DatePickerRange(id='date-picker-range',
                                min_date_allowed=start,
                                max_date_allowed=end,
                                start_date=start,
                                end_date=display)], id='datepicker_button'),
        html.Div([
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.Img(src=profile_image, style={'borderRadius': '50%','height': '100%', 'width': '100%'} ),
                        style={"textAlign": "center","borderRadius": "50%","backgroundColor": "lightgray","height": "100%", "width": "100%",},
                    ),
                    width={'size': 2, 'offset':1},),
            ),
            dbc.Row(
                dbc.Col(
                    html.Div([
                            html.H1(username, style={'font-size': '20','margin-top' : '20px','margin-bottom': '10px', 'margin-left' : '25px', 'color': 'black'}),
                            html.P(account, style={'font-size': '14','margin-bottom': '10px', 'margin-left' : '25px', 'color': 'gray'}),
                            html.P("Welcome to Team 16's website! In this page, you will find various data visualizations and information on tweets related to the EUR/USD currency pair.", 
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
            ],
            style={"marginBottom": "30px"},
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
                                                html.P("With the increasing prevalence of social media platforms such as Twitter, there has been a growing interest in analyzing public sentiment and its potential impact on the stock market. This has led to the development of various analytical techniques, including natural language processing, to classify tweets into different sentiment categories such as neutral, bullish, and bearish. By using data visualisation to discover the relation between time series data on USD/EURO stock and tweet sentiment, this project aims to uncover valuable insights into the relationship between social media sentiment and financial decision-making."),               
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
                                                html.P("Choose the date range of the data to be displayed in the visualisations below using the hovering calendar. You can also refine the date range by using drag-and-drop on the first visualisation. The date range of the cropped region will then be used.")
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
                                                html.P("This first visualisation shows the values of the EURUSD and the activity index over the selected time period."),
                                                html.P("The price line is green when both the variations of the price and the index go in the same direction, it is red otherwise.\
                                                        The activity colorscale represents the sum of the number of tweets weighted by the number of followers, the activity is expressed in millions of followers.\
                                                        The influential tweets displayed in the box are the 3 tweets with the greatest audience (number of followers) posted on the day before the high index variation."),
                                                html.Div(className='bandeau_dessous', children=[
                                                    html.Div(className='selecteur_viz', children=[
                                                        None
                                                    ]),
                                                ]),
                                                dbc.Row(className='main_vis_container', children=[
                                                    dbc.Col([
                                                            dcc.Graph(
                                                                id='main_vis',
                                                                figure=main_viz.init_main_figure(preprocess.select_timeframe(stats, start, display))
                                                            )
                                                        ], width=9),

                                                    dbc.Col(
                                                        children=[
                                                            html.Div(id='panel',
                                                                    children=[
                                                                        html.H5(['Influential tweets']),
                                                                        html.Hr(),
                                                                        dbc.Input(id='search-input', type='text', placeholder='Search...',),
                                                                        html.Div(id='date_row', style={'color':'gray', 'text-align':'justify'}),
                                                                        html.Div(id='index_var', style={'color':'gray'}),
                                                                        html.Br(),
                                                                        html.Div(id='tweet_row', style={
                                                                            'fontSize': '18px',"margin-top": "0px"})])]
                                                        ,style={'display': 'inline-block',
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
                                                    html.Span(account, style={'color':'gray', 'font-size': '14'})
                                                ], style=tweets_header_style),
                                            ]),
                                            html.Div([
                                                html.P("This stacked bar chart illustrates the number of tweets for each type of variation. The variation can be either bullish, neutral or bearish. The activity is equivalent to the sum of the tweet author's following count in the past 3 days (from the date of the tweet). Each bar in the visualization is associated to a 2M activity interval."),
                                                html.Div(className='bar_vis', children=[
                                                    html.Div([
                                                            dcc.Graph(
                                                                id='bar_vis',
                                                                figure=bar.init_bar_figure(stats)
                                                            )
                                                        ], style={'display': 'flex', 'justify-content': 'center'}),
                                                ])             
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
                                                html.P("This spider chart shows the hourly index variations starting from March 2021 to August 2021. As we can see, the variation seems to peak at 2 PM EST on average. Switch over to the 'Scatter' tab to see more detailed entries."),
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
                                                html.P("That's it for now! Stay tuned for more information on currency exchange rates."),               
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

dbc.Button("Back to Top", href="/", className='bi-arrow-up bi-align-center me-2', style={"border-radius": "10px", "width": "fit-content", "height": "35px", "position": "absolute", 'left': '87.7vw', 'bottom': '100px', 'font-size': '16px'}),
    ], style={'vertical-align':'top', 'word-wrap':'break-word',
                'border': '1px solid black', 'padding':'10px',
                'border-color':'lightgray',
                'margin-left':'1%', 'margin-right':'1%',
                'position': 'relative'},
)

@app.callback(
    [Output('tweet_row', 'children'),
     Output('index_var', 'children'),
     Output('date_row', 'children')],
    [Input('main_vis', 'clickData'),
     Input('search-input', 'value')],
    [State('tweet_row', 'children'),
     State('index_var', 'children'),
     State('date_row', 'children')]
    )

def display_tweet(click, query, cur_tweet, cur_index, cur_date):
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], [], ['Click on a dark marker on the index chart to see more information about the tweet that led to high index variation.']
    
    if ctx.triggered[0]['prop_id']=='search-input.value':
        cur_date = cur_date.replace('Date : ', '')
        tweet = main_viz.get_tweet(cur_date, query)
        output1 = html.Div([html.P(tweet[i],style={'margin-top': '0px', 'padding-top': '0px'}) for i in range(len(tweet))]
                , style={'line-height': '90%'})
        return output1, cur_index, cur_date
    
    elif (ctx.triggered[0]['prop_id'].split('.')[0]=='main_vis') & (ctx.triggered[0]['value']['points'][0]['curveNumber'] == 0):
        date =  ctx.triggered[0]['value']['points'][0]['x'] 
        tweet = main_viz.get_tweet(date)
        
        output1 = html.Div([html.Div([html.P(tweet[i],style={'margin-top': '0px', 'padding-top': '0px'}) for i in range(len(tweet))])
                ], style={'line-height': '90%'})
        index_variation = stats[stats['timestamp']==date]['index_variation'].round(2).values[0]
        output2 = f'Index variation : {index_variation}'
        output3 = 'Date : ' + str(date)
        return output1, output2, output3
    else:
        return cur_tweet, cur_index, cur_date

@app.callback(
    [Output('main_vis', 'figure'),
     Output('bar_vis', 'figure'),
     Output('radar_vis', 'figure'),
     Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('main_vis', 'relayoutData')]
)
def update_figures(start_date, end_date, rel):
    #if callback is triggered by dragging and dropping on main vis
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'main_vis':
        if 'xaxis.range[0]' in rel.keys():
            start_date = rel['xaxis.range[0]'].split()[0]
            end_date = rel['xaxis.range[1]'].split()[0]

    # Select the timeframe from the data set
    df = preprocess.select_timeframe(stats, start_date, end_date)

    main_fig = main_viz.init_main_figure(df)
    bar_fig = bar.init_bar_figure(df)
    radar_fig = radar.init_radar_figure(df)

    return main_fig, bar_fig, radar_fig, start_date, end_date

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("datepicker_button", "className"), # dummy attribute
    [Input("datepicker_button", "id")],
)