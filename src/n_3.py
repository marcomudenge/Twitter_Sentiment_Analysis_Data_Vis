import numpy as np
import pandas as pd
import plotly.graph_objects as go


def polar_chart(df):
    """
    Args:
        df: Dataframe already preprocessed
    Returns:
        Theta, r, and color_freq. Input to creation of polar chart.
    """
    fig = go.Figure()

    for i in range(24):  # Loop over all hours
        # Dataframe with only i:th hour included
        hour_df = df[df['timestamp'].astype(int) == i]
        min_val = hour_df['index_variation'].min()
        max_val = hour_df['index_variation'].max()

        # Create ranges of index_variation values
        n_ranges = round(len(hour_df) / 3)
        range_size = (max_val - min_val) / n_ranges
        ranges = [(min_val + i * range_size, min_val + (i + 1) * range_size) for i in range(n_ranges)]

        # Count number of times values appear within the previously defined ranges
        counts = []
        for r in ranges:
            count = len(hour_df[(hour_df['index_variation'] >= r[0]) & (hour_df['index_variation'] < r[1])])
            counts.append(count)

        # Overwrite df with new dataframe including range-values and count
        df_freq = pd.DataFrame({'range': ranges, 'count': counts})
        df_freq = df_freq[df_freq['count'] != 0]
        df_freq = df_freq.sort_values(by='range')

        theta = [i * 15] * len(df_freq)
        r = [r[1] for r in df_freq['range']]
        color_freq = df_freq['count'].tolist()

        update_fig(fig, theta, r, color_freq)

    return fig

def update_fig(fig, theta, r, color_freq):
    """
    Args:
        theta: angles for different hours
        r: index_variation ranges
        color_freq: number of times a certain index_variation range appeared at a given hour
    Returns:
        Polar chart
    """

    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=theta,
        mode='markers',
        marker=dict(color=color_freq, colorscale='aggrnyl', size=10,
                    colorbar=dict(nticks=1)),
        showlegend=False
        )
    )

    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                direction='clockwise',
                tickmode='array',
                tickvals=np.arange(0, 360, 15),
                ticktext=['00', '', '', '', '', '', '06', '', '', '', '', '',
                          '12', '', '', '', '', '', '18', '', '', '', '', '']
            )
        )
    )
    return fig
