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
        html.H2('Roles'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Roles Database')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Hr(),
                        html.Div( 
                            [
                                html.H4('Find Roles'),
                                    dbc.Form([
                                        dbc.Row(
                                            [
                                                dbc.Label("Search by Role Name", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='rolename_filter',
                                                        placeholder='Role Name'
                                                    ),
                                                    width=5
                                                )
                                            ],className='mb-3'),
                                    #  html.Hr(), 
                                      dbc.Row(
                                            [
                                                dbc.Label("Filter by Division", width=2),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[{'label':division, 'value':division} for division in list_division],
                                                            id='employee_division',
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
                                    id='rolehome_rolelist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )



@app.callback(
    [
        Output('rolehome_rolelist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('rolename_filter', 'value'), # changing the text box value should update the table
        Input('employee_division','value')
    ]
)
def rolehome_rolelist_fxn(pathname, searchterm,division):
    print(pathname)
    if pathname == '/roles':

        sql = """ 
        SELECT role_id, role_name, division
        FROM roles
        WHERE 1=1
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Role ID', 'Role Name', 'Division'] #table column names
        
        
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND role_name ILIKE %s "
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
