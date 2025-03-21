import numpy as np
import pandas as pd
from dash import Dash, html, Input, Output, dcc,dash_table,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

call = pd.read_csv('call.csv')

def create_header(image_path, title, height="5vh"):     
    """
    Crée un en-tête avec une image et un texte.
    
    Parameters:
        image_path (str): Le chemin de l'image à afficher
        title (str): Le titre à afficher à côté de l'image
        height (str): Hauteur du header (default: "5vh")
    
    Returns:
        html.Div: Un composant Dash contenant l'image et le titre alignés
    """
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src=image_path,
                        style={
                            "width": "30px",
                            "height": "30px",
                            "object-fit": "contain"
                        }
                    ),
                    width="auto",
                    className="ms-1 d-flex align-items-center"
                ),
                dbc.Col(
                    html.H6(
                        title, 
                        className="text-start ms-2"  
                    ),
                    width="auto",
                ),
            ],
            justify="start",
            align="center",
            className="g-0"  # Enlève le gutter entre les colonnes
        ),
        style={
            'borderBottom': '2px solid #ccc',
            # 'height': height,
            'padding': '2px 12px',
            'width': '100%'  # Assure que le header prend toute la largeur
        },
        className=' d-flex align-items-center'
    )

def create_pie_ans(data, values, names,color_discrete_map ):
    fig1 = px.pie(data, values=values, names=names,color=names,color_discrete_map=color_discrete_map, hole=.3)
    fig1.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",  # Supprime le fond général
    plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig1

def create_bar_chart(data, x , y , names ,color_discrete_map):
    fig2 = px.bar(data, x=x, y=y, color=names,color_discrete_map=color_discrete_map)
    fig2.update_layout(
    autosize=True,
    xaxis_title="",
    yaxis_title="",
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",  # Supprime le fond général
    plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig2

def create_gaugechart(x):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = x,
    mode = "gauge+number+delta",
    delta = {'reference': 3.5},
    gauge = {'axis': {'range': [None, 6]},
             'bar': {'color': "#144483"},
             'bordercolor': "#f8f9fa",
             'steps' : [
                 {'range': [0, 3], 'color': "#f8f9fa"},
                 {'range': [3, 6], 'color': "#f8f9fa"}],
             'threshold' : {'line': {'color': "#144483", 'width': 4}, 'thickness': 0.75, 'value': 3.5}}))
    fig.update_layout(
        autosize=True,  # Ajustement automatique
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",  # Supprime le fond général
        plot_bgcolor="rgba(0,0,0,0)"  # Largeur dynamique (supprime toute contrainte fixe)
    )

    return fig



dropdown1=  html.Div([
        "Agent",
        dcc.Dropdown(call['Agent'].unique(), id='dropdown_agent')
    ])

dropdown2=  html.Div([
        "Topic",
        dcc.Dropdown(call['Topic'].unique(), id='dropdown_topic')
    ])

daterange= html.Div([
    'Date',
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=np.min(call['Date']),
        end_date=np.max(call['Date']),
        display_format='YYYY-MM-DD'
    )])


