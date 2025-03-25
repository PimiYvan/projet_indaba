import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback,clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash
from widget import dropdown_groupe,type_check,sexe_check,don_check,genre_check,eligible,matrimoine
import json
import pathlib

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()

print(DATA_PATH.joinpath("donnees_nettoyees_donneurs.csv").exists())





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


# def get_pandas_data(csv_filename: str) -> pd.DataFrame:
#    '''
#    Load data from /data directory as a pandas DataFrame
#    using relative paths. Relative paths are necessary forcd
#    data loading to work in Heroku.
#    '''
#    PATH = pathlib.Path(__file__).parent
#    DATA_PATH = PATH.joinpath("data").resolve()
#    return pd.read_csv(DATA_PATH.joinpath(csv_filename))

# df = get_pandas_data("donnees_nettoyees_candidats (1).csv")

# data_donneur=pd.read_csv('donnees_nettoyees_donneurs.csv')
# df = pd.read_csv("donnees_nettoyees_candidats (1).csv") 

df['ÉLIGIBILITÉ AU DON.'] = df['ÉLIGIBILITÉ AU DON.'].replace({
    "Eligible": "Éligible",
    "Temporairement Non-eligible": "temporaire",
    "Définitivement non-eligible": "Non Éligible"
   })

navbar = dbc.Navbar(
    [
        dcc.Location(id="url", refresh=True),  # Ajout ici pour gérer la redirection
        dbc.Col(
            html.Div([
                html.H3('CRIMSON UNITY'),
            ], className=""),
            width=2
        ),
        dbc.Col(
            [
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Analyse des candidats",href="/candidat", id="nav-candidat")),
                        dbc.NavItem(dbc.NavLink("Analyse des donneurs", href="/donneur", id="nav-donneur")),
            
                    ],
                    className='nav-links d-flex mt-auto'
                )
            ],
            width=10,
            className="d-flex flex-column mt-auto g-0"
        )
    ],
    
    style={
        'width': '100%', 
        'height': '80px',
        'top': 0, 
        'z-index': 1000,
        'position': 'fixed',
        'background-color': '#f8f9fa'  # ajout d'une couleur de fond claire
    },
    className='w-100 g-0 px-0 mx-0 bg-light',
    sticky='top'
)

# Layout de l'application
# app.layout = html.Section([navbar], style={'overflow-x': 'hidden'})

app.layout = html.Section([
    html.Div(navbar),
    dash.page_container
 ]
 ,style={'margin': 0,"overflowX": "hidden"},
#  'overflow-x': 'hidden'
 className=""
 )









# Callback pour afficher/masquer la sidebar
# @app.callback(
#     Output("sidebar", "style"),
#     Output("main-content", "style"),
#     Input("menu-btn", "n_clicks"),
#     prevent_initial_call=True
# )
# def toggle_sidebar(n_clicks):
#     if n_clicks % 2 == 1:  # Barre latérale masquée
#         return {'display': 'none'}, {'margin-left': '0', 'margin-top': '80px', 'width': '100%'}
#     else:  # Barre latérale visible
#         return ({'height': 'calc(100vh - 80px)', 'width': '16.67%', 'top': '80px', 'position': 'fixed'}, 
#                 {'margin-left': '16.67%', 'margin-top': '80px', 'width': 'calc(100% - 16.67%)'})




@app.callback(
    [Output("nav-candidat", "className"),
     Output("nav-donneur", "className"),
     Output("url", "pathname")],  # Ajout pour redirection
    [Input("_pages_location", "pathname")]
)
def update_nav_active(pathname):
    base_class = "nav-link"

    # Si l'utilisateur arrive sur la page d'accueil ("/" ou None), on le redirige vers "/candidat"
    if pathname in [None, "/"]:
        return f"{base_class} active", base_class, "/candidat"
    
    # Gestion des onglets actifs
    candidat_class = f"{base_class} active" if pathname == "/candidat" else base_class
    donneur_class = f"{base_class} active" if pathname == "/donneur" else base_class

    return candidat_class, donneur_class, pathname




