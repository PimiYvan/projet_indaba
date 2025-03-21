import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output,dcc,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash


dash.register_page(__name__, path="/candidat")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


layout = html.Section([
    html.Div('bonjour')
])







if __name__ == "__main__":
    app.run_server()