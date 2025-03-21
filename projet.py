import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output,dcc,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import locale
locale.setlocale(locale.LC_TIME, "French_France")


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



sales = pd.read_csv('sales.csv')
# print(sales)


def format_number(value):
    try:
        value = float(value)  
        if value >= 1000000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1000:
            return f"{value / 1000:.1f}K"
        else:
            return f"£{value:,.2f}"  
    except ValueError:
        return "Invalid number"
      
    
def create_pie_chart(data1, values, names, title,color_discrete_map):
    fig1 = px.pie(data1, values=values, names=names,color=names, color_discrete_map=color_discrete_map, hole=.3)
    fig1.update_layout(
    autosize=True,
    title=title,
    title_font=dict(size=20, color='black', family='Arial'),
    margin=dict(l=0, r=0, t=50, b=0))
    return fig1

def create_bar_chart(data, x, y, title):
    fig2 = px.bar(data, x=x, y=y,orientation='h')
    fig2.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="",
        autosize=True,
        title_font=dict(size=20, color='black', family='Arial'),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig2


def create_revenue_kpi_card(id, card_title, image_src,):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    
                    dbc.Col(
                        html.Div(
                            html.Img(
                                src=image_src,  
                                style={
                                    "width": "50px",
                                    "height": "50px",
                                    "marginRight": "10px",  
                                },
                            ),
                            style={
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                        ),
                        width=3,
                    ),
                    # Colonne pour le contenu texte (à droite)
                    dbc.Col(
                        html.Div(
                            [
                                html.H3(id=id, className="card-text text-center mb-1"),
                                html.H6(card_title, className="card-subtitle mb-0 small-text inline-text text-center p-0 m-0 ",style={"font-size":"14px"} ),
                            ],
                            
                            style={"textAlign": "left"},  
                        ),
                        width=9,
                    ),
                ],
                align="center", 
                justify="start",  
            ),
        ),
        className="w-100 text-white text-center rounded-3  mb-3  ms-1  ",
        style={"backgroundColor": "#00747c","height": "95px"},  
    )

checklist1=dcc.Checklist(id='checklist-trim',  # Ajoutez un ID unique
        options=[{'label': str(trim), 'value': trim} for trim in sales['trimestre'].unique()],
        inline=True,
        className='text-white ')
    
checklist2=dcc.Checklist(id='checklist-annee',
        options=[{'label': str(annee), 'value': annee} for annee in sales['annee'].unique()],
        inline=True,
        className='text-white')
        
segment_style = {
    'border': '1px solid #ccc',
    'borderRadius': '5px',
    'padding': '10px',
    'margin': '5px',
    'backgroundColor': '#00747c',
    'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
}

segment1 = html.Div(checklist1, style=segment_style)
segment2 = html.Div(checklist2, style=segment_style)

header_content = dbc.Row(
    [
        dbc.Col(html.H2("Sales Analysis"), width='auto',className='ms-3'),  # Texte à gauche
        dbc.Col(dbc.Row(
            [
                dbc.Col(segment1, width='auto'),
                dbc.Col(segment2, width='auto')
            ],
            align='center',
            justify='end',
            className="g-0"  # Supprime les espacements horizontaux entre les colonnes
        ), width=True)  # Colonnes pour les segments alignées à droite
    ],
    align='center',
    className="g-0",  # Supprime les espacements horizontaux entre les colonnes
    style={'height': '100%'}
)

header = dbc.Container(
    header_content,
    fluid=True,
    className="m-0 p-0",  # Supprime les marges et les espacements internes
    style={
        'backgroundColor': '#f8f9fa',
        'padding': '10px 20px',  # Ajustez le padding selon vos besoins
        'borderBottom': '1px solid #dee2e6'
    }
)
    

