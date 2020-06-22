from flask import Flask
from config import Config
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import datetime

import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

from app import views
from app.utility import cdm_pull

# create dash application for editting table
df = cdm_pull('not_needed_right_now')

dapp = dash.Dash(__name__, server=app, url_base_pathname="/edit_table/")
dapp.title = "Edit webform"

dapp.layout = html.Div([
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


@dapp.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")]
)
def update_display(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    selected_rows=[rows[i] for i in derived_virtual_selected_rows]

    try:
        data = html.H1(selected_rows[0]['Title'])
    except IndexError:
        data = html.H1('Selected Data...')

    return data
