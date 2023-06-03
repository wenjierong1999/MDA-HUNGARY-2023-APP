import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                title='MDA Project',
                use_pages=True,
                external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

########################################################################################################################
#                                            DATA LOADING                                                 #
########################################################################################################################


########################################################################################################################
#                                         DEFINING CALLBACK FUNCTIONS                                             #
########################################################################################################################


########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################

sidebar = html.Div(
    [
        html.H2("Content", className="display-7"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
        ),
    ],
)

app.layout = dbc.Container(
    [dbc.Row([
        dbc.Col([html.H1("Modern Data Analytics [G0Z39a]",
                        style={'textAlign': 'center'}),
                 html.H2("APP Demo 2022-2023",style={'textAlign': 'center'})
                 ])
    ]),
        html.Hr(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        sidebar
                    ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2
                ),
                dbc.Col(
                    [
                        dash.page_container
                    ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10
                )
            ]
        )
    ]
    , fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)