app.layout = html.Section(
    [


    html.Div(header,className="m-0 p-0 fixed-top"),

    

# ),############# header###############################################################
        html.Section(
            [
              dbc.Row(
            [
                dbc.Col( html.Div(
                    [
                        html.H3("kpi",className='text-center mb-2'),
                        html.Hr(style={"border": "3px solid", "width": "100%","margin":"0","padding": "0"},className="bg-dark mb-3"),
                        dbc.Stack(
            [
                html.Div(create_revenue_kpi_card(
                        id='kpi_ca',
                        card_title="Chiffre d'affaire ",
                        image_src="assets/revenue.png",  # Exemple d'image
                        ),),
                
                 html.Div(
                     create_revenue_kpi_card(
                     id='kpi_ct',
                     card_title="Cout Total",
                     image_src="assets/calculator (1).png",  # Exemple d'image
                     ),),
                html.Div(create_revenue_kpi_card(
                     id="kpi_marge",
                     card_title="Marge",
                     image_src="assets/broker.png",  # Exemple d'image
                     ),),
                html.Div(create_revenue_kpi_card(
                     id='kpi_delai',
                     card_title="Delai de livraison",
                     image_src="assets/fast-delivery.png",  # Exemple d'image
                     ),),
            ],
            gap=3,
        ),
                    ]),width=2,style={"height": "100vh", "overflow": "hidden"}),
               ##### ########### zone pour les segments###########################
                dbc.Col([
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Graph(id="pie_category",style={"width": "100%", "height": "100%"}) ),
                                            dbc.Col(dcc.Graph(id="pie_canal",style={"width": "100%", "height": "100%"}) )
                                        ],
                                         style={"height": "50%", "overflow": "hidden"} 
                                        
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Graph(id="bar_prod",style={"width": "100%", "height": "100%","overflow":"auto"}) ),
                                            dbc.Col(dcc.Graph(id="bar_client",style={"width": "100%", "height": "100%","overflow":"auto"}))
                                        ],
                                        style={"height": "50%", "overflow": "hidden"} 
                                    )
                                ]),
                            dbc.Col(dcc.Graph(id="map_chiffre",style={"width": "100%", "height": "100%","overflow":"auto"}),width=5),
                        ],
                        style={"height": "70%", "overflow": "hidden"}   
                    ),
                    dbc.Row(dcc.Graph(id="bar_date",style={"width": "100%", "height": "100%","overflow":"auto"}),style={"height": "30%", "overflow": "hidden"})
                    
                    
                ],
                 width=10,
                 style={"height": "100vh", "overflow": "hidden"}
                    )
                    
               ])],style={"margin-top": "70px"})],className="m-0 p-0")
               
            
                
           

@app.callback(
    [Output("pie_category", "figure"),
    Output("pie_canal", "figure")],
     
    [Input("checklist-trim", "value"),
    Input("checklist-annee", "value")],
    prevent_initial_call=False
    )

def pie_chart(trimestre=None, annee=None):
    filtered_sales = sales.copy()
    print(filtered_sales)
    if trimestre:
        filtered_sales = filtered_sales[filtered_sales["trimestre"].isin(trimestre)]
    if annee:
        filtered_sales = filtered_sales[filtered_sales["annee"].isin(annee)]

    fig_category = create_pie_chart(filtered_sales, "marge", 'Catégorie', 'Marge par catégorie',color_discrete_map={'Catégorie 1':'#00747c','Catégorie 2':'#00bbc9'})
    fig_canal = create_pie_chart(filtered_sales, 'marge', 'Canal', 'Marge par canal',color_discrete_map={'Grossiste':'#00747c','Détaillant':'#00bbc9','Export':'#cacaca'})
   
    return fig_category,fig_canal 


@app.callback(
   [ Output("bar_prod", "figure"),
    Output("bar_client", "figure")],
   
    
    [Input("checklist-trim", "value"),
    Input("checklist-annee", "value")],
    prevent_initial_call=False
    )

