


##############################################################################
# #######################################################################################################
# Usual Dash dependencies
from dash import dcc
from dash import html, ctx 
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
import dbconnect as db


def get_employee_names():   #get those w results only
    sql_emp = """

    SELECT distinct d.employee_name
        FROM roles a
        JOIN test b 
            on a.role_id = b.role_id 
        JOIN skills c 
            ON b.skill_id = c.skill_id 
        JOIN employees d 
            ON a.role_id = d.role_id
        JOIN results e 
            ON d.employee_id = e.employee_id and b.test_id = e.test_id
        WHERE 1=1 

        """
    values=[]
    cols=['employee_name']
    df = db.querydatafromdatabase(sql_emp,values,cols)
    return df['employee_name'].tolist()

list_employees = (get_employee_names())

def blank_fig():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[1,3,2,5,4],
        theta=['','','','',''],
        fill='toself',
        name='No Data. Select Employee Name'
    ))
    fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 5]
                )),
            showlegend=False,
            title = f"Please Select Employee Name"
            )
    return [fig]



# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Results'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Competency Mapping by Employee')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Hr(),
                        html.Div( 
                            [
                                    dbc.Form([
                                        # dbc.Row(
                                        #     [
                                        #         dbc.Label("Employee Name", width=5),
                                        #         dbc.Col(
                                        #             dbc.Input(
                                        #                 type='text',
                                        #                 id='employeename_filter',
                                        #                 placeholder='Enter Employee Name'
                                        #             ),
                                        #             width=5
                                        #         )
                                        #     ],className='mb-3'),
                                    dbc.Row(
                                            [
                                                dbc.Label("Employee Name", width=5),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[{'label':employee, 'value':employee} for employee in list_employees],
                                                            id='employeename_dropdown',
                                                            placeholder='Search Employee Name'
                                                        ),
                                                        width=5
                                                    )
                                            ],
                                            className='mb-3' # add 1em bottom margin
                                        ),
                                    #  html.Hr(), 
                                      dbc.Row(
                                            [
                                                dbc.Label("Skill Type", width=5),
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
                                     [dcc.Graph(id='spiderplot_results',figure=blank_fig()),
                                     html.Button(id='reset',children = 'Clear')]
                                )
                            ]
                        )
                    ]
                )
            ]
        )



@app.callback(
    [
        Output('spiderplot_results', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('employeename_dropdown','value'),
        Input('skilltype_filter','value'),
        Input('reset','n_clicks')
    ]
)
def spiderplotresults_here(pathname,emp_name,skilltype,n_clicks):
    print(pathname)
    #if emp_name is not None:
    # if ctx.triggered_id == 'reset':
    #     fig1 = go.Figure(data=[go.Scatter(x=[], y=[])])
    #     return fig1
   
    if ctx.triggered_id == 'reset':
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[1,3,2,5,4],
            theta=['','','','',''],
            fill='toself',
            name='No Data. Select Employee Name'
        ))
        fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                    )),
                showlegend=False,
                title = f"Please Select Employee Name"
                )
        return [fig]

    elif (emp_name is not None):
        if pathname == '/results':

            sql = """ 
            SELECT distinct d.employee_name, a.role_name,  c.skill_name, b.expected_rating, e.rating, d.employee_id, a.division
            FROM roles a
            JOIN test b 
                on a.role_id = b.role_id 
            JOIN skills c 
                ON b.skill_id = c.skill_id 
            JOIN employees d 
                ON a.role_id = d.role_id
            JOIN results e 
                ON d.employee_id = e.employee_id and b.test_id = e.test_id
            WHERE 1=1 
            """
            values = [] # blank since I do not have placeholders in my SQL
            cols = ['employee_name','role_name','skill_name','expected_rating','rating','employee_id','division'] #table column names
            
            ### ADD THIS IF BLOCK
            # if searchterm:
            #     # We use the operator ILIKE for pattern-matching
            #     sql += "AND d.employee_name ILIKE %s "
            #     values += [f"%{searchterm}%"]

            if emp_name:
                sql += "AND d.employee_name ILIKE %s"
                values += [f"%{emp_name}%"]
            
            if skilltype:
                sql += "AND skill_type ILIKE %s"
                values += [f"%{skilltype}%"]

            df = db.querydatafromdatabase(sql, values, cols)
            
            employee_name_str = df['employee_name'].unique()[0]
            role_name_str = df['role_name'].unique()[0]
            employee_id_str = df['employee_id'].unique()[0]
            division_str = df['division'].unique()[0]

            if df.shape: # check if query returned anything
                fig = go.Figure()

                #expected skill level
                fig.add_trace(go.Scatterpolar(
                    r=df['expected_rating'].tolist(),
                    theta=df['skill_name'].tolist(),
                    fill='toself',
                    name='Ideal Rating'
                ))

                #results 
                fig.add_trace(go.Scatterpolar(
                    r=df['rating'].tolist(),
                    theta=df['skill_name'].tolist(),
                    fill='toself',
                    name='Self Rating'
                ))

                fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                    )),
                showlegend=False,
                title = f"Competency Mapping Results for {employee_name_str} (Employee#: {employee_id_str}) <br> for the role of {role_name_str} <br> under {division_str} <br><br>"
                )
                return [fig]
            else:
                return PreventUpdate
        else:
            return PreventUpdate 
    else:
        return PreventUpdate


