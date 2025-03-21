import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Supposons que les données sont déjà chargées dans un dataframe appelé 'df'
# Si vous avez besoin de charger les données depuis Excel:
df = pd.read_csv('donnees_nettoyees_2020.csv')

# 1. Distribution par sexe
def plot_distribution_sexe():
    sexe_counts = df['Sexe'].value_counts().reset_index()
    sexe_counts.columns = ['Sexe', 'Nombre']
    
    fig = px.pie(sexe_counts, 
                 values='Nombre', 
                 names='Sexe', 
                 title='Distribution des donneurs par sexe',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hole=0.3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        annotations=[dict(text='n=1900', x=0.5, y=0.5, font_size=18, showarrow=False)],
        height=500,
        width=700
    )
    return fig

# 2. Distribution par groupe sanguin et rhésus
def plot_distribution_groupe_sanguin():
    groupe_counts = df['Groupe Sanguin ABO / Rhesus '].value_counts().reset_index()
    groupe_counts.columns = ['Groupe', 'Nombre']
    
    # Séparer les groupes positifs et négatifs pour mieux visualiser
    groupe_counts['Rhesus'] = groupe_counts['Groupe'].str.contains('\+').map({True: 'Positif', False: 'Négatif'})
    groupe_counts['Groupe ABO'] = groupe_counts['Groupe'].str.replace('\+|\-', '')
    
    fig = px.bar(groupe_counts, 
                x='Groupe ABO', 
                y='Nombre', 
                color='Rhesus',
                title='Distribution par groupe sanguin et rhésus',
                barmode='group',
                color_discrete_map={'Positif': '#FF4C4C', 'Négatif': '#4C72FF'})
    
    fig.update_layout(
        xaxis_title='Groupe sanguin ABO',
        yaxis_title='Nombre de donneurs',
        legend_title='Rhésus',
        height=500,
        width=800
    )
    return fig

# 3. Pyramide des âges par sexe
def plot_pyramide_ages():
    # Nettoyer la colonne d'âge pour ne garder que les valeurs numériques valides
    df["Age "] = pd.to_numeric(df["Age "], errors='coerce')
    df_clean = df[df["Age "].between(18, 70)]  # Filtrer les âges plausibles
    
    # Créer des tranches d'âge pour une meilleure visualisation
    bins = [17, 25, 30, 35, 40, 45, 50, 55, 60, 70]
    labels = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-70']
    df_clean['Tranche d\'âge'] = pd.cut(df_clean["Age "], bins=bins, labels=labels, right=False)
    
    # Compter par sexe et tranche d'âge
    age_sex_counts = df_clean.groupby(['Tranche d\'âge', 'Sexe']).size().unstack().fillna(0)
    
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
            marker_color='pink'
        ))
    
    # Ajouter les barres pour les hommes (M)
    if 'M' in age_sex_counts.columns:
        fig.add_trace(go.Bar(
            y=age_sex_counts.index,
            x=age_sex_counts['M'],
            name='Hommes',
            orientation='h',
            marker_color='blue'
        ))
    
    # Mise en page
    fig.update_layout(
        title='Pyramide des âges par sexe',
        xaxis_title='Nombre de donneurs (Hommes à gauche, Femmes à droite)',
        yaxis_title='Tranche d\'âge',
        barmode='relative',
        bargap=0.1,
        height=600,
        width=900
    )
    
    # Formater l'axe des x pour afficher des valeurs absolues
    fig.update_xaxes(tickformat='abs')
    
    return fig

# 4. Types de donation par groupe sanguin
def plot_donation_par_groupe():
    # Filtrer les valeurs NAN dans le type de donation
    df_clean = df[df['Type de donation'] != 'NAN']
    
    # Créer un tableau croisé des types de donation par groupe sanguin
    donation_groupe = pd.crosstab(df_clean["Groupe Sanguin ABO / Rhesus "], df_clean['Type de donation'])
    donation_groupe_melted = donation_groupe.reset_index().melt(
        id_vars=["Groupe Sanguin ABO / Rhesus "], 
        var_name='Type de donation', 
        value_name='Nombre'
    )
    
    fig = px.bar(donation_groupe_melted,
                x="Groupe Sanguin ABO / Rhesus ",
                y='Nombre',
                color='Type de donation',
                title='Types de donation par groupe sanguin',
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(
        xaxis_title='Groupe sanguin',
        yaxis_title='Nombre de donations',
        legend_title='Type de donation',
        height=500,
        width=850
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

# 5. Distribution des phénotypes
def plot_distribution_phenotypes():
    # Simplifier les phénotypes pour une meilleure visualisation
    # On extrait juste la partie "kell" pour voir la distribution
    df['Kell Status'] = df["Phenotype "].str.contains('\+kell').map({True: 'Kell+', False: 'Kell-'})
    
    kell_counts = df['Kell Status'].value_counts().reset_index()
    kell_counts.columns = ['Kell Status', 'Nombre']
    
    fig = px.pie(kell_counts, 
                values='Nombre', 
                names='Kell Status', 
                title='Distribution des donneurs par statut Kell',
                color_discrete_sequence=px.colors.sequential.Plasma_r)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=500,
        width=700
    )
    return fig

# 6. Analyse croisée de l'âge moyen par type de donation et sexe
def plot_age_moyen_donation_sexe():
    # Nettoyer la colonne d'âge
    df["Age "] = pd.to_numeric(df["Age "], errors='coerce')
    df_clean = df[(df["Age "].between(18, 70)) & (df['Type de donation'] != 'NAN')]
    
    # Calculer l'âge moyen par type de donation et sexe
    age_mean = df_clean.groupby(['Type de donation', 'Sexe'])["Age "].mean().reset_index()
    
    fig = px.bar(age_mean, 
                x='Type de donation', 
                y="Age ", 
                color='Sexe',
                title='Âge moyen par type de donation et sexe',
                barmode='group',
                color_discrete_map={'M': 'blue', 'F': 'pink'})
    
    fig.update_layout(
        xaxis_title='Type de donation',
        yaxis_title='Âge moyen',
        legend_title='Sexe',
        height=500,
        width=800,
        xaxis=dict(
            ticktext=['Don de sang total', 'Don de plasma/plaquettes'],
            tickvals=['F', 'B']
        )
    )
    
    # Ajouter les valeurs exactes au-dessus des barres
    for i in range(len(age_mean)):
        fig.add_annotation(
            x=age_mean.iloc[i]['Type de donation'],
            y=age_mean.iloc[i]["Age "],
            text=f"{age_mean.iloc[i]["Age "]:.1f}",
            showarrow=False,
            yshift=10,
            font=dict(size=12)
        )
    
    return fig

# Fonction pour afficher tous les graphiques dans un tableau de bord interactif
def display_dashboard(df_input):
    global df
    df = df_input.copy()
    
    # Créer les graphiques
    fig1 = plot_distribution_sexe()
    fig2 = plot_distribution_groupe_sanguin()
    fig3 = plot_pyramide_ages()
    fig4 = plot_donation_par_groupe()
    fig5 = plot_distribution_phenotypes()
    fig6 = plot_age_moyen_donation_sexe()
    
    # Afficher les graphiques
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()
    fig5.show()
    fig6.show()

# Exemple d'utilisation:
display_dashboard(df)