def bar_chart(trimestre=None, annee=None):

    filtered_sales = sales.copy()
    if trimestre:
        filtered_sales = filtered_sales[filtered_sales["trimestre"].isin(trimestre)]
    if annee:
        filtered_sales = filtered_sales[filtered_sales["annee"].isin(annee)]

    sales_produit = filtered_sales.groupby('Nom_Produit')["chiffre d'affaire"].sum().reset_index().sort_values("chiffre d'affaire", ascending=True)[:5]
    bar_produit = create_bar_chart(sales_produit, "chiffre d'affaire", "Nom_Produit", "Chiffre d'affaire par produit")
    bar_produit.update_traces(marker_color='#00747c') 

    sales_client = filtered_sales.groupby('Client')["chiffre d'affaire"].sum().reset_index().sort_values("chiffre d'affaire", ascending=True)[:5]
    bar_cl = create_bar_chart(sales_client, "chiffre d'affaire", "Client", "Chiffre d'affaire par client")
    bar_cl.update_traces(marker_color='#00bbc9') 
    return bar_produit,bar_cl

@app.callback(
    
    Output("map_chiffre", "figure"),
    
    [Input("checklist-trim", "value"),
    Input("checklist-annee", "value")],
    prevent_initial_call=False
    )
def map_chart(trimestre=None, annee=None):

    filtered_sales = sales.copy()
    if trimestre:
        filtered_sales = filtered_sales[filtered_sales["trimestre"].isin(trimestre)]
    if annee:
        filtered_sales = filtered_sales[filtered_sales["annee"].isin(annee)]


    map_ca = px.scatter_mapbox(
    filtered_sales,
    lat="latitude",
    lon="longitude",
    text="Ville",
    zoom=5,
    size = "chiffre d'affaire",
    mapbox_style="open-street-map")

    map_ca.update_traces(marker=dict(color='#00747c'))

    map_ca.update_layout(
    title="chiffre d'affaire par ville",
    autosize=True,
    title_font=dict(size=20, color='black', family='Arial'),
    margin=dict(l=0, r=0, t=50, b=0))

    return map_ca

@app.callback(
    
    Output("bar_date", "figure"),
    
    [Input("checklist-trim", "value"),
    Input("checklist-annee", "value")],
    prevent_initial_call=False
    )
def bar_date(trimestre=None, annee=None):

    filtered_sales = sales.copy()
    if trimestre:
        filtered_sales = filtered_sales[filtered_sales["trimestre"].isin(trimestre)]
    if annee:
        filtered_sales = filtered_sales[filtered_sales["annee"].isin(annee)]

    sales_date = filtered_sales.groupby('Date de Commande')["chiffre d'affaire"].sum().reset_index()
    bar_date1 = px.bar(sales_date, x='Date de Commande', y="chiffre d'affaire")
    bar_date1.update_traces(marker_color='#00747c') 
    bar_date1.update_layout(
    title="chiffre d'affaire par date",
    autosize=True,
    xaxis_title="",  # Supprime le titre de l'axe X
    yaxis_title="",
    title_font=dict(size=20, color='black', family='Arial'),
    margin=dict(l=0, r=0, t=50, b=0))
    return bar_date1

@app.callback(
    [
    Output("kpi_ca", "children"),
    Output("kpi_ct", "children"),
    Output("kpi_marge", "children"),
    Output("kpi_delai", "children")
    ], 
    [Input("checklist-trim", "value"),
    Input("checklist-annee", "value")],
    prevent_initial_call=False
    )
def update_kpis(trimestre=None, annee=None):
    filtered_sales = sales.copy()
    if trimestre:
        filtered_sales = filtered_sales[filtered_sales["trimestre"].isin(trimestre)]
    if annee:
        filtered_sales = filtered_sales[filtered_sales["annee"].isin(annee)]
    ca = filtered_sales["chiffre d'affaire"].sum()
    ct = filtered_sales["cout total"].sum()
    marge = (filtered_sales['marge'].sum()/filtered_sales["chiffre d'affaire"].sum())
    delai= filtered_sales['delai'].mean()

    formatted_ca='£'+format_number(ca)
    formatted_ct='£'+format_number(ct)
    formatted_marge = f"{marge * 100:.2f}%"
    formatted_delai = f"{delai:.0f}Jrs"

    return formatted_ca,formatted_ct,formatted_marge,formatted_delai

    
  

if __name__ == "__main__":
    app.run()