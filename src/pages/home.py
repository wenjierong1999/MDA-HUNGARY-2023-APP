import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/',
                   title='Group Hungary',
                   name='Group Hungary')


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.P(children="In this APP, you can explore the noise and metro data collected in Leuven, Belgium, 2022.",className="mb-0"),
            html.P(children="Please click on the left column (content), to play with data visualization.",className="mb-0"),
            html.Br(),
            html.Ul([
                html.Li(children="Density Map: to check the noise level on map",className="list-group-item list-group-item-action list-group-item-info"),
                html.Li(children="Noise level and Humidity: to see how these 2 factors change through time",className="list-group-item list-group-item-action list-group-item-info"),
                html.Li(children="Noise Types: to see the composition and distribution of the noise types through time",className="list-group-item list-group-item-action list-group-item-info"),
                html.Li(children="Noise Types and Humidity: to see the noise types broken down by the humidity level",className="list-group-item list-group-item-action list-group-item-info"),
                html.Li(children="Random Forest Model: summarization of the factors affect noise types",className="list-group-item list-group-item-action list-group-item-info"),
            ],className="list-group",style={"width":"18cm"})
        ])
    ]),
])