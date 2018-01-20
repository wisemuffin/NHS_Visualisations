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
# dimension_element_picker = list(df[dimension_picker].unique())
# dimension_element_picker.insert(0, 'All')

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
    html.H1(children='NHS analysis'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Markdown(children=markdown_text),

    # tabs to navigate between analysis
    dcc.Tabs(
        tabs=[
            {'label': 'Tab {}'.format(i), 'value': i} for i in range(1, 5)
        ],
        value=3,
        id='tabs'
    ),
    html.Div(id='tab-output'),

    # call backs will modify this container depending on which tab is selected
    html.Div(id='container'),


    # graph component that will be passed layout and data from the function update_graph().
    dcc.Graph(id='nhs-111-graph-bar'),

    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),

    # navigation buttons
    html.Div(
        [
            html.Button('Back', id='back', style={
                        'display': 'inline-block'}),
            html.Button('Next', id='next', style={
                        'display': 'inline-block'})
        ],
        className='two columns offset-by-two'
    ),

    # dropdown to select the dimension
    dcc.Dropdown(
        id = 'dimension_dropdown',
        options=[
            dict(label = dimension_options[i],value = dimension_options[i]) for i in range (0, len(dimension_options))
        ],
        value = dimension_options[0]
    ),

    # dropdown of chilren of the selected dimension
    dcc.Dropdown(id = 'dimension_element_dropdown')

])

"""
START : Tab Container
"""

@app.callback(
    Output(component_id='container',  component_property='children'),
    [Input(component_id='tabs', component_property='value')]
)
def set_tab_to_display(tab):
    if tab == 1:
        tab_display = html.Div(children=[
            dcc.Graph(id='nhs-111-graph-bar')
        ])
    else:
        tab_display = html.Div(children=[

        ])
    return tab_display


"""
START : NHS_111_Container
"""

# sets the children of dimension_element_dropdown
@app.callback(
    Output(component_id='dimension_element_dropdown', component_property='options'),
    [Input(component_id='dimension_dropdown', component_property='value')]
)
def set_dimension_elements(dimension_picker):
    options = df[dimension_picker].unique()
    options = [{'label': i, 'value': i} for i in options]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# sets the initial value in the dimension_element_dropdown when the dimension_dropdown dropdown changes i.e. chaning the dimension.
@app.callback(
    Output(component_id='dimension_element_dropdown', component_property='value'),
    [Input(component_id='dimension_element_dropdown', component_property='options')]
)
def set_display_children(available_options):
    return available_options[0]['value']


@app.callback(
    Output(component_id='nhs-111-graph-bar', component_property='figure'),
    [Input(component_id='dimension_dropdown', component_property='value'),
    Input(component_id='dimension_element_dropdown', component_property='value')]
)
def update_graph(dimension_picker, dimension_element_picker):
    # if all is selected in the dimension_element_picker then do not include a dimension in the group by clause
    if dimension_element_picker == 'All':
        df_grouped = df.groupby(by=['Date'], as_index=False).sum()
    else:
        df_filtered = df[df[dimension_picker] == dimension_element_picker]
        df_grouped = df_filtered.groupby(by=[dimension_picker,'Date'], as_index=False).sum()

    # Future development: Could allow users to select metrics
    metric_options_selected = metric_options

    return {
        # use the DataFrame columns for generating data
        'data' : [go.Scatter(
            x = df_grouped['Date'],
            y = df_grouped[metric_options_selected[i]],
            mode = 'lines',
            name = metric_options_selected[i],
    #         text = df_grouped[metric_options_selected[i]],
            opacity = 0.8,
        ) for i in range(0, len(metric_options_selected))], # loop through traces

        # plot titles and axis labels
        'layout' : go.Layout(
            barmode='group',#'group', # switch between stack and group
            title='<b>NHS 111 calls where  </b>'+ dimension_picker+' = '+dimension_element_picker,
            yaxis = dict(
                type = 'log', # switches to a logarythmic scale
                title='<i>Volume</i>'
            ),
    #         xaxis=dict(
    #             title='<i>Date</i>'
    #         )
        )
    }

"""
END: NHS_111_Container
"""



if __name__ == '__main__':
    app.run_server(debug=True)
