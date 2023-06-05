import dash
from dash import html, dcc, callback,ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


pagetitle = "Acknowledgements"

dash.register_page(__name__,
                       path=f"/{pagetitle}",
                       title=pagetitle,
                       name=pagetitle,
                       order=6)


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H3(children="Acknowledgements"),
            html.Br(),
            html.P(children="We extend our heartfelt gratitude and appreciation to the esteemed lecturers of the course, Modern Data Analytics. Their dedication and efforts in organising this exceptional and insightful course have left an indelible mark on our learning journey."),
            html.Br(),
            html.P(children="Firstly, we express our sincere thanks to Professor Dr. Jan De Spiegeleer. Through his profound knowledge and expertise, he provided us with a comprehensive understanding of state-of-the-art data processing techniques, collaborative teamwork, and leveraging cloud technology to drive our projects forward."),
            html.Br(),
            html.P(children="We are immensely grateful to Gregory van Kruijsdijk for his illuminating sessions on big data analysis and modelling. His teachings have equipped us with a strong foundation to collectively manipulate and harness the power of data."),
            html.Br(),
            html.P(children="Our appreciation also goes to Ruben Kerkhofs, who skillfully introduced us to web application development and visualization. His insightful approach encapsulated the essential components covered in this course, leaving us with a holistic understanding of the subject matter.")
        ],style={"width":"20cm"})
    ])
])