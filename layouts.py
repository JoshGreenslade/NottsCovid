import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import config

layout1 = html.Div([
    html.Div([
        dcc.Graph(id='map-figure'),
        dcc.Dropdown(id='dropdown',
                     options=[{'label': i, 'value': i} for i in config['areaCodes']])
    ], className='g'),
    html.Div([
        dash_table.DataTable(
            id='datatable'
        )
    ]),
])
