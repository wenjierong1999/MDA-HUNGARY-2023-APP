import dash
from dash import html, dcc, callback
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)
########################################################################################################################
#                                            DATA LOADING                                                 #
########################################################################################################################
df_noise_weather = pd.read_csv('s3://mda-maindata/assets/Percentile_Noise_Weather_for_APP_Un-scaled.csv')
df_noiseTypes = pd.read_csv('s3://mda-maindata/assets/Export_41_and_weather.csv')

# <1-1> Create the dataframe to plot line chart. Selecting only 3 sites with relative full noise records
# Condition 1: Keep specific columns
columns_to_keep_lineGraph = ['description_x', 'timestamp', 'mean_lamax', 'mean_lcpeak', 'LC_HUMIDITY', 'data_number']
# Condition 2: Select specific noise monitoring site

loc_match_dict = {
    'Parkstraat_2': 'data0_02',
    'Naamsestraat_62': 'data0_06',
    'Calvariekapel': 'data0_03'
}

selectlist = ['Parkstraat_2', 'Naamsestraat_62', 'Calvariekapel']


########################################################################################################################
#                                         DEFINING CALLBACK FUNCTIONS                                             #
########################################################################################################################
@callback(
    Output(component_id='selectbox-linep-loc-result', component_property='children'),
    Output(component_id='linep-humdity-lcpeak-loc',component_property='figure'),
    Input(component_id='selectbox-linep-loc', component_property='value')
)
def update_selectbox_linep_loc(loc):
    filtered_df = df_noise_weather[df_noise_weather['data_number'].isin([loc_match_dict[loc]])][columns_to_keep_lineGraph].copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['timestamp'], y=filtered_df['mean_lcpeak'], name='Noise Peak Type C',
                             line=dict(color='red')))
    fig.add_trace(go.Scatter(x=filtered_df['timestamp'], y=filtered_df['LC_HUMIDITY'], name='Humidity', line=dict(color='blue')))

    fig.update_layout(
        title=loc,  # Use the dataframe name as the title
        xaxis_title='Datetime',
        yaxis_title='Values'
    )
    return f'You have selected {loc}', fig


########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################


layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.H2('This is the page for visualization on xx'))
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dcc.Dropdown(selectlist, selectlist[0], id='selectbox-linep-loc')
                ),
            ]),
            dbc.Col([
                html.Div(
                    id='selectbox-linep-loc-result'
                ),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dcc.Graph(id="linep-humdity-lcpeak-loc")
                )

            ])
        ])
    ]
)
