import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output,dcc,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash


app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP,"/assets/style.css"])




nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active", href="/",id="nav-home",className='text-dark nav-link ')),
        dbc.NavItem(dbc.NavLink("A link", href="/performance",id="nav-performance",className='text-dark nav-link ')),
        dbc.NavItem(dbc.NavLink("Another link", href="/Analyse",id="nav-analyse",className='text-dark nav-link  ')),
        dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#",className='text-dark nav-link')),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            nav=True,
        )
     ],className='mt-auto nav-custom'

)


app.layout = html.Section([
    dbc.Row(
        [
            dbc.Col(html.Div('cool'),width=2,className='bg-light' ,style={"height": "100vh"}),
            dbc.Col([
                html.Div(nav,className=' d-flex flex-column  bg-secondary',style={"height": "80px",} ),
                dash.page_container 
            ],width=10)
        ],className="g-0",
    ),

    # dcc.Location pour gérer l'URL
    # dcc.Location(id="url", refresh=False)
])








# Callback pour afficher la page demandée
# def display_page(pathname):
#     # 🔹 Par défaut, charger la page "/Acceuil"
#     if pathname == "/" or pathname == "/Acceuil":
#         return dash.page_registry["pages.Acceuil"]["layout"]  # Charge le layout de la page Acceuil
    
#     # 🔹 Vérifier si la page demandée existe
#     if pathname in Dash.page_registry:
#         return dash.page_registry[pathname]["layout"]
    
#     # ❌ Si la page n'existe pas
#     return html.H1("Page introuvable", className="text-danger")


# Callback pour mettre à jour dynamiquement la classe 'active'

@callback(
    [Output("nav-home", "className"),
     Output("nav-performance", "className"),
     Output("nav-analyse", "className")],
    [Input("_pages_location", "pathname")]
)
def update_nav_active(pathname):
    # Liste des classes de base pour tous les liens
    base_classes = "text-dark nav-link"
    
    # Initialisation des classes pour chaque lien
    home_class = base_classes
    performance_class = base_classes
    analyse_class = base_classes
    
    # Si pathname est None, on retourne les classes de base
    if pathname is None:
        pathname = "/"
        
    # Ajout de la classe active en fonction du pathname
    if pathname == "/":
        home_class += " active"
    elif pathname == "/performance":
        performance_class += " active"
    elif pathname == "/Analyse":
        analyse_class += " active"
        
    return home_class, performance_class, analyse_class










if __name__ == "__main__":
    app.run()