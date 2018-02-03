# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import pandas as pd
import numpy as np


# test imports
import json

external_css = [
    # dash stylesheet
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
]


''' Start : NHS cancer survival Data prep '''
url = 'cancersurvivalbystage.xls'
df_cancer = pd.read_excel(url, sheet_name='Table 1. Full Results',skiprows=5)

# clean the data
df_cancer = df_cancer[df_cancer['Sex']!='Persons']
df_cancer = df_cancer[df_cancer['Stage']!='All stages combined']
df_cancer['Number of Survivors']=df_cancer['Number of tumours']*df_cancer['Net Survival %']/100

cancer_years = df_cancer['Cohort'].unique()
cancer_site = df_cancer['Cancer site'].unique()

''' End : NHS cancer survivalData prep '''

''' Start : NHS 111 Data prep '''

# Data manipulation
url = 'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2017/12/NHS-111-MDS-time-series-to-2017-November-v2.xlsx'
df = pd.read_excel(url, sheet_name='Raw', skiprows=5, header=0, )#, sheet_name='All Attendances - Male', skiprows=3, header=0)
df.rename(columns={'Unnamed: 0':'Concat', 'Unnamed: 1':'Region', 'Unnamed: 2':'Provider Code', 'Unnamed: 3':'Date', 'Unnamed: 4':'Code', 'Unnamed: 5':'Area'}, inplace=True)
df['Year'] = pd.DatetimeIndex(df['Date']).year

# metric_options = ['Population', 'Total calls offered', 'No calls answered', 'Calls answered within 60 secs','Ambulance dispatches']
metric_options = ['Total calls offered', 'No calls answered', 'Calls answered within 60 secs','Ambulance dispatches']
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

df_table_111 = df.loc[0:20]


''' End : NHS 111 Data prep '''

''' Start : NHS Hospital Outpatient Activity data prep '''

url = 'https://digital.nhs.uk/media/34230/Hospital-Outpatient-Activity-2016-17-All-attendances/default/hosp-epis-stat-outp-all-atte-2016-17-tab.xls'
df_male = pd.read_excel(url, sheet_name='All Attendances - Male', skiprows=3, header=0)#names=("code", "provider_desc", "male", "female", "unkown", "total"))
df_female = pd.read_excel(url, sheet_name='All Attendances - Female', skiprows=3, header=0)#names=("code", "provider_desc", "male", "female", "unkown", "total"))

# Append the two data frames to one and other
df_male["Gender"] = "Male"
df_female["Gender"] = "Female"
df_out_act= pd.concat([df_male, df_female])

# unpivot the age columns
df_out_act= df_out_act.melt(id_vars=["Main Specialty Code", "Main Specialty Code Description","Gender"])
df_out_act.rename(columns={'variable':'Age Group'},inplace=True)
df_out_act['Age Group'] = df_out_act['Age Group'].astype('str')

# remove total columns
df_out_act= df_out_act[df_out_act["Main Specialty Code Description"] != "Total"]
df_out_act= df_out_act[df_out_act["Age Group"] != "Total"]
df_out_act.head(3)

# Define the sorter
sorter = ['0', '1-4', '5-9', '5-9 ', '10-14', '15', '16', '17', '18', '19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-120', 'Unknown']

# Create the dictionary that defines the order for sorting
sorterIndex = dict(zip(sorter,range(len(sorter))))

# Generate a rank column that will be used to sort
# the dataframe numerically
df_out_act['Age Group Rank'] = df_out_act['Age Group'].map(sorterIndex)

df_out_act.sort_values('Age Group Rank', inplace = True)
# df_out_act.drop('Age Group Rank', inplace = True)

# Clean up the data types
df_out_act["Age Group"] = df_out_act["Age Group"].astype("category")
df_out_act["Gender"] = df_out_act["Gender"].astype("category")

# Set up summarised code for Body Systems
divisions = pd.read_excel('divisions of clinical work.xlsx')
divisions.rename(columns={'Code': 'Main Specialty Code', 'Main Specialty Title': 'Main Specialty Code Description'}, inplace=True)
divisions.drop(columns='Main Specialty Code Description', inplace=True)
df_out_act= df_out_act.merge(divisions, how='left', on='Main Specialty Code')

