from dash.dependencies import Input, Output
import pandas as pd
import json
from app import app, data_ctrl
import ast
import plotly.express as px
import plotly.graph_objs as go

# Map the columns to the data
cols = [{"id": "areaName", "name": "Name"},
        {"id": "LtlaName", "name": "Local Authority"},
        {"id": "latest.newCasesBySpecimenDate.rollingSum", "name": "Number of Cases"},
        {"id": "latest.newCasesBySpecimenDate.rollingRate", "name": "Cases per 100k population"}]


def get_row_from_hover(hover_data):
    # Get the correct row from the dataframe
    area_code = hover_data['points'][0]['location']
    df = data_ctrl.data
    row = df[df['areaCode'] == area_code]

    # Unstack the dataframe to make it easier to manipulate
    row = row.unstack()
    row.index = row.index.get_level_values(0)

    return row


@app.callback(
    [Output('datatable', 'data'), Output('datatable', 'columns')],
    Input('map-figure', 'hoverData'))
def display_hover_data(hover_data):

    row = get_row_from_hover(hover_data)

    # Get the columns to include in the dataframe
    row = row[['areaName',
               'LtlaName',
               'latest.newCasesBySpecimenDate.rollingSum',
               'latest.newCasesBySpecimenDate.rollingRate']]
    data_for_table = row.to_frame().T.to_dict('records')

    return data_for_table, cols


@app.callback(
    Output('rolling-figure', 'figure'),
    Input('map-figure', 'hoverData'))
def display_rolling_figure(hover_data):

    # Get the time-series data
    time_series_data = data_ctrl.time_series
    mean_cases = time_series_data.groupby('date').mean().reset_index()

    # Get the latest-case data for that row
    area_code = hover_data['points'][0]['location']
    data = time_series_data[time_series_data['areaCode'] == area_code]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=data['date'],
                                y=data['rollingRate'],
                                name=data['areaName'].unique()[0],
                                mode='lines+markers',
                                marker=dict(color='green', size=10),
                                line=dict(color='green')))
    figure.add_trace(go.Scatter(x=mean_cases['date'],
                                y=mean_cases['rollingRate'],
                                mode='lines',
                                name='Nottinghamshire Average',
                                line=dict(color='blue')))

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    figure.layout.yaxis.range = [0, 1200]
    figure.layout.yaxis.dtick = 200
    figure.layout.xaxis.range = [
        pd.to_datetime('2020-08-01'), data['date'].max()]

    figure.update_layout(plot_bgcolor='white')
    figure.update_yaxes(showgrid=True, zeroline=True,
                        gridcolor='#CCCCCC', showline=True)
    figure.update_layout(legend=dict(yanchor="top",
                                     y=0.99,
                                     xanchor="left",
                                     x=0.01
                                     ))

    return figure
