def get_radar_trend_hover_template():
    '''
        Sets the template for the hover tooltips
        of the radar average plot.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.
        The labels' font is bold and the values are normal weight
        returns:
            The content of the tooltip
    '''
    return '<span style="font-weight:bold;">Time :</b> %{theta}:00 <br></span>'+\
           '<span style="font-weight:bold;">Average Variation :</b> %{r}</span>'+\
            '<extra></extra>'

def get_radar_scatter_hover_template():
    '''
        Get the template for the hover tooltips
        of the radar scatter plot.
        returns:
            The content of the tooltip
    '''
    return '<span style="font-weight:bold;">Time :</b> %{theta}:00 <br></span>' +\
           '<span style="font-weight:bold;"><br>variation :</b> %{r} <br></span>'+\
           '<span style="font-weight:bold;"><br>Occurences :</b> %{marker.color} times</span>'+\
             '<extra></extra>'

def get_bar_chart_hover_template():
    '''
        Get the template for the hover tooltips
        of the bar char plot (second viz).
        returns:
            The content of the tooltip
    '''
    return '<span style="font-weight:bold;">Nombre de tweets :</b> %{y} </span>' +\
           '<span style="font-weight:bold;"><br>Intervalle de followers :</b> %{x} millions</span>' +\
            '<extra></extra>'

def get_main_vis_line_chart_hover_template():
    '''
        Get the template for the hover tooltips
        of the line chart of the main viz.
        returns:
            The content of the tooltip
    '''
    return '<span style="font-weight:bold;">Date & Time :</b> %{x} <br></span>' +\
           '<span style="font-weight:bold;">Price :</b> %{y} </span>' +\
            '<extra></extra>'

def get_main_vis_bar_chart_hover_template():
    '''
        Get the template for the hover tooltips
        of the bar chart of the main viz.
        returns:
            The content of the tooltip
    '''
    return '<span style="font-weight:bold;">Date & Time:</b> %{x} <br></span>' +\
           '<span style="font-weight:bold;">Index :</b> %{y} <br></span>' +\
           '<span style="font-weight:bold;">Activity :</b> %{marker.color}' +\
            '<extra></extra>'