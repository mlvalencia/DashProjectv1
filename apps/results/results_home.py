# # from dash import dcc
# # import plotly.graph_objs as go

# # fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# # dcc.Graph(figure=fig)



# # Usual Dash dependencies
# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc
# import dash
# from dash.exceptions import PreventUpdate
# from dash.dependencies import Input, Output, State
# import pandas as pd

# # Let us import the app object in case we need to define
# # callbacks here
# from app import app
# #for DB needs
# import dbconnect as db

# from dash import dcc
# import plotly.graph_objs as go

# #fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# import plotly.graph_objects as go

# # get categories as list per skill and role via sql based on employee number
# # print employee name, division, role 


# # categories = ['Data Analytics','Data Visualization','Problem Management',
# #               'Business Needs Analysis', 'Computational Modelling']

# def get_employee_results():   
#     sql_emp = """
#     SELECT d.employee_name, a.role_name,  c.skill_name, b.expected_rating,  e.rating
#         FROM roles a
#         JOIN test b 
#             on a.role_id = b.role_id 
#         JOIN skills c 
#             ON b.skill_id = c.skill_id 
#         JOIN employees d 
#             ON a.role_id = d.role_id
#         JOIN results e 
#             ON d.employee_id = e.employee_id
#         WHERE 1=1 
#         and d.employee_id = '14'
#         """
#     values=[]
#     cols=['employee_name','role_name','skill_name','expected_rating','rating']
#     df = db.querydatafromdatabase(sql_emp,values,cols)
#     return df

# df = get_employee_results()
# expected_list = df['expected_rating'].tolist()
# rating_list = df['rating'].tolist()
# skills_list = df['skill_name'].tolist()




# layout = html.Div(
#     [
#         html.H2('Results'), # Page Header
#         html.Hr(),
#         dbc.Row([
                
#                     dbc.Label("Employee Number", width=3),
#                        dbc.Col(
#                             dbc.Input(
#                                 type='text',
#                                 id='employee_number',
#                                 placeholder='Enter Employee ID'
#                             ),
#                             width=5
#                                                 )
#                        ]),
#         dcc.Graph(id='scatterplot-skills',figure=fig),
#         ]
# )





##########################################################################################################
# ########################################################################################################
# #######################################################################################################
# #######################################################################################################
# Usual Dash dependencies
from dash import dcc
from dash import html
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
def get_employee_names():   
    sql_emp = """
    SELECT DISTINCT employee_name FROM employees
        """
    values=[]
    cols=['employee_name']
    df = db.querydatafromdatabase(sql_emp,values,cols)
    return df['employee_name'].tolist()

list_employees = (get_employee_names())

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
                                        dbc.Row(
                                            [
                                                dbc.Label("Employee ID", width=5),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='employeeid_filter',
                                                        placeholder='Enter Employee ID'
                                                    ),
                                                    width=5
                                                )
                                            ],className='mb-3'),
                                    dbc.Row(
                                            [
                                                dbc.Label("Employee Name", width=5),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[{'label':employee, 'value':employee} for employee in list_employees],
                                                            id='employeename_dropdown',
                                                            placeholder='Employee Name'
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
                                     dcc.Graph(id='scatterplot_results',figure={})
                                )
                            ]
                        )
                    ]
                )
            ]
        )



@app.callback(
    [
        Output('scatterplot_results', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('employeeid_filter', 'value'),
        Input('employeename_dropdown','value'),
        Input('skilltype_filter','value')
    ]
)
def scatterplot_results_here(pathname, searchterm,emp_name,skilltype):
    print(pathname)
    if pathname == '/results':

        sql = """ 
        SELECT distinct d.employee_name, a.role_name,  c.skill_name, b.expected_rating, e.rating
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
        cols = ['employee_name','role_name','skill_name','expected_rating','rating'] #table column names
        
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND d.employee_id = %s "
            values += [f"%{searchterm}%"]

        if emp_name:
            sql += "AND d.employee_name = %s"
            values += [f"%{emp_name}%"]
        
        if skilltype:
            sql += "AND skill_type = %s"
            values += [f"%{skilltype}%"]

        df = db.querydatafromdatabase(sql, values, cols)
        
        employee_name_str = df['employee_name'].unique()[0]

        if df.shape: # check if query returned anything
            fig = go.Figure()

            #expected skill level
            fig.add_trace(go.Scatterpolar(
                r=df['expected_rating'].tolist(),
                theta=df['skill_name'].tolist(),
                fill='toself',
                name='Expected Skill Level'
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
            title = f"Competency Mapping Results for {employee_name_str} for the role of "
            )
            return [fig]
        else:
            return print("No records to display")
        
    else: 
      raise PreventUpdate


