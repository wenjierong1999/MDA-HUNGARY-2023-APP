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
                        html.P("Summarization of the factors to predict noise types with random forest"),
                    ],
                    title="Modeling"),
                    dbc.AccordionItem([
                        html.P("To see how these 2 factors change through time"),
                    ],
                        title="Noise level and Humidity"),
                    dbc.AccordionItem([
                        html.P("Checking the composition and distribution of the noise types through time, broken down by the humidity level"),
                    ],
                        title="Noise Types and Humidity"),
                ],
                always_open=True,
                flush=True,style={"width":"11cm"})
            ]),
    ]),
])
])