# Set up group by
dimension = {'Divisions of clinical work': df_out_act["Divisions of clinical work"].unique(),'Gender': df_out_act['Gender'].unique()}
dimension_out_act_options = ['Gender', 'Divisions of clinical work']
dimension_out_act_picker = dimension_out_act_options[0]
df_out_act_grouped = df_out_act.groupby(by=[dimension_out_act_picker,'Age Group','Age Group Rank'], as_index=False).sum()
df_out_act_grouped.dropna(inplace=True)

''' Emd : NHS Hospital Outpatient Activity data prep '''

# set up footer
theme = {
    # 'font-family': 'Raleway',
    'background-color': '#ddd',
}

def create_footer():
    # p = html.P(
    #     children=[
    #         html.Span('Built with '),
    #         html.A('Plotly Dash',
    #                href='https://github.com/plotly/dash', target='_blank'),
    #         # html.Span(' and:'),
    #     ],
    #     style = {
    #         'display': 'inline-block',
    #         'width': '80%',
    #         # 'display': 'flex',
    #         'justify-content': 'left',
    #         'align-items':'left',
    #         'height':'2em',
    #         'margin': '0',
    #         'padding': '0.5em'
    #     }
    # )
    
    hashtags = 'plotly,dash,nhs'
    tweet = 'Dash UK NHS, a cool dashboard with Plotly Dash!'
    twitter_href = 'https://twitter.com/intent/tweet?hashtags={}&text={}'\
        .format(hashtags, tweet)
        
    twitter = html.A(
        children=html.I(children=[], className='fa fa-twitter fa-3x'),
        title='Tweet me!', href=twitter_href, target='_blank')

    linkedin = html.A(
        children=html.I(children=[], className='fa fa-linkedin-square fa-3x'),
        title='My Linkedin',
        href='https://www.linkedin.com/in/david-griffiths-5a9387a1/', target='_blank')
        
    github = html.A(
        children=html.I(children=[], className='fa fa-github fa-3x'),
        title='Repo on GitHub',
        href='https://github.com/wisemuffin/CS50project', target='_blank')

    li_right_first = {'line-style-type': 'none', 'display': 'inline-block'}
    li_right_others = {k: v for k, v in li_right_first.items()}
    li_right_others.update({'margin-left': '10px'})
    ul = html.Ul(
        children=[
            html.Li(twitter, style=li_right_first),
            html.Li(linkedin, style=li_right_others),
            html.Li(github, style=li_right_others),
        ],
        style={
            # 'width':'20%',
            # 'display': 'inline-block',
            'display': 'flex',
            'justify-content': 'center',
            'align-items':'center',
            'height':'70%',
            'margin': '0',
            'padding': '0.5em'
        }

    )

    div = html.Div([ul]) #div = html.Div([p, ul])
    footer_style = {
        'font-size': '1.2em',
        'background-color': theme['background-color'],
        'padding': '0.5em',
        'width': '100%',
        'position': 'relative',    
    }
    footer = html.Footer(div, style=footer_style)
    return footer

    
'''
Build the App
'''

app = dash.Dash()
server = app.server

app.config['suppress_callback_exceptions']=True # used when assigning callbacks to components that are generated by other callbacks (and therefore not in the initial layout), then you can suppress this exception by setting

# Choose the CSS styly you like
for css in external_css:
    app.css.append_css({'external_url': css})


