import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback,clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash
from widget import don_check,genre_check,eligible,matrimoine
import json
import pathlib

PATH = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = PATH.joinpath("data").resolve()



def get_pandas_data(csv_filename: str) -> pd.DataFrame:
    '''
    Load data from /data directory as a pandas DataFrame
    using relative paths.
    '''
    csv_path = DATA_PATH.joinpath(csv_filename)

    # Vérifier si le fichier existe avant de le charger
    if not csv_path.exists():
        raise FileNotFoundError(f"Le fichier {csv_filename} est introuvable dans {DATA_PATH}")

    return pd.read_csv(csv_path)

# Charger les données
df = get_pandas_data("donnees_nettoyees_candidats (1).csv")

dash.register_page(__name__, path="/candidat")



# df = pd.read_csv("donnees_nettoyees_candidats (1).csv") 

df['ÉLIGIBILITÉ AU DON.'] = df['ÉLIGIBILITÉ AU DON.'].replace({
    "Eligible": "Éligible",
    "Temporairement Non-eligible": "temporaire",
    "Définitivement non-eligible": "Non Éligible"
   })


layout=html.Div([
        dbc.Row([
            dbc.Col(html.Div([
            dbc.Row(
            dbc.Col(
            dbc.Stack(
            [
                html.Div(eligible),
                html.Div(matrimoine),
                html.Div(don_check),
                html.Div(genre_check)
                
            ],
            gap=2,
           
            ),
            
            className='  ',
            width={"size": 10, "offset": 1},
            
            )
        )
            ]),style={'height': 'calc(100vh - 80px)','width': '16.67%', 'top': '80px','position':'fixed','display': 'flex',
            'flexDirection': 'column',
            
            'justifyContent': 'center','backgroundColor':'#A5D8DD'},id="sidebar",width=2),
            dbc.Col(
            html.Div([
            dbc.Row([
            dbc.Col([
                dbc.Row(),
                dbc.Row([
                    dbc.Col([
                        html.Div(dcc.Graph(id='pie_eligible',style={'height': '100%', 'width': '100%'},className='mx-auto'),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'}),
                        html.Div(dcc.Graph(id='pie_genre',style={'height': '100%', 'width': '100%'}),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'},className=' mt-2 '),
                    ],width=6),
                    dbc.Col(html.Div(dcc.Graph(id='map',style={'height': '100%', 'width': '100%'}),className='',style={'height':'100%','width': '100%', 'overflow': 'hidden'}),width=6),
                ],className='mt-2 '),
                dbc.Row([
                    dbc.Col(html.Div(dcc.Graph(id='bar_matri',style={'height': '100%', 'width': '100%'}),className='',style={'height':'400px','width': '100%', 'overflow': 'hidden'}),width=6),
                    dbc.Col(html.Div(dcc.Graph(id='bar_edu',style={'height': '100%', 'width': '100%'}),className='',style={'height':'100%','width': '100%', 'overflow': 'hidden'}),width=6),
                ],className='mt-2 '),
                dbc.Row(
                    [dbc.Col(html.Div(dcc.Graph(id='bar_tranche',style={'height': '100%', 'width': '100%'}),style={'height':'400px','width': '100%', 'overflow': 'hidden'}),width=6),
                    dbc.Col(html.Div(dcc.Graph(id='bar_elig',style={'height': '100%', 'width': '100%'}),style={'height':'100%','width': '100%', 'overflow': 'hidden'}),width=6)  
                    ],
                    
                    className='mt-2 '),

            ]
            
            )
            ],className='mt-2'),
            ],className='me-1 ms-2 mb-3 ')   
            ,style={'margin-left': '16.67%','margin-top': '90px', 'padding-top': '20px','z-index': 1,  # Valeur inférieure à celle de la navbar (1000)
            'position': 'relative' },id="main-content",className='',width=10),
             
        ], className='')
    ])


