import dash
from dash import html, dcc, callback, ctx
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

dash.register_page(__name__)
########################################################################################################################
#                                            DATA LOADING                                                 #
########################################################################################################################
noise_map = pd.read_csv("s3://mda-maindata/assets/Percentile_Noise_Weather_for_APP_Un-scaled_NAdropped.csv")

########################################################################################################################
#                                         DEFINING CALLBACK FUNCTIONS                                             #
########################################################################################################################
@callback(
    Output(component_id='output-date-picker', component_property='children'),
    Output(component_id='container-button-timestamp', component_property='children'),
    Output(component_id="noise-density-map", component_property="figure"),
    Input(component_id="noise-date-picker", component_property="date"),
    Input(component_id="hour-slider",component_property="value"),
    Input(component_id='btn-nclicks-1', component_property='n_clicks'),
    Input(component_id='btn-nclicks-2', component_property='n_clicks'),
    Input(component_id='btn-nclicks-3', component_property='n_clicks')
)
def update_density_map(date_value,hour,btn1,btn2,btn3):
    date_object = date.fromisoformat(date_value)
    month = date_object.month
    day = date_object.day
    noise_map_date = noise_map[(noise_map["month"] == month)
                               & (noise_map["day"] == day)
                               & (noise_map["hour"] == hour)]
    string_prefix = 'You have selected: '
    date_string = date_object.strftime('%b %d, %A')
    
    msg = "You have selected noise map of laf 10%"
    fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf10_per_hour",
                            color="laf10_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[40, 80],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"location": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )
    if "btn-nclicks-1" == ctx.triggered_id:
        msg = "You have selected noise map of laf 10%"
        fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf10_per_hour",
                            color="laf10_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[40, 80],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"location": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )

    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "You have selected noise map of laf 90%"
        fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf90_per_hour",
                            color="laf90_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[30, 60],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"location": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )

    elif "btn-nclicks-3" == ctx.triggered_id:
        msg = "You have selected noise map of laf 905%"
        fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf95_per_hour",
                            color="laf95_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[30, 60],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"location": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )
        
    return string_prefix+date_string, html.Div(msg), fig

########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################

layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H2(children="Noise level in Leuven 2022, by hour")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.DatePickerSingle(
                    id="noise-date-picker",
                    calendar_orientation="horizontal",
                    day_size=39,
                    number_of_months_shown=1,
                    min_date_allowed=date(2022, 2, 17),
                    max_date_allowed=date(2022, 12, 31),
                    initial_visible_month=date(2022, 2, 17),
                    date=date(2022, 2, 17),
                    month_format="MMMM, YYYY"
                ),html.Div(id="output-date-picker")])
        ]),
        dbc.Col([
                html.Button('laf10', id='btn-nclicks-1', n_clicks=0),
                html.Button('laf90', id='btn-nclicks-2', n_clicks=0),
                html.Button('laf95', id='btn-nclicks-3', n_clicks=0),
                html.Div(id='container-button-timestamp')
        ])

    ]),

    dbc.Row([
        dbc.Col([
                html.Div([
                    dcc.Slider(
                        id="hour-slider",
                        min=0,max=23,
                        step=None,
                        value=0,
                        marks={str(hour): str(hour) + ":00" for hour in range(0, 24)},
                        updatemode="drag"
                    )
            ])
        ])
    ]),
    dbc.Row([
        dcc.Graph(id="noise-density-map")
    ]),
    dbc.Row([
        html.Div([
            html.H3("Description"),
            html.Div([
                html.P("On this page, we present the scatter plot of A-weighted sound level by hour, measured with a fast time-constant (LAF). A-weighting is the 'common' name for frequency-weighted sound levels, measured over the 'A' frequency range, and LAFn means A-weighted, sound level exceeded for n% of the measurement period, calculated by statistical analysis, where n is between 0.01% and 99.99%.",style={'width': '20cm'}),
                html.P("The reason why we choose to present LAF10, LAF90, LAF95 is: the L10 has been found over the years to be a useful descriptor of road traffic noise as it correlates quite well with the disturbance people feel when close to busy roads as well as more rural situations, while LAF90 or LAF 95 have been widely adopted to quantify background noise levels.",style={'width': '20cm'})
                ])
            ])
    ]),
    dbc.Row([
        html.Div([
            html.H3("How to use:"),
            html.Div([
                html.P("At the top, you can use the calendar to choose a specific date, and move the slider to select different hours, then the plot will show you the noise level at different locations. You can also click different buttons to output different noise levels (LAF10, LAF90, LAF95).",style={'width': '20cm'}),
                html.P("When you hover over a specific scatter point, there will be a hoverbox showing the noise decibel and location corresponding to the scatter point. ",style={'width': '20cm'})
                ])
            ])
    ]) 
])
