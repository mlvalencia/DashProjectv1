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

def get_employee_division():   
    sql_emp = """
    SELECT DISTINCT division FROM roles
        """
    values=[]
    cols=['division']
    df = db.querydatafromdatabase(sql_emp,values,cols)
    return df['division'].tolist()

list_division = (get_employee_division())

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Skills Mapping'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Skills Mapping')
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
                                                dbc.Label("Search by Role Name", width=5),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='rolename_filter',
                                                        placeholder='Role'
                                                    ),
                                                    width=5
                                                )
                                            ],className='mb-3'),
                                    #  html.Hr(), 
                                      dbc.Row(
                                            [
                                                dbc.Label("Filter by Division", width=5),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[{'label':division, 'value':division} for division in list_division],
                                                            id='division_filter',
                                                            placeholder='Division'
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
                                    id='skillhome_skillist_role'
                                )
                            ]
                        )
                    ]
                )
            ]
        )



@app.callback(
    [
        Output('skillhome_skillist_role', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('rolename_filter', 'value'),
        Input('division_filter','value')
    ]
)
def skillhome_skillist_role(pathname, searchterm, division):
    print(pathname)
    if pathname == '/skills_map':

        sql = """
        SELECT a.role_name, c.skill_name, c.description, b.expected_rating
        FROM roles a
        JOIN test b 
            on a.role_id = b.role_id 
        JOIN skills c 
            ON b.skill_id = c.skill_id 
        WHERE 1=1 
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Role','Skill Name','Description','Expected Rating'] #table column names
        
        
        ### ADD THIS IF BLOCK
        if searchterm:
            sql += "AND role_name ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if division:
            sql += "AND division ILIKE %s"
            values += [f"%{division}%"]
    
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: # check if query returned anything
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return "No records to display"
        
    else: 
      raise PreventUpdate
