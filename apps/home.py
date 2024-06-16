# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app


# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Discover Skills. Drive Success.'),
        html.Hr(),
        html.Div(
            [
                html.Span(
                    "Welcome! Discover your data science talents' competencies and help drive team success. This is the official portal for the results of the data science skills competencies of the Data Science Group of Company XYZ.",
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Explore your employee database, skill sets, and roles under different departments via their respective tabs.",
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Already took the assessment? Click below for the results.",
                ),
                html.Div(
                    dbc.Button("Results here!", color="info", size="lg",
                               #className="my-2",
                               className="d-grid gap-2",
                               href='/results')
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Contact your HR Business Partner to schedule an assessment.",
                    style={'font-style':'italic'}
                ),
            ]
        )
    ]
)