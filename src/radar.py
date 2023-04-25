import plotly.graph_objects as go
import numpy as np

import preprocess
import hover_template


def init_radar_figure(data):
    '''
        Creates and return the radar figure.

        Args:
            data: The dataframe to process
        Returns:
            The radar figure
    '''

    # Get the start and end dates for the title
    start, end, _ = preprocess.get_timeframe(data)

    # prepare the average data set
    mean_df = preprocess.get_radar_trend_data(data)

    # prepare the scatter data set
    scatter_data = preprocess.get_radar_scatter_data(data)

    # Create the figures
    fig = go.Figure()
    fig = add_radar_trend_figure(fig, mean_df)
    fig = add_radar_scatter_figure(fig, scatter_data)

    # Customize layout
    fig.update_layout(polar=dict(angularaxis=dict(tickvals=np.arange(0, 360, 15),
                                 ticktext=[str(x) for x in np.arange(24)],
                                            showticklabels=True,
                                            showline=False,
                                            showgrid=False,
                                            linewidth=3,
                                            ticks='inside',
                                            direction='clockwise'
                                            ),
                                 radialaxis=dict(
                                            ticktext=[str(x) for x in np.arange(24)],
                                            showticklabels=True,
                                            ticks='',
                                            showline=True,
                                            showgrid=True,
                                            gridcolor='white',
                                            tickfont=dict(size=10),
                                            tickangle=45
                                            )),
                      template=None)

    # Add buttons
    fig.update_layout(
        title="Hourly visualisation of the index variation <br><sup>{} to {}</sup>".format(start, end),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{'visible': [True, False]}],
                        label="Trend",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [False, True]}],
                        label="Scatter",
                        method="update"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="center",
                y=-0.25,
                yanchor="bottom"
            ),
        ],
        legend=dict(traceorder='normal',
                    x=0.4)
    )

    return fig


def add_radar_scatter_figure(fig, scatter_data):
    '''
        Adds scatters to the radar figure.

        Args:
            data: The base figure and the processed data
        Returns:
            The updated figure with added scatters.
    '''
    scatter = go.Scatterpolar(r=scatter_data["variation"], theta=scatter_data["hour_angle"], 
                              mode='markers',
                              marker=dict(color=scatter_data["count"],
                                          colorscale='Teal',
                                          colorbar=dict(title="Frequency",
                                                        x=0.75),
                                          showscale=True),
                              hovertemplate=hover_template.get_radar_scatter_hover_template(),
                              visible=False)

    fig.add_trace(scatter)

    return fig


def add_radar_trend_figure(fig, mean_df):
    '''
        Adds a trend line to the radar figure.

        Args:
            data: The base figure and the processed data  
        Returns:
            The updated figure with added trend.
    '''

    trend = go.Scatterpolar(r=mean_df["index_variation"], theta=mean_df["hour_angle"], mode='lines',
                            connectgaps=True,
                            hovertemplate=hover_template.get_radar_trend_hover_template())

    fig.add_trace(trend)
    return fig
