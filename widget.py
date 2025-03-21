import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash

data_donneur=pd.read_csv('donnees_nettoyees_donneurs.csv')


dropdown_groupe=  html.Div([
        "Groupe Sanguin",
        dcc.Dropdown(data_donneur['Groupe_Sanguin'].unique(), id='dropdown_groupe')
    ])


sexe_check=html.Div([
        "Sexe",
        dcc.Checklist(data_donneur['Sexe'].unique(),id='sexe_check')
])

type_check=html.Div([
    "Type_donation",
    dcc.Checklist(data_donneur['Type_donation'].unique(),id='type_check')
])



    