tabs = {1:'111 Program', 2: 'Cancer Survival', 3:'Outpatient Activity 2016-17'}

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='NHS analysis', style = {'display': 'inline-block'}),
        html.Img(src='http://survation.com/wp-content/uploads/2014/12/NHS-logo.jpg', alt="Computer Hope logo small",style = {'position' : 'absolute', 'right':'0px', 'height':'auto', 'width':'5.5%', 'padding' : '10px'})
        # html.Img(src='http://survation.com/wp-content/uploads/2014/12/NHS-logo.jpg', style = {'position' : 'absolute', 'right':'0px', 'height':'5.5%', 'width':'5.5%', 'padding' : '10px'})
        ],
        style = {'display': 'inline-block'}
    ),

    # tabs to navigate between analysis
    dcc.Tabs(
        tabs=[
            {'label': '{}'.format(v), 'value': k} for k, v in tabs.items()
        ],
        value=1,
        id='tabs'
    ),
    # call backs will modify this tab-output depending on which tab is selected
    html.Div(id='tab-output'),
    
    # # Dave playing around with bootstrap
    # html.Div(children=
    #     [html.Button(children='Dave', className='btn btn-warning btn-lg', type='button'),
    #     html.Button(children='Dave', className='btn btn-info btn-xs', type='button'),
    #     html.Button(children='Dave', className='btn btn-link btn-sm', type='button'),
    #     html.Div(
    #         children=[html.Button(children='Dave', className='btn btn-primary btn-sm', type='button'),
    #             html.Button(children='Dave', className='btn btn-primary btn-sm', type='button')],
    #         className='btn-group btn-group-lg',
    #     ),
    #     ],
    #     className = 'jumbotron',
    #     style = {'margin':'1em'}
    # ),
    

    # # navigation buttons
    # html.Div(
    #     [
    #         html.Button('Back', id='back', style={
    #                     'display': 'inline-block'}),
    #         html.Button('Next', id='next', style={
    #                     'display': 'inline-block'})
    #     ],
    #     className='two columns offset-by-two'
    # )


     create_footer()


])

"""
START : Tab tab-output
"""

