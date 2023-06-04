import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

pagename='Modeling'

dash.register_page(__name__,
                   path=f'/{pagename}',
                   title=pagename,
                   name=pagename,
                   order=4)


layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H2(children="Using Random Forest to Predict Noise Type"),
            html.P("This page provides information about the initial model we applied and the importance of its features, along with a brief project conclusion."),
            html.P("We aim to explain the intriguing findings we discovered through modeling, hoping to provide you with interesting insights into how temporal, spatial, and meteorological factors contribute to predicting noise types.")
        ], style={"width":"20cm"})
    ]),
    html.Br(),
    dbc.Row([
            html.Img(src="https://github.com/wenjierong1999/MDA-HUNGARY-2023-APP/blob/master/assets/relative_importance_of_features.png?raw=true")
        ], style={"width":"15cm"}),       
    html.Br(),
    dbc.Row([
        html.P("From the bar chart, we observe that the most significant features for predicting noise types (with relative importance exceeding 60%) are Hour, Location, Month, Solar Radiation, Radiation per Hour, Wind Direction, Dew Point, Wind Speed, and Relative Humidity. Notably, Hour, Location, and Month exhibit values above 80%."),
        html.P("This suggests that the 'time' of day and specific location provide valuable clues for predicting noise types compared to other features."),
        html.P("Additionally, we notice that temperature obtained from different quality control levels (Temperature QCL0, QCL1, QCL2, and QCL3) also play important roles in noise type prediction. However, these temperature values may not contribute more information to the classifier than Dew Point, which encompasses relative humidity, air pressure, and temperature. Therefore, Dew Point becomes a better predictor than other calibrated temperature values."),
        html.P("Moreover, solar radiation also has a significant impact on the prediction. The amount of radiation not only reflects people's inclination for outdoor activities but also indirectly represents their circadian cycles. When combined with location information, these meteorological data enhance the predictive power of the model.")
    ], style={"width":"20cm"}),
    html.Br(),
    dbc.Row([
        html.Img(src="https://github.com/wenjierong1999/MDA-HUNGARY-2023-APP/blob/master/assets/accuracy.png?raw=true")
    ], style={"width":"15cm"}),
    html.Br(),
    dbc.Row([
       html.P("Furthermore, we present different test accuracies using data collected over various time periods. While we cannot provide an exact explanation for the discrepancies in accuracy, it is intriguing to compare these results with the bar chart on the Noise Type page, which illustrates monthly noise types throughout the entire year. Particularly, the occurrence of noise types shows significant variation within the first three months. However, after this initial period, the occurrence of noise types becomes more abundant. The evenly distributed nature of our 'labels' across the entire year and city posed challenges in categorizing noise events."),
       html.P("In our exploration, we have found potential correlations between urban noise and weather parameters. To further investigate cyclic and clustered data like noise and meteorological-hydrological profiles, advanced models should be employed. Additionally, we have observed that some shops in Leuven ceased operations during/after the pandemic period. Incorporating historical text data from the geo-dataset or the internet would be advantageous in exploring societal changes and gaining more supporting information to unravel urban noise levels. For now, we would like to express our gratitude for visiting our web application and exploring the current results we have presented.")
    ], style={"width":"20cm"})
])