app.layout = html.Section(
    [
        # Header
        html.Div(
            dbc.Row(
                [
                    # Colonne pour l'image
                    dbc.Col(
                        html.Img(
                            src="assets/img/group-call.png",
                            style={"width": "50px", "height": "50px"}
                        ),
                        width="auto",  # Ajuste automatiquement la taille
                        className="ms-2  d-flex align-items-center",# Supprime le padding et ajoute une marge gauche minimale
                    ),
                    # Colonne pour le texte
                    dbc.Col(
                        html.H2("CAll CENTER DATA", style={'font-family': 'Regular 400 Italic'},className="text-start m-0"),
                        width="auto",
                        style={"margin-left": "5px"},
                        className="p-0 m-0 d-flex align-items-center"
                    )
                ],
                justify="start",  # Aligne les colonnes sur la gauche
                align="center"    # Aligne verticalement au centre
            ),
            style={'borderBottom': '3px solid #dee2e6'},
            className='bg-light'
        ),

        # Contenu principal
        html.Div(
            dbc.Row(
                [
                dbc.Col(
                [
                html.Div([
                dbc.Stack(
            [
                html.Div(dropdown1),
                html.Div(dropdown2),
                html.Div(daterange),
            ],
            gap=3,
            ),
            ],className='bg-light',style={'height':'60%'}),
            html.Div([
            html.Div(create_header('assets/img/chart-pie-alt.png', 'Avg Speed of Answer')),
            html.Div(html.H2(id='kpi_mean',style={'flex': '1', 'minHeight': '0','fontSize': '50px',    
            'fontWeight': 'bold',},className='d-flex justify-content-center align-items-center'),
            style={'display': 'flex',
            'flexDirection': 'column',
            'height': '100%'}
            ),

            ],style={'height':'40%'})
            ],
            
                className='p-0 m-0',
                width=2,
                style={'height': '100%'}
                    ),
####################### side bar ##########################################################
            dbc.Col(
            [
            dbc.Row([
    dbc.Col([
        # Container principal avec flex column
        html.Div([
            # Header
            create_header('assets/img/historique-des-appels.png', 'Answered Call'),
            # Graph container qui prendra l'espace restant
            html.Div([
            dcc.Graph(
            id="pie_answer",
            style={
            'height': '100%',
            'width': '100%'
            },
            config={'displayModeBar': False},  # Optionnel : cache la barre d'outils
            )
            ],style={'flex': '1', 'minHeight': '0','marginTop': '10px'})  # minHeight important pour flex
            ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'height': '100%'
            }),
           ], width=4, className='p-0 m-0'),
           dbc.Col([
            html.Div(create_header('assets/img/poignee-de-main.png', 'Resolved Call')),
            html.Div(dcc.Graph(id='pie_res',style={'height':'100%','width':'100%'},config={'displayModeBar': False})
                    ,style={'flex': '1', 'minHeight': '0','marginTop': '10px'})
           ],style={'display':'flex','flexDirection':'column','height':'100%'}, width=4),
           dbc.Col([
               html.Div(create_header('assets/img/reseau-social.png', 'Average Satisfaction')),
               html.Div(dcc.Graph(id='gauge_chart',style={'height':'100%','width':'100%'},config={'displayModeBar': False})
                    ,style={'flex': '1', 'minHeight': '0','marginTop': '10px'})
           ],style={'display':'flex','flexDirection':'column','height':'100%'}, width=4),
           ],style={'height': '40%'}),

            dbc.Row([
            dbc.Col([
                html.Div(create_header('assets/img/graphique-histogramme.png', 'Number of Calls per Month')),
                html.Div(dcc.Graph(id='bar_char',style={'height':'100%','width':'100%'},config={'displayModeBar': False})
                    ,style={'flex': '1', 'minHeight': '0','marginTop': '10px'})
            ],style={'display':'flex','flexDirection':'column','height':'100%'},width=4),
            dbc.Col([
            html.Div(create_header('assets/img/casque.png', 'Agent Statistics')),
            html.Div(dash_table.DataTable(
            id='datatable',
            columns=[  # Les colonnes peuvent être définies dynamiquement dans le callback
            {'name': 'Agent', 'id': 'Agent'},
            {'name': 'Answered call', 'id': 'Answered_Count'},
            {'name': 'Resolved call', 'id': 'Resolved_Count'},
            {'name': 'Avg Speed of answer in sec', 'id': 'Speed of answer in seconds'},
            {'name': 'Satisfaction rating', 'id': 'Satisfaction rating'}
          ],
          data=[],  # Les données seront injectées via le callback

           # style_cell_conditional=[
           #     {
           #         'if': {'column_id': c},
           #         'textAlign': 'left'
           #     } for c in ['Date', 'Region']
           # ],
           style_data={
               'color': 'black',
               'backgroundColor': 'white'
           },
           style_data_conditional=[
           {
               'if': {'row_index': 'odd'},
               'backgroundColor': 'rgb(220, 220, 220)',
           }
          ],
          style_header={
              'backgroundColor': 'rgb(210, 210, 210)',
              'color': 'black',
              'fontWeight': 'bold'
          }
         ),style={'flex': '1', 'minHeight': '0','marginTop': '10px'})
            ],style={'display':'flex','flexDirection':'column','height':'100%'},width=8),
    
            ],style={'height': '60%'}),

            ],
            width=10,
            style={'height': '100%'}
            )
#################### zone a graphique ####################################################
                ],
                style={'height': '100%'}
            ),
            style={'flex':'1', 'overflow': 'hidden'},# Flexbox pour occuper l'espace restant
            className='ms-2 me-2 p-3'  
        )
    ],
    style={
        'height': '100vh',  # Hauteur de l'écran
        'overflow': 'hidden',
        'display':'flex',
        'flexDirection': 'column'
        
    },
    className='bg-light' 
    
)


