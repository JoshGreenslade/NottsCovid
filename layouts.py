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
                               center={'lat': 53.10902922895685,
                                       'lon': -1.046953174103217},
                               zoom=9,
                               opacity=0.4,
                               color_continuous_scale='Aggrnyl')
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_accesstoken='pk.eyJ1IjoiamdyZWVuc2xhZGUiLCJhIjoiY2tpcnJqOWF6MGs3dTMwb2JyYWN4MzNtZCJ9.M8BhWR_plOZDW2v8UaZeJA')
map_fig.update(layout_coloraxis_showscale=False)


def generate_table(dataframe, cols):
    """ Generates a html table based on a dataframe and column mapping """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(cols[col]) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])


def get_top_5_cases():
    """ Returns the top 5 areas with the highest case rate
    """
    # Get the data
    top_5_locs = data_ctrl.data
    top_5_locs = top_5_locs.sort_values(
        'latest.newCasesBySpecimenDate.rollingRate', ascending=False).head()

    # Get the columns
    top_5_locs = top_5_locs[['areaName', 'LtlaName',
                             'latest.newCasesBySpecimenDate.rollingRate']]
    top_5_locs_cols = {'areaName': 'Name',
                       'LtlaName': 'Local Authority',
                       'latest.newCasesBySpecimenDate.rollingRate': 'Cases per 100k population'}

    return generate_table(top_5_locs, top_5_locs_cols)


def get_total_cases():

    data = data_ctrl.data
    total_cases = data['latest.newCasesBySpecimenDate.rollingSum'].sum()

    return html.Div([
        html.H4(f'Total Cases: '),
        html.H2(f' {round(total_cases, 0)}')
    ])


def get_average_rate():

    data = data_ctrl.data
    total_rate = data['latest.newCasesBySpecimenDate.rollingRate'].mean()

    return html.Div([
        html.H4(f'Rate Per 100K population: '),
        html.H2(f' {round(total_rate, 1)}')
    ])


layout1 = html.Div([
    html.Div([
        html.H1('Greater Nottingham Covid Dashboard')
    ], className='nav'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    get_total_cases(),
                ], className=''),
                html.Div([
                    get_average_rate(),
                ], className=''),
                html.Div([
                    html.Div([
                        html.H3('Top 5 areas')
                    ]),
                    get_top_5_cases(),
                ], className='top5')
            ], className='KPI'),



            dcc.Graph(id='map-figure', figure=map_fig,
                      className='map_graph'),
            # html.Div([})
            #
            # ], className='card rate_graph')


        ], className='main_content'),
        html.Div([
            dcc.Graph(id='rolling-figure',
                      className='rolling_figure')
        ],  className='roll_container')

        # html.Div([
        #     dash_table.DataTable(
        #         id='datatable',
        #         data=[]
        #     )
        # ], className='card'),
    ], className='container')
])
