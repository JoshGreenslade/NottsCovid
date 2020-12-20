from dash.dependencies import Input, Output
import pandas as pd
import json
from app import app, data_ctrl
import plotly.express as px


@app.callback(
    Output('readout', 'children'),
    Input('map-figure', 'hoverData'))
def display_hover_data(hover_data):
    return json.dumps(hover_data['points'][0]['location'], indent=2)
