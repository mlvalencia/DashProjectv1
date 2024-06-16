##########################################
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


def get_divisions():   #get those w results only
    sql_div = """

    SELECT distinct a.division
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
    cols=['division']
    df = db.querydatafromdatabase(sql_div,values,cols)
    return df['division'].tolist()

list_divisions = (get_divisions())


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_layout(
        title = dict(
            text=f"Please select division name.",
                x=0.5,
                y=0.5,
                xanchor='center',
                yanchor='middle'
        ),
        title_font_family="sans-serif"
        )
    return fig



# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Results by Division'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Competency Mapping by Division')
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
                                                dbc.Label("Division Name", width=2),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[{'label':division, 'value':division} for division in list_divisions],
                                                            id='divisionname_dropdown',
                                                            placeholder='Search Division Name'
                                                        ),
                                                        width=5
                                                    )
                                            ],
                                            className='mb-3' # add 1em bottom margin
                                        ),
                                    #  html.Hr(), 
                                      dbc.Row(
                                            [
                                                dbc.Label("Skill Type", width=2),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=['Enabling','Functional'],
                                                            id='skilltype_filter_div',
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
                                     [dcc.Graph(id='spiderplot_results_div',figure=blank_fig()),
                                     dbc.Button(color="warning",
                                                size="lg",
                                                className="d-grid gap-2 col-6 mx-auto my-2",
                                                id='reset_all',children = 'Clear all',
                                                style={"horizontalAlign": "left"})]
                                )
                            ]
                        )
                    ]
                ),
        
            ]
        )



@app.callback(
    [
        Output('spiderplot_results_div', 'figure'),
        Output('divisionname_dropdown','value'),
        Output('skilltype_filter_div','value'),
    ],
    [
        Input('url', 'pathname'),
        Input('divisionname_dropdown','value'),
        Input('skilltype_filter_div','value'),
        Input('reset_all','n_clicks')
    ]
)
def spiderplotresults_here(pathname,div_name,skilltype,n_clicks):
    print(pathname)
    #if emp_name is not None:
    # if ctx.triggered_id == 'reset':
    #     fig1 = go.Figure(data=[go.Scatter(x=[], y=[])])
    #     return fig1
   
    if ctx.triggered_id == 'reset_all':
        fig = go.Figure()

        fig = blank_fig()
        return [fig,None,None]

    elif (div_name is not None):
        if pathname == '/results_division':

            sql = """ 
            SELECT distinct a.division, c.skill_name, c.skill_type, avg(cast(b.expected_rating as float)) as expected_rating_avg, avg(cast(e.rating as float)) as rating_avg
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
            and d.end_role_date is NULL
			
            """
            values = [] # blank since I do not have placeholders in my SQL
            cols = ['division','skill_name','skill_type','expected_rating_avg','rating_avg'] #table column names
            


            if div_name is not None and skilltype is None:
                sql += "AND a.division ILIKE %s GROUP BY a.division, c.skill_name, c.skill_type"
                values += [f"%{div_name}% "]
            elif div_name is not None and skilltype is not None:
                sql += """AND a.division ILIKE %s AND skill_type ILIKE %s 
                     GROUP BY a.division, c.skill_name, c.skill_type"""
                values += [f"%{div_name}%", f"%{skilltype}%"]
                
            # 

            df = db.querydatafromdatabase(sql, values, cols)
            
            division_str = df['division'].unique()[0]

            if df.shape: # check if query returned anything
                fig = go.Figure()

                #expected skill level
                fig.add_trace(go.Scatterpolar(
                    r=df['expected_rating_avg'].tolist(),
                    theta=df['skill_name'].tolist(),
                    fill='toself',
                    name='Ideal Rating'
                ))

                #results 
                fig.add_trace(go.Scatterpolar(
                    r=df['rating_avg'].tolist(),
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
                title = dict(
                    text=f"Competency Mapping Results for {division_str}",
                      x=0.5,
                      y=0.95,
                      xanchor='center',
                      yanchor='top',
                ),
                title_font_family="sans-serif"
                )
                fig.update_layout(margin=dict(t=150))

                return [fig,div_name,skilltype]
            else:
                return PreventUpdate
        else:
            return PreventUpdate 
    else:
        return PreventUpdate


