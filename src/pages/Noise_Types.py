import dash
from dash import html, dcc, callback, ctx
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

dash.register_page(__name__,
                   path="/Noise-Types",
                   title="Noise Types",
                   name="Noise Types")
########################################################################################################################
#                                            DATA LOADING                                                 #
########################################################################################################################
df_noise_weather = pd.read_csv("s3://mda-maindata/assets/Percentile_Noise_Weather_for_APP_Un-scaled.csv")
df_noiseTypes = pd.read_csv("s3://mda-maindata/assets/Export_41_and_weather.csv")

## <2-1> Create the dataframe to plot bar chart.
# Keep specific columns
columns_to_keep_bar = ['month', 'day', 'hour', 'weekday', 'noise_event_laeq_primary_detected_class', 'Humidity>80']

# Make a new dataframe for the function to run. Select full hour
df_noiseTypes_bar = df_noiseTypes[columns_to_keep_bar].copy()
df_noiseTypes_bar['weekday']=df_noiseTypes_bar['weekday'].astype('int')
df_noiseTypes_bar['weekday_name'] = df_noiseTypes_bar['weekday'].apply(lambda x: calendar.day_name[x] if (x>=0) & (x<7) else None)

## Create Dataframes for <2-2-1>
# Group the data by month and primary type to get the count
grouped_noise_month = df_noiseTypes_bar.groupby(['month', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count')

## Create Dataframes for <2-2-2>
# Group the data by weekday and primary type to get the count
grouped_noise_weekday = df_noiseTypes_bar.groupby(['weekday', 'weekday_name', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count')

## Create Dataframes for <2-2-3>
# Group the data by hour and primary type to get the count
grouped_noise_hour = df_noiseTypes_bar.groupby(['hour', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count')

## Create Common Dataframes for <2-2-4>, <2-2-5> & <2-2-6>
# Filter the data based on Humidity>80 column values
df_humidity_gt_80 = df_noiseTypes_bar[df_noiseTypes_bar['Humidity>80'] == 1]
df_humidity_lt_80 = df_noiseTypes_bar[df_noiseTypes_bar['Humidity>80'] == 0]

## Create specific Dataframes for <2-2-4>
# Group the data by month and noise type for Humidity>80 = 1
df_humidity_gt_80_mon = df_humidity_gt_80.groupby(['month', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_gt_80_mon')
# Group the data by month and noise type for Humidity>80 = 0
df_humidity_lt_80_mon = df_humidity_lt_80.groupby(['month', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_lt_80_mon')

## Create specific Dataframes for <2-2-5>
# Group the data by weekday and noise type for Humidity>80 = 1
df_humidity_gt_80_week = df_humidity_gt_80.groupby(['weekday','weekday_name', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_gt_80_week')
# Group the data by weekday and noise type for Humidity>80 = 0
df_humidity_lt_80_week = df_humidity_lt_80.groupby(['weekday', 'weekday_name', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_lt_80_week')

## Create specific Dataframes for <2-2-6>
# Group the data by hour and noise type for Humidity>80 = 1
df_humidity_gt_80_hour = df_humidity_gt_80.groupby(['hour', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_gt_80_hour')
# Group the data by month and noise type for Humidity>80 = 0
df_humidity_lt_80_hour = df_humidity_lt_80.groupby(['hour', 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count_lt_80_hour')# Create a dictionary to assign colors to each primary type

# Create a dictionary to assign colors to each primary type
color_mapping = {
    'Transport road - Passenger car': 'rgb(105, 105, 105)',
    'Unsupported': 'rgb(220, 220, 220)',
    'Human voice - Shouting': 'rgb(255, 127, 14)',
    'Transport road - Siren': 'rgb(214, 39, 40)',
    'Human voice - Singing': 'rgb(227, 119, 194)',
    'Music non-amplified': 'rgb(140, 86, 75)',
    'Nature elements - Wind': 'rgb(188, 189, 34)',
    }


########################################################################################################################
#                                         DEFINING CALLBACK FUNCTIONS                                             #
########################################################################################################################


@callback(
    Output(component_id="noise-event-by-month", component_property="figure"),
    Input(component_id='btn-nclicks-1', component_property='n_clicks'),
    Input(component_id='btn-nclicks-2', component_property='n_clicks'),
    Input(component_id='btn-nclicks-3', component_property='n_clicks')
)
def update_bar_chart_month(btn1,btn2,btn3):

    # noise event by month
    fig_mon = go.Figure()

    for noise_type, color in color_mapping.items():
        data_subset = grouped_noise_month[grouped_noise_month['noise_event_laeq_primary_detected_class'] == noise_type]
        fig_mon.add_trace(go.Bar(
            x=data_subset['month'],
            y=data_subset['count'],
            name=noise_type,
            marker_color=color
        ))

    # Update the layout of the chart
    fig_mon.update_layout(
        title='Noise Type Count by Month, Leuven (2022)',
        xaxis_title='Month',
        yaxis_title='Types Count',
        barmode='stack'  # Set the bar mode to stack for different color segments
    )

    if "btn-nclicks-1" == ctx.triggered_id:
        # noise event by month
        fig_mon = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = grouped_noise_month[grouped_noise_month['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_mon.add_trace(go.Bar(
                x=data_subset['month'],
                y=data_subset['count'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the chart
        fig_mon.update_layout(
            title='Noise Type Count by Month, Leuven (2022)',
            xaxis_title='Month',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

    elif "btn-nclicks-2" == ctx.triggered_id:
        # Create the first bar chart for Humidity>80 = 1
        fig_gt_80_mon = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_gt_80_mon[df_humidity_gt_80_mon['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_gt_80_mon.add_trace(go.Bar(
                x=data_subset['month'],
                y=data_subset['count_gt_80_mon'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the first chart
        fig_gt_80_mon.update_layout(
            title='Noise Type Count by Month (Humidity>80%)',
            xaxis_title='Month',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_mon = fig_gt_80_mon

    elif "btn-nclicks-3" == ctx.triggered_id:
        # Create the second bar chart for Humidity>80 = 0
        fig_lt_80_mon = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_lt_80_mon[df_humidity_lt_80_mon['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_lt_80_mon.add_trace(go.Bar(
                x=data_subset['month'],
                y=data_subset['count_lt_80_mon'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the second chart
        fig_lt_80_mon.update_layout(
            title='Noise Type Count by Month (Humidity<80%)',
            xaxis_title='Month',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_mon = fig_lt_80_mon

    return fig_mon


@callback(
    Output(component_id="noise-event-by-week", component_property="figure"),
    Input(component_id='btn-nclicks-4', component_property='n_clicks'),
    Input(component_id='btn-nclicks-5', component_property='n_clicks'),
    Input(component_id='btn-nclicks-6', component_property='n_clicks')
)
def update_bar_chart_week(btn4,btn5,btn6):
    # noise event by week
    # Create a bar chart with different color segments for each primary type
    fig_week = go.Figure()

    for noise_type, color in color_mapping.items():
        data_subset = grouped_noise_weekday[grouped_noise_weekday['noise_event_laeq_primary_detected_class'] == noise_type]
        fig_week.add_trace(go.Bar(
            x=data_subset['weekday_name'],
            y=data_subset['count'],
            name=noise_type,
            marker_color=color
        ))

    # Update the layout of the chart
    fig_week.update_layout(
        title='Noise Type Count by Weekday, Leuven (2022)',
        xaxis_title='Weekdays',
        yaxis_title='Types Count',
        barmode='stack'  # Set the bar mode to stack for different color segments
    )


    if "btn-nclicks-4" == ctx.triggered_id:
        fig_week = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = grouped_noise_weekday[grouped_noise_weekday['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_week.add_trace(go.Bar(
                x=data_subset['weekday_name'],
                y=data_subset['count'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the chart
        fig_week.update_layout(
            title='Noise Type Count by Weekday, Leuven (2022)',
            xaxis_title='Weekdays',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        # Update the layout of the chart
        fig_week.update_layout(
            title='Noise Type Count by Weekday, Leuven (2022)',
            xaxis_title='Weekdays',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

    elif "btn-nclicks-5" == ctx.triggered_id:
        # Create the first bar chart for Humidity>80 = 1
        fig_gt_80_week = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_gt_80_week[df_humidity_gt_80_week['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_gt_80_week.add_trace(go.Bar(
                x=data_subset['weekday_name'],
                y=data_subset['count_gt_80_week'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the first chart
        fig_gt_80_week.update_layout(
            title='Noise Type Count by Weekday (Humidity>80%)',
            xaxis_title='Weekdays',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_week = fig_gt_80_week

    elif "btn-nclicks-6" == ctx.triggered_id:
        # Create the second bar chart for Humidity>80 = 0
        fig_lt_80_week = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_lt_80_week[df_humidity_lt_80_week['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_lt_80_week.add_trace(go.Bar(
                x=data_subset['weekday_name'],
                y=data_subset['count_lt_80_week'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the second chart
        fig_lt_80_week.update_layout(
            title='Noise Type Count by Weekday (Humidity<80%)',
            xaxis_title='Weekdays',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_week = fig_lt_80_week

    return fig_week

@callback(
    Output(component_id="noise-event-by-hour", component_property="figure"),
    Input(component_id='btn-nclicks-7', component_property='n_clicks'),
    Input(component_id='btn-nclicks-8', component_property='n_clicks'),
    Input(component_id='btn-nclicks-9', component_property='n_clicks')
)
def update_bar_chart_month(btn7,btn8,btn9):

    # noise event by hour
    # Create a bar chart with different color segments for each primary type
    fig_hour = go.Figure()

    for noise_type, color in color_mapping.items():
        data_subset = grouped_noise_hour[grouped_noise_hour['noise_event_laeq_primary_detected_class'] == noise_type]
        fig_hour.add_trace(go.Bar(
            x=data_subset['hour'],
            y=data_subset['count'],
            name=noise_type,
            marker_color=color
        ))

    # Update the layout of the chart
    fig_hour.update_layout(
        title='Noise Type Count by Hour, Leuven (2022)',
        xaxis_title='Hour',
        yaxis_title='Types Count',
        barmode='stack'  # Set the bar mode to stack for different color segments
    )

    if "btn-nclicks-7" == ctx.triggered_id:
        # Create a bar chart with different color segments for each primary type
        fig_hour = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = grouped_noise_hour[grouped_noise_hour['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_hour.add_trace(go.Bar(
                x=data_subset['hour'],
                y=data_subset['count'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the chart
        fig_hour.update_layout(
            title='Noise Type Count by Hour, Leuven (2022)',
            xaxis_title='Hour',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )
        
    if "btn-nclicks-8" == ctx.triggered_id:
        # Create the first bar chart for Humidity>80 = 1
        fig_gt_80_hour = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_gt_80_hour[df_humidity_gt_80_hour['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_gt_80_hour.add_trace(go.Bar(
                x=data_subset['hour'],
                y=data_subset['count_gt_80_hour'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the first chart
        fig_gt_80_hour.update_layout(
            title='Noise Type Count by Hour (Humidity>80%)',
            xaxis_title='Hour',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_hour = fig_gt_80_hour

    if "btn-nclicks-9" == ctx.triggered_id:
        # Create the second bar chart for Humidity>80 = 0
        fig_lt_80_hour = go.Figure()

        for noise_type, color in color_mapping.items():
            data_subset = df_humidity_lt_80_hour[df_humidity_lt_80_hour['noise_event_laeq_primary_detected_class'] == noise_type]
            fig_lt_80_hour.add_trace(go.Bar(
                x=data_subset['hour'],
                y=data_subset['count_lt_80_hour'],
                name=noise_type,
                marker_color=color
            ))

        # Update the layout of the second chart
        fig_lt_80_hour.update_layout(
            title='Noise Type Count by Hour (Humidity<80%)',
            xaxis_title='Hour',
            yaxis_title='Types Count',
            barmode='stack'  # Set the bar mode to stack for different color segments
        )

        fig_hour = fig_lt_80_hour
    
    return fig_hour

########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################

layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H3(children="The types of noise broken down by month, weekday, and hour")
        ])
    ]),
    dbc.Row([
        html.Div([
            html.P(children="On this page, we display the noise types that exceed 70 decibels in an interactive manner. By clicking on the seven colorful squares in the legend, you can select the types of noise to be shown. This allows you to get a glimpse of the noise sources that occurred over time in Leuven in 2002.")
        ],style={"width":"20cm"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Button('Entire', id='btn-nclicks-1', n_clicks=0,className='btn btn-secondary',style={"aria-label":"Basic example"}),
                html.Button('Humidity > 80%', id='btn-nclicks-2', n_clicks=0,className='btn btn-secondary'),
                html.Button('Humidity < 80%', id='btn-nclicks-3', n_clicks=0,className='btn btn-secondary')
            ],className="btn-group",style={"aria-label":"Basic example"})
        ])

    ]),

    dbc.Row([
        dcc.Graph(id="noise-event-by-month")
    ]),
   dbc.Row([
        dbc.Col([
            html.Div([
                html.Button('Entire', id='btn-nclicks-4', n_clicks=0, className='btn btn-secondary',
                            style={"aria-label": "Basic example"}),
                html.Button('Humidity > 80%', id='btn-nclicks-5', n_clicks=0, className='btn btn-secondary'),
                html.Button('Humidity < 80%', id='btn-nclicks-6', n_clicks=0, className='btn btn-secondary')
            ], className="btn-group", style={"aria-label": "Basic example"})
        ])

    ]),

    dbc.Row([
        dcc.Graph(id="noise-event-by-week")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Button('Entire', id='btn-nclicks-7', n_clicks=0, className='btn btn-secondary',
                            style={"aria-label": "Basic example"}),
                html.Button('Humidity > 80%', id='btn-nclicks-8', n_clicks=0, className='btn btn-secondary'),
                html.Button('Humidity < 80%', id='btn-nclicks-9', n_clicks=0, className='btn btn-secondary')
            ], className="btn-group", style={"aria-label": "Basic example"})
        ])

    ]),

    dbc.Row([
        dcc.Graph(id="noise-event-by-hour")
    ])
])
