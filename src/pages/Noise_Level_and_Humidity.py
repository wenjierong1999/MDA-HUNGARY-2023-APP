import dash
from dash import html, dcc, callback
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__,
                   path='/Noise-Level-and-Humidity',
                   title='Noise level and Humidity',
                   name='Noise level and Humidity'
                   )
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
    return fig


########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################


layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.H3('The relationship of noise peak values and humidity'))
        ]),
        dbc.Row([
            dbc.Col([
                html.Div('Select the location to display:'),
                html.Div(
                    dcc.Dropdown(selectlist, selectlist[0], id='selectbox-linep-loc',style={'width': '8cm'})
                )
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('On this page, we present the relationship between C-weighted noise peak values and humidity in 2022. C-weighting is used for high-level measurements and peak sound pressure levels. Unlike the A-weighted curve, which is widely used for general-purpose noise measurements, the C-weighting better correlates with the human response to high noise levels, including noise-induced hearing loss and other health issues.'),
                    html.P('At the top, you can use the menu bar to select the location you want to inspect.')
                ],style={'width': '20cm'})
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dcc.Graph(id="linep-humdity-lcpeak-loc")
                )

            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Sound records from locations Calvariekapel, Naamsestraat 62, and Parkstraat 2 are relatively complete. For other locations, the sound values were imputed using the MICE algorithm (Multivariate Imputation by Chained Equations). However, the imputed parts do not exhibit the same cyclic patterns as shown in Calvariekapel, Naamsestraat 62, and Parkstraat 2. Imputed values are closer to the mean noise level in each monitoring site.')
                ],style={'width': '20cm'})
            ])
        ])
    ]
)
