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



# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Skills'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Skills Database')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Hr(),
                        html.Div( 
                            [
                                html.H4('Skills'),
                                    dbc.Form([
                                        dbc.Row(
                                            [
                                                dbc.Label("Search by Skill Name", width=5),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='skillname_filter',
                                                        placeholder='Skill Name'
                                                    ),
                                                    width=5
                                                )
                                            ],className='mb-3'),
                                    #  html.Hr(), 
                                      dbc.Row(
                                            [
                                                dbc.Label("Filter by Skill Type", width=5),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=['Enabling','Functional'],
                                                            id='skilltype_filter',
                                                            placeholder='Skill Type'
                                                        ),
                                                        width=5
                                                    )
                                            ],
                                            className='mb-3' # add 1em bottom margin
                                        )]
                                    )]
                                ),
                                html.Div(
                                    "Insert Table here.",
                                    id='skillhome_skillist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )



@app.callback(
    [
        Output('skillhome_skillist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('skillname_filter', 'value'),
        Input('skilltype_filter','value') 
    ]
)
def employeehome_loademployeelist(pathname, searchterm, skilltype):
    print(pathname)
    if pathname == '/skills':

        sql = """ 
        SELECT DISTINCT skill_name, skill_type, skill_level, description
        FROM skills
        WHERE 1=1 and delete_date is null
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Skill Name','Skill Type','Skill Level','Skill Description'] #table column names
        
        
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND skill_name ILIKE %s "
            values += [f"%{searchterm}%"]
        
        if skilltype:
            sql += "AND skill_type = %s"
            values += [f"{skilltype}"]
    
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: # check if query returned anything
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return "No records to display"
        
    else: 
      raise PreventUpdate
