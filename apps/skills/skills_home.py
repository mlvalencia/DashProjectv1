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
                        html.H3('Manage Records')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Movie Btn
                            [
                                # Add movie button will work like a 
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Skill",
                                    href='/skills/skills_profile'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div( # Create section to show list of movies
                            [
                                html.H4('Find Skills'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Title", width=1),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='moviehome_titlefilter',
                                                        placeholder='Skill Name'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3' # add 1em bottom margin
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with skills will go here.",
                                    id='skillhome_skilllist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)




@app.callback(
    [
        Output('skillhome_skilllist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('moviehome_titlefilter', 'value'), # changing the text box value should update the table
    ]
)

def skillshome_loadskillslist(pathname, searchterm):
    print(pathname)
    if pathname == '/skills':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT skill_id, skill_name, level, description
        FROM skills
        WHERE delete_date is null
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Skill Code', 'Skill Name', 'Level', 'Description']
        
        
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND skill_name ILIKE %s "

            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: # check if query returned anything
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
        
    else:
        raise PreventUpdate