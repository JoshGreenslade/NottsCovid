from dash.dependencies import Input, Output
import pandas as pd
import json
from app import app, data_ctrl
import ast
import plotly.express as px

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

    row = get_row_from_hover(hover_data)
    cases_by_date = row['newCasesBySpecimenDate']
    data = pd.DataFrame(ast.literal_eval(cases_by_date))
    data['date'] = pd.to_datetime(data['date'])

    figure = px.line(x=data['date'],
                     y=data['rollingRate'],
                     labels={'x': 'Date', 'y': 'Cases per 100k population'})

    figure.layout.yaxis.range = [0, 1200]
    figure.layout.xaxis.range = [
        pd.to_datetime('2020-08-01'), data['date'].max()]
    figure.update_traces(mode='lines+markers')

    return figure
