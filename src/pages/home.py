import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/',
                   title='Group Hungary',
                   name='Group Hungary',
                   order=0)


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H2(children="Welcome!")
        ])
    ]),
    dbc.Row([
        html.Div([
            html.P(children="In this APP, you can explore the noise and metro data collected in Leuven, Belgium, 2022.",className="mb-0"),
            html.P(children="Please click on the left column (content), to play with data visualization.",className="mb-0"),
            html.Br(),
            html.H2(children="General Information"),
            html.Div("Click on the each section below for detailed description"),
            html.Div([
                dbc.Accordion([
                    dbc.AccordionItem(
                        [
                            html.P("To check the noise level on map"),
                        ],
                        title="Noise Map",
                    ),
                    dbc.AccordionItem([
                        html.P("To see how these 2 factors change through time"),
                    ],
                        title="Noise level and Humidity"),
                    dbc.AccordionItem([
                        html.P("Checking the composition and distribution of the noise types through time, broken down by the humidity level"),
                    ],
                        title="Noise Types"),
                    dbc.AccordionItem([
                        html.P("Summarization of the factors to predict noise types with random forest"),
                    ],
                        title="Modeling"),

                ],
                always_open=True,
                flush=True,style={"width":"11cm"})
            ]),
    ]),

]),
    html.Br(),
    html.Br(),
    dbc.Row([
        html.Div([
            html.H2(children="Team Member:"),
            html.Div('Fan Yu (r0862624)'),
            html.Div('Jierong Wen (r0912240)'),
            html.Div('Lie Hong (s0203439)'),
            html.Div('Linhan Liu (r0865726)'),
            html.Div('Naichuan Zhang (r0913147)'),
            html.Div('Zarina Serikbulatova (r0822631)')
        ])
    ])
])