@app.callback(
    Output("pie_sexe", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def pie_sexe(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    sexe_counts = filtered_data['Sexe'].value_counts().reset_index()
    sexe_counts.columns = ['Sexe', 'Nombre']
    


    fig = px.pie(sexe_counts, 
                 values='Nombre', 
                 names='Sexe', 
                 color='Sexe',
                 color_discrete_map={'M':'#0091D5','F':'#EA6A47'},
                 hole=0.3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        autosize=True,
        title=dict(
        text='Distribution des donneurs par sexe',
        font=dict(size=13, color='black', family='Arial'),
        
        
    ), 
    
    margin=dict(l=0, r=0, t=30, b=0)  # Supprime les marges inutiles
        )
    return fig



@app.callback(
    Output("pie_distribution", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def pie_distribution(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    filtered_data['Kell Status'] = filtered_data["Phenotype"].str.contains(r'\+kell', na=False).map({True: 'Kell+', False: 'Kell-'})
    
    kell_counts= filtered_data['Kell Status'].value_counts().reset_index()
    kell_counts.columns = ['Kell Status', 'Nombre']
 
    
    fig = px.pie(kell_counts, 
                values='Nombre', 
                names='Kell Status', 
                title='Distribution des donneurs par statut Kell',
                color='Kell Status',
                color_discrete_map={  # Utilisation correcte de la carte des couleurs
               'Kell+': '#0091D5',  # Bleu
               'Kell-': '#EA6A47'   # Rouge-orange
    })
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
       autosize=True,
       title_font=dict(size=13, color='black', family='Arial'),
       margin=dict(l=0, r=0, t=30, b=0) 
    )
    return fig


@app.callback(
    Output("bar_age", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_age(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    filtered_data["Age "] = pd.to_numeric(filtered_data["Age"], errors='coerce')
    df_clean = filtered_data[(filtered_data["Age"].between(18, 70)) & (filtered_data['Type_donation'] != 'NAN')]
    
    # Calculer l'âge moyen par type de donation et sexe
    age_mean = df_clean.groupby(['Type_donation', 'Sexe'])["Age"].mean().reset_index()
    
    fig = px.bar(age_mean, 
                x='Type_donation', 
                y="Age", 
                color='Sexe',
                color_discrete_map={'M':'#0091D5', 'F':'#EA6A47'},
                title='Âge moyen par type de donation et sexe',
                barmode='group',
                )
    
    fig.update_layout(
        legend_title='Sexe',
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=2, t=30, b=0),
        xaxis=dict(
        tickvals=['F', 'B'],
        title_text=""  # Supprime le titre de l'axe X
        ),
        yaxis=dict(
        title_text=""
        ),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white" 
       )
    return fig


@app.callback(
    Output("bar_groupe", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_groupe(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    groupe_counts = filtered_data['Groupe_Sanguin'].value_counts().reset_index()
    groupe_counts.columns = ['Groupe', 'Nombre']

    # Séparer les groupes positifs et négatifs pour mieux visualiser
    groupe_counts['Rhesus'] = groupe_counts['Groupe'].str.contains(r'\+').map({True: 'Positif', False: 'Négatif'})
    groupe_counts['Groupe ABO'] = groupe_counts['Groupe'].str.replace(r'\+|\-', '', regex=True)

    fig = px.bar(groupe_counts, 
             x='Groupe ABO', 
             y='Nombre', 
             color='Rhesus',
             title='Distribution par groupe sanguin et rhésus',
             barmode='group',
             color_discrete_map={'Positif': '#0091D5', 'Négatif': '#EA6A47'})
    fig.update_layout(
        xaxis_title='Groupe sanguin ABO',
        yaxis_title='Nombre de donneurs',
        legend_title='Rhésus',
        autosize=True,
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white",
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=2, t=30, b=0),
        yaxis=dict(
        title_text=""
        ),
        xaxis=dict(
        title_text=""
        )
    )
    print(fig)
    return fig

        
@app.callback(
    Output("pyramide", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def pyramide(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    filtered_data["Age "] = pd.to_numeric(filtered_data["Age"], errors='coerce')
    data_donneur_clean = filtered_data[filtered_data["Age"].between(18, 70)]  # Filtrer les âges plausibles
    
    # Créer des tranches d'âge pour une meilleure visualisation
    bins = [17, 25, 30, 35, 40, 45, 50, 55, 60, 70]
    labels = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-70']
    data_donneur_clean['Tranche d\'âge'] = pd.cut(data_donneur_clean["Age"], bins=bins, labels=labels, right=False)
    
    # Compter par sexe et tranche d'âge
    age_sex_counts = data_donneur_clean.groupby(['Tranche d\'âge', 'Sexe']).size().unstack().fillna(0)
    
    # Convertir les comptes masculins en négatifs pour la pyramide
    if 'M' in age_sex_counts.columns:
        age_sex_counts['M'] = -age_sex_counts['M']
    
    # Créer la figure
    fig = go.Figure()
    
    # Ajouter les barres pour les femmes (F)
    if 'F' in age_sex_counts.columns:
        fig.add_trace(go.Bar(
            y=age_sex_counts.index,
            x=age_sex_counts['F'],
            name='Femmes',
            orientation='h',
            marker_color='#EA6A47'
        ))
    
    # Ajouter les barres pour les hommes (M)
    if 'M' in age_sex_counts.columns:
        fig.add_trace(go.Bar(
            y=age_sex_counts.index,
            x=age_sex_counts['M'],
            name='Hommes',
            orientation='h',
            marker_color='#0091D5'
        ))
    
    # Mise en page
    fig.update_layout(
        title='Pyramide des âges par sexe',
        xaxis_title='Nombre de donneurs (Hommes à gauche, Femmes à droite)',
        yaxis_title='Tranche d\'âge',
        autosize=True,
        barmode='relative',
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=2, t=30, b=0),
        yaxis=dict(
        title_text="",
        showticklabels=False
        ),
        xaxis=dict(
        title_text="",
        showticklabels=False
        ),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white",
        
        
    )
    return fig


@app.callback(
    Output("bar_don", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_don(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

        # Créer un tableau croisé des types de donation par groupe sanguin
    df_clean = filtered_data[filtered_data['Type_donation'] != 'NAN']
    donation_groupe = pd.crosstab(df_clean["Groupe_Sanguin"], filtered_data['Type_donation'])
    donation_groupe_melted = donation_groupe.reset_index().melt(
        id_vars=["Groupe_Sanguin"], 
        var_name='Type_donation', 
        value_name='Nombre'
    )
    
    fig = px.bar(donation_groupe_melted,
                x="Groupe_Sanguin",
                y='Nombre',
                color='Type_donation',
                title='Types de donation par groupe sanguin',
                barmode='stack',
                color_discrete_map={'B':'#0091D5','F':'#EA6A47'})
    
    fig.update_layout(
        xaxis_title='Groupe_Sanguin',
        yaxis_title='Nombre de donations',
        legend_title='Type_donation',
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=2, t=30, b=0),
        yaxis=dict(
        title_text=""
        ),
        xaxis=dict(
        title_text=""
        
        ),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white"
    )
    
    # Ajouter des annotations pour clarifier les types de donations
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        text="F = Don de sang total<br>B = Don de plasma/plaquettes",
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4
    )
    return fig

@app.callback(
    Output("bar", "figure"),
    [Input('dropdown_groupe', "value"),
    Input("sexe_check", "value"),
    Input("type_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_phenotype(dropdown_groupe=None, sexe_check=None, type_check=None):

    filtered_data = data_donneur.copy()
    if dropdown_groupe:
        filtered_data = filtered_data[filtered_data["Groupe_Sanguin"] == dropdown_groupe]
    if sexe_check:
        filtered_data = filtered_data[filtered_data["Sexe"].isin(sexe_check)]
    if type_check:        
        filtered_data = filtered_data[filtered_data["Type_donation"].isin(type_check)]

    data_phenotype = filtered_data.groupby('Phenotype').size().reset_index(name='Nombre')
    fig = go.Figure(go.Bar(
    x=data_phenotype['Nombre'],
    y=data_phenotype['Phenotype'],
    orientation='h',
    marker=dict(color='#0091D5') 
    ))
    
    fig.update_layout(
    title="Distribution des phénotypes",  
    autosize=True,
    title_font=dict(size=13, color='black', family='Arial'),
    margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor="white",  # Fond du graphique en blanc
    paper_bgcolor="white"
    )
    return fig
    


@app.callback(
    Output("pie_eligible", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def pie_eligible(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    filtered_data['ÉLIGIBILITÉ AU DON.'] = filtered_data['ÉLIGIBILITÉ AU DON.'].replace({
    "Eligible": "Éligible",
    "Temporairement Non-eligible": "temporaire",
    "Définitivement non-eligible": "Non Éligible"
   })


    fig = px.pie(filtered_data, 
                 names='ÉLIGIBILITÉ AU DON.', 
                 title='Distribution des éligibilités ',
                 color='ÉLIGIBILITÉ AU DON.',
                 color_discrete_map={'Éligible':'#0091D5','temporaire':'#EA6A47','Non Éligible':'#A5D8DD'}
                )
    
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(
        # legend_title_text='Éligibilité',
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
        
    )
    return fig


@app.callback(
    Output("pie_genre", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def pie_genre(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    fig = px.pie(filtered_data, names="Genre",color='Genre',title="Répartition des donneurs par genre",
                 color_discrete_map={'homme':'#0091D5','femme':'#EA6A47'})
    
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig


@app.callback(
    Output("bar_elig", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_elig(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

#     filtered_data['ÉLIGIBILITÉ AU DON.'] = filtered_data['ÉLIGIBILITÉ AU DON.'].replace({
#     "Eligible": "Éligible",
#     "Temporairement Non-eligible": "temporaire",
#     "Définitivement non-eligible": "Non Éligible"
#    })

    genre_elig = filtered_data.groupby(['Genre', 'ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')
    
    fig = px.bar(genre_elig, 
                 x='Genre', 
                 y='Nombre', 
                 color='ÉLIGIBILITÉ AU DON.',
                 title='Distribution des donneurs par genre et éligibilité',
                 barmode='group',
                 color_discrete_map={'Éligible':'#0091D5','temporaire':'#EA6A47','Non Éligible':'#A5D8DD'}
                 )
    
    fig.update_layout(
        xaxis_title='Genre',
        yaxis_title='Nombre de donneurs',
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white" ,
        xaxis=dict(
        title_text=""  # Supprime le titre de l'axe X
        ),
        yaxis=dict(
        title_text="",
        showticklabels=False,
        ),
        legend=dict(title_text="")
        
    )
    return fig



@app.callback(
    Output("bar_matri", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_matri(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    educ_matrim = filtered_data.groupby(['Niveau d\'etude', 'Situation Matrimoniale SM']).size().reset_index(name='Nombre')
    
    fig = px.bar(educ_matrim, 
                x='Niveau d\'etude', 
                y='Nombre', 
                color='Situation Matrimoniale SM',
                title='Répartition des donneurs par niveau d\'étude et situation matrimoniale',
                barmode='stack',
                color_discrete_map={'Célibataire':'#0091D5','Marié (e)':'#EA6A47','veuf (veuve)':'#A5D8DD','Divorcé(e)':'#1C4E80'})
    
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white" ,
        xaxis=dict(
        title_text=""  # Supprime le titre de l'axe X
        ),
        yaxis=dict(
        title_text="",
        showticklabels=False,
        ),
        legend=dict(title_text="")
        
    )
    return fig


@app.callback(
    Output("bar_edu", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_edu(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    # filtered_data['ÉLIGIBILITÉ AU DON.'] = filtered_data['ÉLIGIBILITÉ AU DON.'].replace({
    # "Eligible": "Éligible",
    # "Temporairement Non-eligible": "temporaire",
    # "Définitivement non-eligible": "Non Éligible"
    # })

    df_etud=filtered_data.groupby(["Niveau d'etude",'ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')
    
    fig = px.bar(df_etud, x="Niveau d'etude",y='Nombre',color="ÉLIGIBILITÉ AU DON.", title="Éligibilité au don selon le niveau d'étude",
                 color_discrete_map={'Éligible':'#0091D5','temporaire':'#EA6A47','Non Éligible':'#A5D8DD'})
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white" ,
        xaxis=dict(
        title_text=""  # Supprime le titre de l'axe X
        ),
        yaxis=dict(
        title_text="",
        showticklabels=False,
        ),
        legend=dict(title_text="")
        
    )
    return fig
    


@app.callback(
    Output("bar_tranche", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def bar_tranche(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    # filtered_data['ÉLIGIBILITÉ AU DON.'] = filtered_data['ÉLIGIBILITÉ AU DON.'].replace({
    # "Eligible": "Éligible",
    # "Temporairement Non-eligible": "temporaire",
    # "Définitivement non-eligible": "Non Éligible"
    # })
    bins = [18, 25, 35, 45, 55, 65]  # Bornes des tranches
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65']  # Labels des tranches

# Création de la colonne 'tranche_age'
    filtered_data['tranche_age'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)
    df_age_elig = filtered_data.groupby(['tranche_age','ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')  

    df_age_elig = filtered_data.groupby(['tranche_age','ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')
    fig = px.bar(df_age_elig, x="tranche_age", y="Nombre", color='ÉLIGIBILITÉ AU DON.',
             color_discrete_map={'Éligible':'#0091D5','temporaire':'#EA6A47','Non Éligible':'#A5D8DD'},
             title="Répartition de l'âge selon l'éligibilité")
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="white",  # Fond du graphique en blanc
        paper_bgcolor="white" ,
        xaxis=dict(
        title_text=""  # Supprime le titre de l'axe X
        ),
        yaxis=dict(
        title_text="",
        showticklabels=False,
        ),
        legend=dict(title_text="")
        
    )
    return fig



@app.callback(
    Output("map", "figure"),
    [Input('dropdown_eligible', "value"),
     Input('dropdown_matrimoine', "value"),
    Input("don_check", "value"),
    Input("genre_check", "value"),
    ],
    prevent_initial_call=False
)
def map(dropdown_eligible=None,dropdown_matrimoine=None, don_check=None, genre_check=None):

    filtered_data = df.copy()
    if dropdown_eligible:
        filtered_data = filtered_data[filtered_data["ÉLIGIBILITÉ AU DON."] == dropdown_eligible]
    if dropdown_matrimoine:
        filtered_data = filtered_data[filtered_data["Situation Matrimoniale SM"] == dropdown_matrimoine]
    if don_check:
        filtered_data = filtered_data[filtered_data["A t il elle déjà donné le sang"].isin(don_check)]
    if genre_check:        
        filtered_data = filtered_data[filtered_data["Genre"].isin(genre_check)]

    with open(DATA_PATH.joinpath("douala_arrondissements.json"), "r", encoding="utf-8") as f:
        json_data = json.load(f)

# Modifier le JSON pour correspondre aux noms du DataFrame
    for feature in json_data["features"]:
        feature["properties"]["NAME_3"] = feature["properties"]["NAME_3"].replace("Douala", "Douala ")

# Charger les données du DataFrame
    df_ville = filtered_data.groupby('Arrondissement de résidence').size().reset_index(name='Nombre')

# Filtrer seulement Douala 1 à 5
    arrondissements_douala = ["Douala 1", "Douala 2", "Douala 3", "Douala 4", "Douala 5"]
    df_ville = df_ville[df_ville["Arrondissement de résidence"].isin(arrondissements_douala)]

# Créer la carte
    fig = px.choropleth_mapbox(
    data_frame=df_ville,
    geojson=json_data,
    featureidkey="properties.NAME_3",
    locations="Arrondissement de résidence",
    color="Nombre",
      color_continuous_scale=[  
        (0.0, "#A5D8DD"),  
        (0.5, "#0091D5"),  
        (1.0, "#1C4E80")   
    ],
    mapbox_style="open-street-map",
    center={"lat": 4.06, "lon": 9.71},
    zoom=9,
    title="Distribution des candidats par arrondissement"
  )

    fig.update_traces(marker_line_width=2, marker_line_color="white")
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    return fig

   




 
    

          
# Lancer l'application
if __name__ == "__main__":
    app.run(debug=False)

