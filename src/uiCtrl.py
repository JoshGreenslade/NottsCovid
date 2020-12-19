import json
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)


class UiCtrl:
    """ A class for controlling the UI """

    def __init__(self, data_ctrl, app):

        self.app = app
        self.data_ctrl = data_ctrl

        with open(config['geojsonPath']) as geofile:
            self.geojson = json.load(geofile)

            df = pd.DataFrame({
                "x": [1, 2, 1, 2],
                "y": [1, 2, 3, 4],
                "customdata": [1, 2, 3, 4],
                "fruit": ["apple", "apple", "orange", "orange"]
            })

        self.app.layout = html.Div([
            html.Div([
                dcc.Graph(id='test')
            ]),
            html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    data=df.to_dict('records')
                )
            ]),
        ])
