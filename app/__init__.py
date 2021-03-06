__author__="Ryan Wolfslayer"
__license__="GNU General Public License v3.0"
__maintainer__="Ryan Wolfslayer"
__email__="ryan.wolfslayer@gmail.com"

# __init__.py
# File brings different project components together into one importable application
# This file also creates the Dash data table used with Editing publications

from app.utility import cdm_pull
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_bootstrap import Bootstrap
from config import Config
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import datetime
from .models import db

import pandas as pd
import uuid

app = Flask(__name__) # start flask app
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db.init_app(app)
db.create_all(app=app)


local_url = "http://localhost:5000"

# create dash application for editting table
df = cdm_pull('not_needed_right_now')
df = df.reset_index(drop=True)
# dapp = dash application (i.e. table lookup)
dapp = dash.Dash(__name__, server=app, url_base_pathname="/edit_table/",
                 external_stylesheets=[dbc.themes.BOOTSTRAP])
dapp.title = "Edit webform"

dapp.server.secret_key = str(uuid.uuid4())

dapp.layout = dbc.Container(
    html.Div([
        html.H1('Select Record to Edit', className="p-5"),
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {'name': 'Title', 'id': 'Title', 'type': 'text'},
                {'name': 'Creator', 'id': 'Creator', 'type': 'text'},
                {'name': 'Published in', 'id': 'Published in', 'type': 'text'},
                {'name': 'DOI', 'id': 'DOI_Number', 'type': 'text'},
                {'name': 'Link', 'id': 'Public address', 'type': 'text'}
            ],
            virtualization=False,
            page_action='native',
            page_current=0,
            page_size=10,
            style_header={'backgroundColor': '#3d5a80', 'color': '#ffffff', 'text-align': 'center',
                          'font-family': 'sans-serif', 'font-weight': '700', 'width': 'auto', 'min-width': '100px', 'margin-bottom': '20%'},

            style_cell={'font-family': 'sans-serif',
                        'text-align': 'center', 'whitespace': 'normal', 'height': 'auto'},

            style_cell_conditional=[
                {
                    'if': {'column_id': 'Title'},
                    'textAlign': 'left'
                },
                {
                    'if': {'column_id': 'Creator'},
                    'textAlign': 'left'
                }
            ],
            style_as_list_view=True,
            data=df.to_dict('records'),
            row_selectable="single",
            selected_rows=[],
            filter_action='native',
            sort_action='native',

            style_table={
                'height': 400,
            },
            style_data={
                'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },

            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#E9ECEF',
                }
            ],
            css=[

            ]
        ),
        html.Br(),
        html.Hr(),
        html.Div(id='datatable-interactivity-container', className='p-3'),
        html.A(html.Button('Edit records', className="btn btn-success"),
               href='{}/edit'.format(local_url))
    ]))


@dapp.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")]
)
def update_display(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    selected_rows = [rows[i] for i in derived_virtual_selected_rows]

    try:
        # If the selected column is incorrect, select will stop working
        data = html.Div([html.H3('Selected Data', className="mb-3 ml-1"), html.Table(
            [
                html.Tr([html.Th('Title', className="col-2"), html.Td(selected_rows[0]
                                                                      ['Title'], className="col-6")], className="d-flex"),
                html.Tr([html.Th('Creators', className="col-2"), html.Td(selected_rows[0]
                                                                         ['Creator'], className="col-6")], className="d-flex"),
                html.Tr([html.Th('Published in', className="col-2"), html.Td(
                    selected_rows[0]['Published in'], className="col-6")], className="d-flex"),
                html.Tr([html.Th('DOI_Number', className="col-2"), html.Td(selected_rows[0]
                                                                           ['DOI_Number'], className="col-6")], className="d-flex")
            ], className="table"
        )])

    except IndexError:
        data = html.Div([html.H3('Selected Data', className="mb-3 ml-1"), html.Table(
            [
                html.Tr([html.Th('Title', className="col-2"), html.Td('', className="col-6"),
                         html.Td('', className="col-4 border-0")], className="d-flex"),
                html.Tr([html.Th('Creators', className="col-2"),
                         html.Td('', className="col-6")], className="d-flex"),
                html.Tr([html.Th('Published in', className="col-2"),
                         html.Td('', className="col-6")], className="d-flex"),
                html.Tr([html.Th('DOI_Number', className="col-2"),
                         html.Td('', className="col-6")], className="d-flex")
            ], className="table"
        )])

    flask.session['data'] = pd.DataFrame(selected_rows).to_json()

    return data

from app import views