import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback,clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash
from widget import dropdown_groupe,type_check,sexe_check


# Créer une instance de l'application Dash sans `use_pages`
dash.register_page(__name__, path="/donneur")



data_donneur=pd.read_csv('donnees_nettoyees_donneurs.csv')








layout = html.Div([
        dbc.Row([
            dbc.Col(html.Div([
            dbc.Row(
            dbc.Col(
            dbc.Stack(
            [
                html.Div(dropdown_groupe),
                html.Div(sexe_check),
                html.Div(type_check),
                
            ],
            gap=4,
           
            ),
            
            className=' mt-4 ',
            width={"size": 10, "offset": 1},
            
            )
        )
            ]),style={'height': 'calc(100vh - 80px)','width': '16.67%', 'top': '80px','position':'fixed','display': 'flex',
            'flexDirection': 'column',
            
            'justifyContent': 'center'},id="sidebar",width=2,className='bg-secondary '),
            dbc.Col(
            html.Div([
            dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Div(dcc.Graph(id='pie_sexe',style={'height': '100%', 'width': '100%'}),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'}),
                        html.Div(dcc.Graph(id='pie_distribution',style={'height': '100%', 'width': '100%'}),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'},className='mt-2'),
                    ],className=''),
                    # dbc.Col(html.Div('cool',style={'height': '100%', 'width': '100%', 'overflow': 'hidden'}),className=' '),
                ],className='g-2')
            ],width=5),
            dbc.Col(html.Div(dcc.Graph(id='bar_age',style={'height': '100%', 'width': '100%'})),className='',width=7)
            ],className=''),
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='bar_groupe',style={'height': '100%', 'width': '100%'}),style={'height': '400px', 'width': '100%', 'overflow': 'hidden'}),width=5,className=''),
                dbc.Col(html.Div(dcc.Graph(id='pyramide',style={'height': '100%', 'width': '100%'})),width=7,className=''),
            ],className=' mt-2'),
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='bar_don',style={'height': '100%', 'width': '100%'}),style={'height': '400px', 'width': '100%'}),width=5),
                dbc.Col(html.Div(dcc.Graph(id='bar',style={'height': '100%', 'width': '100%'}))),
            ],className='mt-2'),
            ],className='me-3 ms-3 mb-3 ')   
            ,style={'margin-left': '16.67%','margin-top': '90px', 'padding-top': '20px','z-index': 1,  # Valeur inférieure à celle de la navbar (1000)
            'position': 'relative'    },id="main-content",className='',width=10),
             
        ], className='')
    ])