@app.callback(
    Output(component_id='tab-output',  component_property='children'),
    [Input(component_id='tabs', component_property='value')]
)
def set_tab_to_display(tab):
    if tab == 1:
        tab_display = html.Div(children=[
            dcc.Markdown('''
                # NHS's 111 Program

                NHS 111 is available 24 hours a day, 7 days a week, 365 days a year to respond to people’s health care needs when
                it’s not a life threatening situation, and therefore is less urgent than a 999 call.
                The service benefits callers where the GP isn’t an option, for instance when the caller is away from home or 
                the caller feels they cannot wait and is simply unsure of which service they require.

                The data is taken from the 
                [NHS 111 Minimum Data Set 2017-18](https://www.england.nhs.uk/statistics/statistical-work-areas/nhs-111-minimum-data-set/nhs-111-minimum-data-set-2017-18/).
                This tab demonstrates how to build high-quality, interactive
                artical that analysis performance.

                ***
                '''.replace('  ', ''), className='container',
                containerProps={'style': {'maxWidth': '650px'}}),


            
            html.Div(children=[
                dcc.Markdown('> What is going on with the 111 programs performance as it scalled up? One of the key KPIs for the 111 Program is anwsering calls as soon as possible. Lets focus on **% of calls answered in 60 seconds**.',
                    className='container',
                    containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                
                
                html.Div(children=dcc.Graph(id='nhs-111-graph-boxplot'),
                    # className='col-lg-8 col-md-12 col-sm-12 col-xs-12', # bootstrp used to arange space on the screen based on the device (iphone/tablet/pc screen size)
                    className='container',
                    ),
                dcc.Markdown('Peformance improved from inception to untill 2015. Lets investigate this performance decline.',
                    className='container',
                    containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                
                
                 dcc.Markdown('> How have care providers pefromed with the scalling of the NHS\'s 111 program?',
                     className='container',
                     containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                 
                html.Div(children=dcc.Graph(id='nhs-111-graph-3d'),
                    # className='col-lg-12 col-md-12 col-sm-12 col-xs-12', # bootstrp used to arange space on the screen based on the device (iphone/tablet/pc screen size)
                    ),
                dcc.Markdown('''
                We can see that most care providers start off with subdued 40%-60% performance at the start of the program. 
                In 2018 the program has matrured and most providers are above 80% and a large proportion are hitting 90%. 
                We also see the from the size of the bubble representing **population** that [Care UK](http://www.careuk.com/) and [NWAS](http://www.nwas.nhs.uk/) two of the largest care providers join the 111 program early 2016
                '''.replace('  ', ''),
                    className='container',
                    containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                    
                dcc.Markdown('> What other metrics might we want to explore in future analysis',
                    className='container',
                    containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                
                html.Div(children=[
                    html.Div(children=[
                        # dropdown to select the dimension
                        html.Div(dcc.Dropdown(
                            id = 'dimension_dropdown',
                            options=[
                                dict(label = dimension_options[i],value = dimension_options[i]) for i in range (0, len(dimension_options))
                            ],
                            value = dimension_options[0],
                        ), style={ 'display': 'inline-block', 'width':'30%'}),
                    
                        # dropdown of chilren of the selected dimension
                        html.Div(dcc.Dropdown(
                            id = 'dimension_element_dropdown',
                            ), style={'display': 'inline-block', 'width':'60%'})
                    ],
                    style={'width':'50%', 'margin':'0 auto'}
                    ),
                    
                    dcc.Graph(id='nhs-111-graph-bar',
                        # className='col-lg-8 col-md-12 col-sm-12 col-xs-12',
                    ),],
                    # className='col-lg-8 col-centered col-md-12 col-sm-12 col-xs-12',
                    className='container',  
                ),
                
                dcc.Markdown('Volumes of calls havent grown much since 2015. This suggest that other factors such as capacity, headcount, or moral may be to blame.',
                    className='container',
                    containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}),
                
                html.Div(className='clearfix'), # bootstrap clearfix fixes up issue where certain resoloutions show overlapping divs
            
            ]),

        ])
    elif tab == 3:
        tab_display = html.Div(children=[
            dcc.Markdown(children='''
                # title
                The data is taken from the [Hospital Episodes Statistics (HES)](https://digital.nhs.uk/catalogue/PUB30154) data warehouse. HES contains records of all admissions, 
                appointments and attendances for patients admitted to NHS hospitals in England.
                
                > The layout is designed in the style operational dashboard.
                '''.replace('  ', '').replace('title', tabs[3]),
                className='container',
                containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}
                ),

            html.Div(children=[
                dcc.Dropdown(
                    id = 'dimension_dropdown_out_act',
                    options=[
                        dict(label = dimension_out_act_options[i],value = dimension_out_act_options[i]) for i in range (0, len(dimension_out_act_options))
                    ],
                    value = dimension_out_act_options[0],
                    #style={'width': '48%'}
                ),],
                style={'width':'30%'},
                className='container',
            ),

            dcc.Graph(id='nhs-out-act-graph-bar', className='container',),
            
            dcc.Markdown(children='''
            * Women were the majority of outpatient attendances (54m vs 40m).
            * Patients aged 60 to 79 years accounted for over 30 per cent of outpacients.
            * Volume of outpatients have increase from 52 million in 2006-07 to 94 million in 2016-17.
            '''.replace('  ', '').replace('title', tabs[1]),
            className='container',
            containerProps={'style': {'maxWidth': '650px', 'padding':'1em'}}
            ),

            dcc.Graph(id='nhs-out-act-graph-donought', className='container',),

            ])
            
    elif tab == 2:
        tab_display = html.Div(children=[
            dcc.Markdown(children='''
                # title
                The data is taken from the [Hospital Episodes Statistics (HES)](https://digital.nhs.uk/catalogue/PUB30154) data warehouse. HES contains records of all admissions, 
                appointments and attendances for patients admitted to NHS hospitals in England.

                
                > The layout is designed in the style operational dashboard.
                '''.replace('  ', '').replace('title', tabs[2]),
                className='container',
                ),
            
            ## slider component not fully visable issue with dash core coponents version
            # html.Div(children=[
            #     dcc.Slider(
            #         id = 'cancer_year_slider',
            #         min=df_cancer['Cohort'].min(),
            #         max=df_cancer['Cohort'].max(),
            #         step=None,
            #         marks={str(year): str(year) for year in df_cancer['Cohort'].unique()},
            #         value = df_cancer['Cohort'].min(),
            #         ),
            #     ],
            #     style={'hieght': '5000px'}
            # ),
            html.Div(children=[
                html.Div(children=[
                    dcc.Dropdown(
                        id = 'cancer_year_slider',
                        options=[
                            dict(label = cancer_years[i],value = cancer_years[i]) for i in range (0, len(cancer_years))
                        ],
                        value = cancer_years[0],
                        ),],
                        style={'width':'30%'},
                    ),
                    dcc.Graph(id='nhs-cancer-graph-bar',
                        style={'height': '310px'},
                        hoverData={'points': [{'x': cancer_site[0]}]} # inital hover state
                    ),
                ],
                # style={'width': '25%'}
                className='container',
                style= {'maxWidth': '900px', 'padding':'1em'},
            ),
            

            # dcc.Graph(id='nhs-cancer-graph-bar',
            #     style={'height': '310px'},
            #     hoverData={'points': [{'x': cancer_site[0]}]} # inital hover state
            # ),
            
            # dcc.Markdown(children=''' **Hover Data**
            # Hover over a cancer site to change graphs below'''),
            dcc.Markdown(children='''
            
            > **Hover over** a cancer site in the bar char above to change graphs below.
            
            '''.replace('  ', ''),
            className='container',
            ),

            # className='col-lg-8 col-centered col-md-12 col-sm-12 col-xs-12'
            html.Div(children=[
                dcc.Graph(id='nhs-cancer-graph-line', style={'display': 'inline-block', 'width': '60%'}),
                dcc.Graph(id='nhs-cancer-graph-donought', style={'display': 'inline-block', 'width': '40%'})
            ],
            className='container',
            style= {'maxWidth': '1700px', 'padding':'1em'},
            # style={'display': 'inline-block','width': '100%'}
            ),
            
            ])


    else:
        tab_display = html.Div(children=[
            html.H1(children='in progress'),
            ])
    return tab_display

"""
START : NHS_cancer_survival
"""
@app.callback(
    Output(component_id='nhs-cancer-graph-bar', component_property='figure'),
    [Input(component_id='cancer_year_slider', component_property='value')]
)
def update_graph_cancer_survival_1(date_filter):
    df_grouped = df_cancer.groupby(by=['Cohort','Cancer site'], as_index=False).sum()
    df_grouped.dropna(inplace=True)

    data = [go.Bar(
      type = 'bar',
      x = df_grouped['Cancer site'],
      y = df_grouped[df_grouped['Cohort'] == date_filter]['Number of tumours'],
      name = date_filter,
      opacity = 0.8
    )]

    # plot titles and axis labels
    layout = go.Layout(
        barmode='stack', # switch between stack and group
        # title='<b>Outpatient-Activity-2016-17 by  </b>'+dimension_picker,
        yaxis = dict(
    #         type = 'log' # switches to a logarythmic scale
            title='<i>One–year net cancer survival</i>'
        ),
        xaxis=dict(
            title='<i>Cancer site</i>'
        ) ,
        bargap=0.1,
        bargroupgap=0.15
    )

    return go.Figure(data=data, layout=layout)

# # Testing Hover over functionality
# @app.callback(
#     Output(component_id='testhoverdata', component_property='children'),
#     [Input(component_id='nhs-cancer-graph-bar', component_property='hoverData')]
# )
# def testhoverdatafunc(hoverData):
#     # return json.dumps(hoverData, indent=2)
#     return str(type(hoverData['points'][0]['x']))
    
    
@app.callback(
    Output(component_id='nhs-cancer-graph-line', component_property='figure'),
    [Input(component_id='nhs-cancer-graph-bar', component_property='hoverData'),
    # Input(component_id='nhs-cancer-graph-bar', component_property='clickData')
    ]

)
def update_graph_cancer_survival_2(hoverData):
    cancer_site_filter = hoverData['points'][0]['x']
    df_grouped = df_cancer.groupby(by=['Cohort','Cancer site'], as_index=False).sum()
    df_grouped.dropna(inplace=True)

    data = [go.Scatter(
      mode = 'lines',
      x = df_grouped['Cohort'].unique(),
      y = df_grouped[df_grouped['Cancer site'] == cancer_site_filter]['Number of tumours'],
      name = 'Number of tumours',
      opacity = 0.8),
            
            go.Scatter(
      mode = 'lines',
      x = df_grouped['Cohort'].unique(),
      y = df_grouped[df_grouped['Cancer site'] == cancer_site_filter]['Number of Survivors'] / df_grouped[df_grouped['Cancer site'] == cancer_site_filter]['Number of tumours'] *100,
      name = 'Net Survival %s',
      yaxis='y2',
      opacity = 0.8),
           ]

    # plot titles and axis labels
    layout = go.Layout(
        barmode='stack', # switch between stack and group
        # title='<b>Outpatient-Activity-2016-17 by  </b>'+dimension_picker,
        yaxis = dict(
    #         type = 'log' # switches to a logarythmic scale
            title='<i>Number of tumours</i>'
        ),
        yaxis2=dict(
            title='<i>Net Survival %</i>',
            overlaying='y',
            side='right'
        ),
        xaxis=dict(
            title=cancer_site_filter+'<i> by year</i>'
        ) ,
        bargap=0.1,
        bargroupgap=0.15,
        showlegend=False
    )


    return go.Figure(data=data, layout=layout)



@app.callback(
    Output(component_id='nhs-cancer-graph-donought', component_property='figure'),
    [Input(component_id='nhs-cancer-graph-bar', component_property='hoverData'),
    # Input(component_id='nhs-cancer-graph-bar', component_property='clickData'),
    Input(component_id='cancer_year_slider', component_property='value')]
    )


def update_graph_cancer_survival_3(x, y):
    date_filter = y
    cancer_site_filter = x['points'][0]['x']
    df_filtered = df_cancer[(df_cancer['Cohort'] == date_filter) & (df_cancer['Cancer site'] == cancer_site_filter)]
    df_grouped = df_filtered.groupby(by=['Stage'], as_index=False).sum()
    df_grouped.dropna(inplace=True)
    
    #calculates the whole value of the pie chart
    centre_value_pie = df_grouped['Number of tumours'].sum()

    data = [go.Pie(
        values = df_grouped['Number of tumours'],
        # values = df_grouped[(df_grouped['Cohort'] == date_filter) ]['Number of tumours'],
        labels = 'Stage: ' + df_cancer['Stage'].astype(str).unique(), #df_grouped['Stage'].unique(),
        type = 'pie',
        hole = 0.7,
        opacity = 0.8),
    ]

    # plot titles and axis labels
    layout = go.Layout(
        annotations = [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": str("{:,.0f}".format(centre_value_pie)) +' Tumours', # resulting from ' + cancer_site_filter + " Cancer for the year " + str(date_filter),
                "align": 'centre',
            }
        ]
    )
    return go.Figure(data=data, layout=layout)



"""
END : NHS_cancer_survival
"""

"""
START : NHS_out_act_tab-output
"""
@app.callback(
    Output(component_id='nhs-out-act-graph-bar', component_property='figure'),
    [Input(component_id='dimension_dropdown_out_act', component_property='value')]
)
def update_graph(dimension_picker):
    df_grouped = df_out_act.groupby(by=[dimension_picker,'Age Group','Age Group Rank'], as_index=False).sum()
    df_grouped.dropna(inplace=True)

    # stops traces from exceeding max trace limit
    if len(dimension[dimension_picker]) >6:
        len_dimension_picker = 6
    else:
        len_dimension_picker = len(dimension[dimension_picker])


    data = [go.Bar(
      type = 'bar',
      x = df_grouped['Age Group'],
      y = df_grouped[df_grouped[dimension_picker] == df_grouped[dimension_picker].unique()[i]]['value'], # filters out values not belonging to the ith demension element
      name = df_grouped[dimension_picker].unique()[i],
      opacity = 0.8
    ) for i in range(0, len_dimension_picker)]

    # plot titles and axis labels
    layout = go.Layout(
        barmode='stack', # switch between stack and group
        # title='<b>Outpatient-Activity-2016-17 by  </b>'+dimension_picker,
        yaxis = dict(
    #         type = 'log' # switches to a logarythmic scale
            title='<i>Outpatient volume</i>'
        ),
        xaxis=dict(
            title='<i>Age groups</i>'
        ) ,
        bargap=0.1,
        bargroupgap=0.15
    )


    return go.Figure(data=data, layout=layout)

@app.callback(
    Output(component_id='nhs-out-act-graph-donought', component_property='figure'),
    [Input(component_id='dimension_dropdown_out_act', component_property='value')]
)
def update_pie_chart_data(dimension_picker):

    values = []

    for option in df_out_act[dimension_picker].dropna().unique():
        df_grouped = df_out_act.groupby(by=[dimension_picker,'Age Group','Age Group Rank'], as_index=False).sum()
        value = df_grouped[df_grouped[dimension_picker] == option]['value'].sum()
        values.append(value)

    fig = {
      "data": [
        {
          "values": values,
          "labels": df_out_act[dimension_picker].dropna().unique(),
          # "domain": {"x": [0, .48]},
          "name": "Outpatient-Activity-2016-17",
          "hoverinfo":"label+percent+name+value",
          "hole": .7,
          "align": 'centre',
          "type": "pie"
        }],
      "layout": {
            # "title":"Outpatient-Activity-2016-17",
            "annotations": [
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": "Outpatient-Activity-2016-17",
                    "align": 'centre',
                    # "x": 0.12,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": "{:,.0f}".format(df_out_act['value'].sum()),
                    "align": 'centre',
                    # "x": 0.19,
                    "y": 0.4
                }

            ]
        }
    }
    return fig

"""
END : NHS_out_act_tab-output
"""

"""
START : NHS_111_tab-output
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

    # use the DataFrame columns for generating data
    data = [go.Scatter(
        x = df_grouped['Date'],
        y = df_grouped[metric_options_selected[i]],
        mode = 'lines',
        name = metric_options_selected[i],
#         text = df_grouped[metric_options_selected[i]],
        opacity = 0.8,
    ) for i in range(0, len(metric_options_selected))] # loop through traces

    # plot titles and axis labels
    layout = go.Layout(
        barmode='group',#'group', # switch between stack and group
        # title='<b>NHS 111 calls where  </b>'+ dimension_picker+' = '+dimension_element_picker,
        yaxis = dict(
            # type = 'log', # switches to a logarythmic scale
            title='<i>Volume</i>'
        ),
#         xaxis=dict(
#             title='<i>Date</i>'
#         )
    )

    return go.Figure(data=data, layout=layout)



@app.callback(
    Output(component_id='nhs-111-graph-3d', component_property='figure'),
    [Input(component_id='dimension_dropdown', component_property='value')]
)
def set_display_children(dimension_picker='Provider Code'):
    df_grouped_3d = df.groupby(by=['Date', 'Provider Code'], as_index=False).sum()

    data = [go.Scatter3d(
        x=df_grouped_3d['Date'],
        z=df_grouped_3d['Calls answered within 60 secs']/df_grouped_3d['Total calls offered']*100,
        y=df_grouped_3d['Provider Code'],
        mode='markers',
        marker=dict(
            size=df_grouped_3d['Total calls offered']/8000, # visualises the volume of calls
            color=df_grouped_3d['Calls answered within 60 secs']/df_grouped_3d['Total calls offered'],                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )]
    
    BACKGROUND = 'rgb(230, 230, 230)'
    
    COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                    [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]
                    
    xlabel = ''
    ylabel = 'Provider Code'
    zlabel = '% Calls answered within 60 secs'
    
    def axis_template_3d( title, type='linear' ):
        return dict(
            showbackground = True,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(255, 255, 255)',
            title = title,
            type = type,
            zerolinecolor = 'rgb(255, 255, 255)'
        )


    layout = go.Layout(
        scene = dict(
            xaxis = dict(
                title=''),
            yaxis = dict(
                title='Provider Code'),
            zaxis = dict(
                tickformat=".0%",
                title='Calls answered within 60 secs'),
                ),
                margin=dict(l=0, r=0,b=0,t=0),
        )

    
    return go.Figure(data=data, layout=layout)
    
@app.callback(
    Output(component_id='nhs-111-graph-boxplot', component_property='figure'),
    [Input(component_id='dimension_dropdown', component_property='value')]
)
def set_display_children(dimension_picker='Provider Code'):
    df_grouped_box = df.groupby(by=['Year', 'Provider Code'], as_index=False).sum()
    df_grouped_box['% Calls answered within 60 secs'] = df_grouped_box['Calls answered within 60 secs']/df_grouped_box['Total calls offered']
    df_grouped_box = df_grouped_box[['Year', 'Provider Code', '% Calls answered within 60 secs']]


    colours = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(127, 150, 220, 0.5)', 'rgba(127, 300, 50, 0.5)']

    traces = []

    for date, cls in zip(df_grouped_box['Year'].unique(), colours):
            traces.append(go.Box(
                y=df_grouped_box[df_grouped_box['Year'] == date]['% Calls answered within 60 secs'],
                name=date,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker=dict(
                    size=2,
                ),
                line=dict(width=1),
            ))


    layout = go.Layout(
        title='% Calls answered within 60 secs',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
            tickformat=".0%",
            
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        # paper_bgcolor='rgb(243, 243, 243)',
        # plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True
    )

    return go.Figure(data=traces, layout=layout)

"""
END: NHS_111_tab-output
"""



if __name__ == '__main__':
    app.run_server(debug=True)
