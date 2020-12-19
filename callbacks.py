from dash.dependencies import Input, Output
import pandas as pd
import json
from app import app, data_ctrl
import plotly.express as px


@app.callback(
    Output('map-figure', 'figure'),
    Input('dropdown', 'value'))
def display_value(value):
    df = data_ctrl.get_data_for_area(value)
    fig = px.choropleth_mapbox(df,
                               geojson=data_ctrl.geojson,
                               color="latest.newCasesBySpecimenDate.rollingRate",
                               locations="areaCode",
                               featureidkey="properties.msoa01cd",
                               center={'lat': 52.88902922895685,
                                       'lon': -1.246953174103217},
                               zoom=9,
                               opacity=0.4)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_accesstoken='pk.eyJ1IjoiamdyZWVuc2xhZGUiLCJhIjoiY2tpcnJqOWF6MGs3dTMwb2JyYWN4MzNtZCJ9.M8BhWR_plOZDW2v8UaZeJA')
    fig.update(layout_coloraxis_showscale=False)
    return fig
