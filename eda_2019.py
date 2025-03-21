import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Supposons que les données sont déjà chargées dans un dataframe appelé 'df'
# Si vous avez besoin de charger les données depuis Excel:
df = pd.read_csv('donnees_nettoyees_2019.csv')

# 1. Distribution de l'éligibilité au don
def plot_eligibilite():
    fig = px.pie(df, 
                 names='ÉLIGIBILITÉ AU DON.', 
                 title='Distribution des éligibilités au don de sang',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend_title_text='Éligibilité',
        height=500,
        width=700
    )
    return fig

# 2. Distribution des donneurs par genre et éligibilité
def plot_genre_eligibilite():
    genre_elig = df.groupby(['Genre', 'ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')
    
    fig = px.bar(genre_elig, 
                 x='Genre', 
                 y='Nombre', 
                 color='ÉLIGIBILITÉ AU DON.',
                 title='Distribution des donneurs par genre et éligibilité',
                 barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Safe)
    
    fig.update_layout(
        xaxis_title='Genre',
        yaxis_title='Nombre de donneurs',
        legend_title_text='Éligibilité',
        height=500,
        width=800
    )
    return fig

# 3. Distribution des taux d'hémoglobine
def plot_hemoglobine():
    # Convertir en numérique si nécessaire
    df['Taux d\'hémoglobine'] = pd.to_numeric(df['Taux d’hémoglobine'], errors='coerce')
    
    # Créer deux sous-ensembles de données pour hommes et femmes
    df_h = df[df['Genre'] == 'm']
    df_f = df[df['Genre'] == 'f']
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Hommes', 'Femmes'))
    
    # Histogramme pour les hommes
    fig.add_trace(
        go.Histogram(x=df_h['Taux d\'hémoglobine'], 
                     name='Hommes',
                     marker_color='blue',
                     opacity=0.7),
        row=1, col=1
    )
    
    # Histogramme pour les femmes
    fig.add_trace(
        go.Histogram(x=df_f['Taux d\'hémoglobine'], 
                     name='Femmes',
                     marker_color='pink',
                     opacity=0.7),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='Distribution des taux d\'hémoglobine par genre',
        height=500, 
        width=900,
        showlegend=False
    )
    
    # Ajouter des lignes pour les seuils d'hémoglobine standard (13 g/dL pour les hommes, 12 g/dL pour les femmes)
    fig.add_vline(x=13, line_width=2, line_dash="dash", line_color="red", row=1, col=1)
    fig.add_vline(x=12, line_width=2, line_dash="dash", line_color="red", row=1, col=2)
    
    return fig

# 4. Répartition des dons par niveau d'étude et situation matrimoniale
def plot_education_matrimoniale():
    educ_matrim = df.groupby(['Niveau d\'etude', 'Situation Matrimoniale (SM)']).size().reset_index(name='Nombre')
    
    fig = px.bar(educ_matrim, 
                x='Niveau d\'etude', 
                y='Nombre', 
                color='Situation Matrimoniale (SM)',
                title='Répartition des donneurs par niveau d\'étude et situation matrimoniale',
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(
        xaxis_title='Niveau d\'études',
        yaxis_title='Nombre de donneurs',
        legend_title_text='Situation Matrimoniale',
        height=600,
        width=850
    )
    
    # Rotation des étiquettes si nécessaire
    fig.update_xaxes(tickangle=45)
    
    return fig

# 5. Carte de chaleur des raisons d'indisponibilité
def plot_raisons_indisponibilite():
    # Sélectionner uniquement les colonnes qui commencent par 'Raison indisponibilité'
    raisons_cols = [col for col in df.columns if col.startswith('Raison indisponibilité')]
    
    # Calculer le pourcentage de chaque raison
    raisons_counts = {}
    for col in raisons_cols:
        reason_name = col.split('[')[1].split(']')[0].strip()
        if 'Oui' in df[col].values:
            count = (df[col] == 'Oui').sum()
            percentage = (count / len(df)) * 100
            raisons_counts[reason_name] = percentage
    
    # Créer un dataframe pour le graphique
    raisons_df = pd.DataFrame(list(raisons_counts.items()), columns=['Raison', 'Pourcentage'])
    raisons_df = raisons_df.sort_values('Pourcentage', ascending=False)
    
    fig = px.bar(raisons_df, 
                x='Raison', 
                y='Pourcentage',
                title='Principales raisons d\'indisponibilité temporaire',
                color='Pourcentage',
                color_continuous_scale='Viridis')
    
    fig.update_layout(
        xaxis_title='Raison',
        yaxis_title='Pourcentage (%)',
        height=500,
        width=850
    )
    
    # Rotation des étiquettes
    fig.update_xaxes(tickangle=45)
    
    return fig

# 6. Distribution des âges des donneurs
def plot_ages():
    # Calculer l'âge à partir de la date de naissance
    # Supposons que la date de référence est la date de remplissage de la fiche
    df['Date de naissance'] = pd.to_datetime(df['Date de naissance'], errors='coerce')
    df['Date de remplissage de la fiche'] = pd.to_datetime(df['Date de remplissage de la fiche'], errors='coerce')
    
    # Filtrer les dates invalides (e.g., celles qui sont dans le futur)
    df_valid = df[(df['Date de naissance'].notna()) & (df['Date de naissance'] < pd.Timestamp('2010-01-01'))]
    
    # Calculer l'âge
    df_valid['Age'] = (df_valid['Date de remplissage de la fiche'] - df_valid['Date de naissance']).dt.days / 365.25
    df_valid['Age'] = df_valid['Age'].fillna(df_valid['Age'].median()).astype(int)
    
    # Filtrer les âges improbables
    df_valid = df_valid[(df_valid['Age'] >= 18) & (df_valid['Age'] <= 70)]
    
    # Grouper par tranche d'âge et par éligibilité
    df_valid['Tranche d\'âge'] = pd.cut(df_valid['Age'], 
                                        bins=[17, 25, 35, 45, 55, 65, 71],
                                        labels=['18-25', '26-35', '36-45', '46-55', '56-65', '66-70'])
    
    age_elig = df_valid.groupby(['Tranche d\'âge', 'ÉLIGIBILITÉ AU DON.']).size().reset_index(name='Nombre')
    
    fig = px.bar(age_elig, 
                x='Tranche d\'âge', 
                y='Nombre', 
                color='ÉLIGIBILITÉ AU DON.',
                title='Distribution des donneurs par tranche d\'âge et éligibilité',
                barmode='group',
                category_orders={"Tranche d'âge": ['18-25', '26-35', '36-45', '46-55', '56-65', '66-70']},
                color_discrete_sequence=px.colors.qualitative.G10)
    
    fig.update_layout(
        xaxis_title='Tranche d\'âge',
        yaxis_title='Nombre de donneurs',
        legend_title_text='Éligibilité',
        height=550,
        width=800
    )
    
    return fig

# Fonction pour afficher tous les graphiques dans un tableau de bord interactif
def display_dashboard(df_input):
    global df
    df = df_input.copy()
    
    # Créer les graphiques
    fig1 = plot_eligibilite()
    fig2 = plot_genre_eligibilite()
    fig3 = plot_hemoglobine()
    fig4 = plot_education_matrimoniale()
    fig5 = plot_raisons_indisponibilite()
    fig6 = plot_ages()
    
    # Afficher les graphiques
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()
    fig5.show()
    fig6.show()

# Exemple d'utilisation:
display_dashboard(df)