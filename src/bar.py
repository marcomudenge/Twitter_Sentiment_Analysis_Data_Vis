import plotly.express as px

import preprocess,hover_template

def init_bar_figure(data):
    '''
        Creates and return the bar figure.

        Args:
            data: The dataframe to process
        Returns:
            The bar figure
    '''

    # preprocess data
    data = preprocess.get_bar_chart_data(data)

    # create the bar figure
    fig = px.bar(data, x='sum_influence_3_days', y='Count',
                color='variation',
                title='Distribution of activity',
                color_discrete_map = { "Bearish": "#FF0000",
                                    "Neutral": "#F4D8CE",
                                    "Bullish": "#00FFBC"},
                category_orders={'sum_influence_3_days': ['0 - 2','2 - 4','4 - 6'],  
                                 "variation": ["Bearish", "Neutral", "Bullish"]}
        )

    # update the figure & hover template
    fig.update_layout(
        dragmode=False,
        barmode='relative',
        title={
        'text': 'Number of tweets depending on the sum of followers regarding the index_variation',
        'xanchor': 'center',
        'yanchor': 'top',
        'x': 0.5,
        'font': dict(size=16)},
        yaxis_title='Count',
        xaxis_title='Activity (3-Days Influence)',
        legend_title='Type of variation'
    )
    
    fig.update_layout({
        'plot_bgcolor': '#F0F0F0',
    })

    fig.update_traces(hovertemplate = hover_template.get_bar_chart_hover_template())

    return fig