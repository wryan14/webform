import dash
import flask
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import datetime

import pandas as pd

from utility import cdm_pull

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# df = df[['continent', 'country', 'pop', 'lifeExp']]  # prune columns for example
# df['Mock Date'] = [
#    datetime.datetime(2020, 1, 1, 0, 0, 0) + i * datetime.timedelta(hours=13)
#    for i in range(len(df))
# ]

df = cdm_pull('asdlfkj')

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {'name': 'Title', 'id': 'Title', 'type': 'text'},
            {'name': 'Creator', 'id': 'Creator', 'type': 'text'},
            {'name': 'Published in', 'id': 'Published in', 'type': 'text'},
            {'name': 'DOI', 'id': 'DOI_Number', 'type': 'text'},
            {'name': 'Link', 'id': 'Public address', 'type': 'text'}
        ],
        data=df.to_dict('records'),
        row_selectable="single",
        selected_rows=[],
        filter_action='native',

        style_table={
            'height': 400,
        },
        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),
    html.Div(id='datatable-interactivity-container'),
    html.Form([
        html.Button('Edit', type='submit')
    ], action="", method="POST")
])


@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")]
)
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    
    selected_rows=[rows[i] for i in derived_virtual_selected_rows]

    try:
        data = html.H1(selected_rows[0]['Title'])
    except IndexError:
        data = html.H1('Selected Data...')

    return data
    


# app.layout = html.Form([
#     dcc.Input(name='name'),
#     html.Button('Submit', type='submit')
# ], action='/post', method='post')

# @app.server.route('/post', methods=['POST'])
# def on_post():
#     data = flask.request.form
#     print(data)
#     return flask.redirect('/')


if __name__ == '__main__':
    app.run_server(debug=True)