@app.callback(
    [Output("pie_answer", "figure"),
    Output("pie_res", "figure")],
    [Input('dropdown_agent', "value"),
    Input("dropdown_topic", "value"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
    prevent_initial_call=False
)
def pie_chart(dropdown_agent=None, dropdown_topic=None, start_date=None, end_date=None):
    print(f"Agent: {dropdown_agent}")
    print(f"Topic: {dropdown_topic}")
    print(f"Dates: {start_date} to {end_date}")

    filtered_call = call.copy()
    
    # Vérifier si dropdown_agent est un objet iterable (liste, tableau, etc.)
    
    if dropdown_agent:
        filtered_call = filtered_call[filtered_call["Agent"] == dropdown_agent]
    
    if dropdown_topic:
        filtered_call = filtered_call[filtered_call["Topic"] == dropdown_topic]
    
    if start_date and end_date:
        filtered_call = filtered_call[
            (filtered_call["Date"] >= start_date) & (filtered_call["Date"] <= end_date)
        ]

    call_ans = filtered_call['Answered (Y/N)'].value_counts().reset_index()
    call_ans.columns = ['Answered (Y/N)', 'Count']
    call_res = filtered_call['Resolved'].value_counts().reset_index()
    call_res.columns = ['Resolved', 'Count']
    pie_ans = create_pie_ans(call_ans,'Count','Answered (Y/N)',color_discrete_map={'Y':'#144483','N':'#3584BF'})
    pie_res = create_pie_ans(call_res,'Count','Resolved',color_discrete_map={'Y':'#144483','N':'#3584BF'})
    return pie_ans,pie_res

@app.callback(
    Output("bar_char", "figure"),
    [Input('dropdown_agent', "value"),
    Input("dropdown_topic", "value"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
    prevent_initial_call=False
)
def bar_chart(dropdown_agent=None, dropdown_topic=None, start_date=None, end_date=None):
    print(f"Agent: {dropdown_agent}")
    print(f"Topic: {dropdown_topic}")
    print(f"Dates: {start_date} to {end_date}")
    
    filtered_call = call.copy()
    
    
    # Vérifier si dropdown_agent est un objet iterable (liste, tableau, etc.)
    
    if dropdown_agent:
        filtered_call = filtered_call[filtered_call["Agent"] == dropdown_agent]
    
    if dropdown_topic:
        filtered_call = filtered_call[filtered_call["Topic"] == dropdown_topic]
    
    if start_date and end_date:
        filtered_call = filtered_call[
            (filtered_call["Date"] >= start_date) & (filtered_call["Date"] <= end_date)
        ]
    grouped = filtered_call.groupby(['month', 'Answered (Y/N)']).size().reset_index(name='Count')
    ordre_mois=['January', 'February', 'March']
    grouped['month'] = pd.Categorical(grouped['month'], categories=ordre_mois, ordered=True)
    grouped = grouped.sort_values('month')
    bar_month = create_bar_chart(grouped, "month", "Count", "Answered (Y/N)",color_discrete_map={'Y':'#144483','N':'#3584BF'})
    return bar_month

@app.callback(
    Output("datatable", "data"),
    [Input('dropdown_agent', "value"),
    Input("dropdown_topic", "value"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
    prevent_initial_call=False
)
def data_table(dropdown_agent=None, dropdown_topic=None, start_date=None, end_date=None):
    print(f"Agent: {dropdown_agent}")
    print(f"Topic: {dropdown_topic}")
    print(f"Dates: {start_date} to {end_date}")
    
    filtered_call = call.copy()
    
    
    # Vérifier si dropdown_agent est un objet iterable (liste, tableau, etc.)
    
    if dropdown_agent:
        filtered_call = filtered_call[filtered_call["Agent"] == dropdown_agent]
    
    if dropdown_topic:
        filtered_call = filtered_call[filtered_call["Topic"] == dropdown_topic]
    
    if start_date and end_date:
        filtered_call = filtered_call[
            (filtered_call["Date"] >= start_date) & (filtered_call["Date"] <= end_date)
        ]
    # Création des colonnes pour comptage des conditions (si pas déjà fait)
    filtered_call['Answered_Count'] = (filtered_call['Answered (Y/N)'] == 'Y').astype(int)
    filtered_call['Resolved_Count'] = (filtered_call['Resolved'] == 'Y').astype(int)
       
       # Groupby et calcul des métriques
    result = filtered_call.groupby(['Agent']).agg({
           'Answered_Count': 'sum',  # Somme pour le nombre d'Answered (Y/N) == 'y'
           'Resolved_Count': 'sum',  # Somme pour le nombre de Resolved == 'Y'
           'Speed of answer in seconds': 'mean',           # Moyenne des notes
           'Satisfaction rating': 'mean'          # Moyenne des tailles
       })
    result['Speed of answer in seconds'] = result['Speed of answer in seconds'].round(2)
    result['Satisfaction rating'] = result['Satisfaction rating'].round(2)
       
       # Réinitialisation de l'index pour un DataFrame propre
    result = result.reset_index()
    return result.to_dict('records')

@app.callback(
    Output("gauge_chart", "figure"),
    [Input('dropdown_agent', "value"),
    Input("dropdown_topic", "value"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
    prevent_initial_call=False
)
def gauge_chart(dropdown_agent=None, dropdown_topic=None, start_date=None, end_date=None):
    print(f"Agent: {dropdown_agent}")
    print(f"Topic: {dropdown_topic}")
    print(f"Dates: {start_date} to {end_date}")

    filtered_call = call.copy()
    
    # Vérifier si dropdown_agent est un objet iterable (liste, tableau, etc.)
    
    if dropdown_agent:
        filtered_call = filtered_call[filtered_call["Agent"] == dropdown_agent]
    
    if dropdown_topic:
        filtered_call = filtered_call[filtered_call["Topic"] == dropdown_topic]
    
    if start_date and end_date:
        filtered_call = filtered_call[
            (filtered_call["Date"] >= start_date) & (filtered_call["Date"] <= end_date)
        ]
        
    chart_gauge = create_gaugechart(np.mean(filtered_call['Satisfaction rating']))
    
    return chart_gauge    
    

@app.callback(
    Output("kpi_mean", "children"),
    [Input('dropdown_agent', "value"),
    Input("dropdown_topic", "value"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
    prevent_initial_call=False
)
def kpi_m(dropdown_agent=None, dropdown_topic=None, start_date=None, end_date=None):
    print(f"Agent: {dropdown_agent}")
    print(f"Topic: {dropdown_topic}")
    print(f"Dates: {start_date} to {end_date}")

    filtered_call = call.copy()
    
    # Vérifier si dropdown_agent est un objet iterable (liste, tableau, etc.)
    
    if dropdown_agent:
        filtered_call = filtered_call[filtered_call["Agent"] == dropdown_agent]
    
    if dropdown_topic:
        filtered_call = filtered_call[filtered_call["Topic"] == dropdown_topic]
    
    if start_date and end_date:
        filtered_call = filtered_call[
            (filtered_call["Date"] >= start_date) & (filtered_call["Date"] <= end_date)
        ]
    avg_satisfaction=filtered_call['Speed of answer in seconds'].mean() 
    avg_satisfaction= f"{avg_satisfaction:.2f}"
    
    return avg_satisfaction   

       
if __name__ == "__main__":
 app.run()
