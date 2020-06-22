import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import datetime

import pandas as pd

from utility import cdm_pull

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
#df = df[['continent', 'country', 'pop', 'lifeExp']]  # prune columns for example
#df['Mock Date'] = [
#    datetime.datetime(2020, 1, 1, 0, 0, 0) + i * datetime.timedelta(hours=13)
#    for i in range(len(df))
#]

df = cdm_pull('asdlfkj')

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(

    columns=[
        {'name': 'Title', 'id': 'Title', 'type': 'text'},
        {'name': 'Creator', 'id': 'Creator', 'type': 'text'},
        {'name': 'Published in', 'id': 'Published in', 'type': 'text'},
        {'name': 'DOI', 'id': 'DOI_Number', 'type': 'text'},
        {'name': 'Link', 'id': 'Public address', 'type': 'text'}
    ],
    data=df.to_dict('records'),
    filter_action='native',

    style_table={
        'height': 400,
    },
    style_data={
        'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    }
)


if __name__ == '__main__':
    app.run_server(debug=True)