import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from app import data_ctrl

from app import config

map_fig = px.choropleth_mapbox(data_ctrl.data,
                               geojson=data_ctrl.geojson,
                               color="latest.newCasesBySpecimenDate.rollingRate",
                               locations="areaCode",
                               featureidkey="properties.msoa11cd",
                               center={'lat': 52.98902922895685,
                                       'lon': -1.246953174103217},
                               zoom=9,
                               opacity=0.4)
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_accesstoken='pk.eyJ1IjoiamdyZWVuc2xhZGUiLCJhIjoiY2tpcnJqOWF6MGs3dTMwb2JyYWN4MzNtZCJ9.M8BhWR_plOZDW2v8UaZeJA')
map_fig.update(layout_coloraxis_showscale=False)

layout1 = html.Div([
    html.Div([
        dcc.Graph(id='map-figure', figure=map_fig),
        dcc.Dropdown(id='dropdown',
                     options=[{'label': i, 'value': i} for i in config['areaCodes']])
    ], className='g'),
    html.Div([
        dash_table.DataTable(
            id='datatable'
        )
    ]),
    html.Div([
        html.Pre(id='readout')
    ]),
])
