# from dash import dcc
# import plotly.graph_objs as go

# fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# dcc.Graph(figure=fig)



# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
import dbconnect as db

from dash import dcc
import plotly.graph_objs as go

#fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

import plotly.graph_objects as go

# get categories as list per skill and role via sql based on employee number


categories = ['Data Analytics','Data Visualization','Problem Management',
              'Business Needs Analysis', 'Computational Modelling']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[1, 5, 2, 2, 3],
      theta=categories,
      fill='toself',
      name='Product A'
))
fig.add_trace(go.Scatterpolar(
      r=[4, 3, 2.5, 1, 2],
      theta=categories,
      fill='toself',
      name='Product B'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=False
)

# dynamic dropdown https://community.plotly.com/t/updating-a-dropdown-menus-contents-dynamically/4920/2 

layout = html.Div(
    [
        html.H2('Results'), # Page Header
        html.Hr(),
        dbc.Row([
                
                    dbc.Label("Employee Number", width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            searchable=True,
                            options = [
                                dict(label='Employee 1', value=1),
                                dict(label='Employee 2', value=2),
                                dict(label='Employee 3', value=3),
                            ],
                            style={'color': 'black'},
                            id = 'dropdown-employees'  
                        ))]),
        dcc.Graph(id='scatterplot-skills',figure=fig),
        ]
)

# @app.callback(
#     [
#         Output('scatterplot-skills', 'figure')
#     ],
#     [
#         Input('dropdown-employees', 'children'),
#     ]
# )

# def skillshome_loadskillslist(pathname, searchterm):
#     print(pathname)
#     if pathname == '/skills':
#         # 1. Obtain records from the DB via SQL
#         # 2. Create the html element to return to the Div
#         sql = """ SELECT skill_id, skill_name, level, description
#         FROM skills
#         WHERE delete_date is null
#         """
#         values = [] # blank since I do not have placeholders in my SQL
#         cols = ['Skill Code', 'Skill Name', 'Level', 'Description']
        
        