import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

pagename='Modelling'

dash.register_page(__name__,
                   path=f'/{pagename}',
                   title=pagename,
                   name=pagename)


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H3(children="Random Forest Modelling")
        ])
    ])
])