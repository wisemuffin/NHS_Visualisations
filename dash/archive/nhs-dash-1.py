# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import pandas as pd
import numpy as np

# Data manipulation
url = 'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2017/12/NHS-111-MDS-time-series-to-2017-November-v2.xlsx'
df = pd.read_excel(url, sheet_name='Raw', skiprows=5, header=0, )#, sheet_name='All Attendances - Male', skiprows=3, header=0)
df.rename(columns={'Unnamed: 0':'Concat', 'Unnamed: 1':'Region', 'Unnamed: 2':'Provider Code', 'Unnamed: 3':'Date', 'Unnamed: 4':'Code', 'Unnamed: 5':'Area'}, inplace=True)

metric_options = ['Population', 'Total calls offered', 'No calls answered', 'Calls answered within 60 secs','Ambulance dispatches']
dimension_options = ['Area','Region','Provider Code']
# Future development: Could allow users to select metrics
metric_options_selected = metric_options

# Interactive variables
dimension_picker = dimension_options[0]
dimension_element_picker = df[dimension_picker][0]

# Data transformation
df_filtered = df[df[dimension_picker] == dimension_element_picker]
# df_filtered = df
df_grouped = df_filtered.groupby(by=[dimension_picker,'Date'], as_index=False).sum()



app = dash.Dash()

# Choose the CSS styly you like
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Markdown(children=markdown_text),

    dcc.Tabs(
        tabs=[
            {'label': 'Tab {}'.format(i), 'value': i} for i in range(1, 5)
        ],
        value=3,
        id='tabs'
    ),
    html.Div(id='tab-output'),
# ], style={
#     'width': '80%',
#     'fontFamily': 'Sans-Serif',
#     'margin-left': 'auto',
#     'margin-right': 'auto'
# })

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
        dcc.Graph(
            id='example-graph2',
            figure={
                'data': [go.Scatter(
                    x = df_grouped['Date'],
                    y = df_grouped[metric_options_selected[i]],
                    mode = 'lines',
                    name = metric_options_selected[i],

                ) for i in range(0, len(metric_options_selected))],
        'layout': go.Layout(
            barmode='group',#'group', # switch between stack and group
            title='<b>NHS 111 calls where  </b>'+ dimension_picker,#+' = '+dimension_element_picker,
            yaxis = dict(
                type = 'log', # switches to a logarythmic scale
                title='<i>Volume</i>'
                ),
            )
            }
        )
])


app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])


# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='my-id', component_property='value')]
# )
# def update_output_div(input_value):
#     return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
