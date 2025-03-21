import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from widget import dropdown_groupe,sexe_check,type_check


# Créer une instance de l'application Dash sans `use_pages`
app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP,"/assets/style.css"])

data_donneur=pd.read_csv('donnees_nettoyees_donneurs.csv')



navbar=dbc.Row(
    [
    dbc.Col( html.Div([
                html.Img(src="assets/img/logo_qualisys.jpg", height="80px",width="100px", className="logo"),  # Logo de l'entreprise
                html.Img(src="assets/img/menu.svg", id="menu-btn", className="hamburger") 
            ], className="d-flex align-items-center "),width=2),  # Flexbox pour aligner le logo et le bouton hamburger
    dbc.Col([
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active",href="/candidat",id="nav-candidat")),
        dbc.NavItem(dbc.NavLink("A link", href="/donneur",id="nav-donneur")),
        dbc.NavItem(dbc.NavLink("Another link", href="/carte",id="nav-carte",)),
    ],className='nav-links d-flex  mt-auto ' 
   )
   ],width=10,className="d-flex flex-column mt-auto g-0")
   ], style={'width': '100vw', 'height': '80px','top': 0, 'z-index': 1000,'position':'fixed'},
   className='w-100 g-0 className="px-0 mx-0" bg-light'
    
)

# Layout de l'application
# app.layout = html.Section([navbar], style={'overflow-x': 'hidden'})

app.layout = html.Section([
    html.Div(navbar),
    html.Div([
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
            className='mt-4 ',
            ),
            width={"size": 8, "offset": 2},
            )
        ),
            
         dbc.Stack(
            [
                # html.Div(dropdown_groupe),
                # html.Div(sexe_check),
                
            ],
            gap=4,
            className='',
            
        )
            ]),style={'height': 'calc(100vh - 80px)','width': '16.67%', 'top': '80px','position':'fixed'},id="sidebar",width=2,className='bg-secondary '),
            dbc.Col(
            html.Div([
            dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Div(dcc.Graph(id='pie_sexe',style={'height': '100%', 'width': '100%'}),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'}),
                        html.Div(dcc.Graph(id='pie_distribution',style={'height': '100%', 'width': '100%'}),style={'height': '200px', 'width': '100%', 'overflow': 'hidden'},className='mt-2'),
                    ],className='me-2'),
                    # dbc.Col(html.Div('cool',style={'height': '100%', 'width': '100%', 'overflow': 'hidden'}),className=' '),
                ],className='g-2')
            ],width=5),
            dbc.Col(html.Div(dcc.Graph(id='bar_age',style={'height': '100%', 'width': '100%'})),className='',width=7)
            ],className=''),
            dbc.Row([
                dbc.Col('cool',width=5,className='bg-dark'),
                dbc.Col('cool',width=7,className='bg-primary'),
            ],className='me-2 mt-2'),
            dbc.Row(dbc.Col(html.Div('cool')),className='mt-2'),
            ],className='me-3 ms-3 mb-3 ')   
            ,style={'margin-left': '16.67%','margin-top': '80px' },id="main-content",className='',width=10),
             
        ], className='')
    ])
 ]
 ,style={'margin': 0, 'padding': 0},
#  'overflow-x': 'hidden'
 className="bg-secondary "
 )

# Callback pour afficher/masquer la sidebar
@app.callback(
    Output("sidebar", "style"),
    Output("main-content", "style"),
    Input("menu-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks):
    if n_clicks % 2 == 1:  # Barre latérale masquée
        return {'display': 'none'}, {'margin-left': '0', 'margin-top': '80px', 'width': '100%'}
    else:  # Barre latérale visible
        return ({'height': 'calc(100vh - 80px)', 'width': '16.67%', 'top': '80px', 'position': 'fixed'}, 
                {'margin-left': '16.67%', 'margin-top': '80px', 'width': 'calc(100% - 16.67%)'})


@app.callback(
    [Output("nav-candidat", "className"),
     Output("nav-donneur", "className"),
     Output("nav-carte", "className")],
    [Input("_pages_location", "pathname")]
)
def update_nav_active(pathname):
    # Liste des classes de base pour tous les liens
    base_class = "nav-link"
    
    # Initialisation des classes pour chaque lien
    candidat_class = base_class
    donneur_class = base_class
    carte_class = base_class
    
    # Si pathname est None, on retourne les classes de base
    if pathname is None:
        pathname = "/"
        
    # Ajout de la classe active en fonction du pathname
    candidat_class = f"{base_class} active" if pathname == "/candidat" else base_class
    donneur_class = f"{base_class} active" if pathname == "/donneur" else base_class
    carte_class = f"{base_class} active" if pathname == "/carte" else base_class
        
    return candidat_class, donneur_class, carte_class


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
                 title='Distribution des donneurs par sexe',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hole=0.3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        autosize=True,
        title_font=dict(size=13, color='black', family='Arial'),
       
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
                color_discrete_sequence=px.colors.sequential.Plasma_r)
    
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
                title='Âge moyen par type de donation et sexe',
                barmode='group',
                color_discrete_map={'M': 'blue', 'F': 'pink'})
    
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
          
# Lancer l'application
if __name__ == "__main__":
    app.run(debug=False)
