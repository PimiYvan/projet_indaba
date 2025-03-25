import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import dash_mantine_components as dmc
import pathlib
import os



PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()

print(os.listdir(DATA_PATH))

# print(DATA_PATH.joinpath("donnees_nettoyees_donneurs.csv").exists())

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
data_donneur = get_pandas_data("donnees_nettoyees_donneurs.csv")


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

options_sexe = data_donneur['Sexe'].unique()
options_type = data_donneur['Type_donation'].unique()
options_don=df['A t il elle déjà donné le sang'].unique()
options_genre=df['Genre'].unique()

df['ÉLIGIBILITÉ AU DON.'] = df['ÉLIGIBILITÉ AU DON.'].replace({
    "Eligible": "Éligible",
    "Temporairement Non-eligible": "temporaire",
    "Définitivement non-eligible": "Non Éligible"
   })

dropdown_groupe=  html.Div([
        html.Div("Groupe Sanguin",style={"fontSize": "15px"}),
        dcc.Dropdown(data_donneur['Groupe_Sanguin'].unique(),style={
            "fontSize": "12px"  # Réduit la taille du texte des options et du bouton
        }, id='dropdown_groupe')
    ])

eligible= html.Div([
        html.Div("Éligibilite au don",style={"fontSize": "15px"}),
        dcc.Dropdown(df['ÉLIGIBILITÉ AU DON.'].unique(), id='dropdown_eligible')
    ])

matrimoine=html.Div([
        html.Div("Situation Matrimoniale",style={"fontSize": "15px"}),
        dcc.Dropdown(df['Situation Matrimoniale SM'].unique(), id='dropdown_matrimoine')
    ])

don_check = dmc.MantineProvider(
    theme={"components": {
        "Chip": {
            "styles": {
                "label": {
                    "width": "100%",  # Prend toute la largeur disponible
                    "justifyContent": "center",
                    "alignItems": "center",  
                    "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
                },
                "input": {
                        ":checked + label": {  # Ciblage du label lorsque l'input est coché
                            "backgroundColor": "#228BE6 !important",
                            "color": "white !important"
                        }
                    },
                "checkIcon": {
                    "display": "none"  # Cache l'icône de coche
                }
            }
        }
    }},
    children=[
        html.Div("A t il elle déjà donné le sang"),
        
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="don_check",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        don,
                        value=don,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for don in options_don
                ]
            ),
            style={
                "width": "100%", 
                "display": "flex",
                "flexDirection": "column",  # Affichage en colonne
                "gap": "10px"  # Espacement entre les boutons
            }
        )
    ]
)


genre_check = dmc.MantineProvider(
    theme={"components": {
        "Chip": {
            "styles": {
                "label": {
                    "width": "100%",  # Prend toute la largeur disponible
                    "justifyContent": "center",
                    "alignItems": "center",  # Centre le texte horizontalement
                    "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
                },
                "input": {
                        ":checked + label": {  # Ciblage du label lorsque l'input est coché
                            "backgroundColor": "#228BE6 !important",
                            "color": "white !important"
                        }
                    },
                "checkIcon": {
                    "display": "none"  # Cache l'icône de coche
                }
            }
        }
    }},
    children=[
        html.Div("Genre", style={"fontSize": "15px"}),

        
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="genre_check",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        genre,
                        value=genre,
                        variant="filled",
                        # color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip",
                    )
                    for genre in options_genre
                ]
            ),
            style={
                "width": "100%", 
                "display": "flex",
                "flexDirection": "column",  # Affichage en colonne
                "gap": "10px"  # Espacement entre les boutons
            }
        )
    ]
)





# Configuration du thème Mantine
sexe_check = dmc.MantineProvider(
    theme={
        "components": {
            "Chip": {
                "styles": {
                    "root": {
                        "width": "100%"  # Assure que le chip prend toute la largeur
                    },
                    "label": {
                        "width": "100%",  # Prend toute la largeur disponible
                        "justifyContent": "center",  # Centre le texte horizontalement
                        "padding": "8px 12px",  # Padding supplémentaire pour l'esthétique
                        # "fontWeight": 500,  # Rend le texte légèrement plus gras
                        "transition": "all 0.2s ease"  # Animation douce
                    },
                    "input": {
                        ":checked + label": {  # Ciblage du label lorsque l'input est coché
                            "backgroundColor": "#228BE6 !important",
                            "color": "white !important"
                        }
                    },
                    "checkIcon": {
                        "display": "none"  # Cache l'icône de coche
                    }
                }
            }
        }
    },
    children=[
        html.Div("Sexe", style={
            "fontSize": "15px", 
        }),
        
        # Conteneur pour gérer l'affichage vertical et l'alignement
        html.Div(
            dmc.ChipGroup(
                id="sexe_check",
                multiple=True,  # Sélection unique
                value=[],
                children=[
                    dmc.Chip(
                        sexe,
                        value=sexe,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for sexe in options_sexe
                ]
            ),
            style={
                "width": "100%", 
                "display": "flex",
                "flexDirection": "column",  # Affichage en colonne
                "gap": "10px"  # Espacement entre les boutons
            }
        )
    ]
)


type_check = dmc.MantineProvider(
    theme={"components": {
        "Chip": {
            "styles": {
                "root": {
                    "width": "100%"  # Assure que le chip prend toute la largeur
                },
                "label": {
                    "width": "100%",  # Prend toute la largeur disponible
                    "justifyContent": "center",  # Centre le texte horizontalement
                    "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
                },
                "input": {
                        ":checked + label": {  # Ciblage du label lorsque l'input est coché
                            "backgroundColor": "#228BE6 !important",
                            "color": "white !important"
                        }
                    },
                "checkIcon": {
                    "display": "none"  # Cache l'icône de coche
                }
            }
        }
    }},
    children=[
        html.Div("Type donation", style={"fontSize": "15px"}),
        
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="type_check",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        type,
                        value=type,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for type in options_type
                ]
            ),
            style={
                "width": "100%", 
                "display": "flex",
                "flexDirection": "column",  # Affichage en colonne
                "gap": "10px"  # Espacement entre les boutons
            }
        )
    ]
)


