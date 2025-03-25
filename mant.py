
import dash
import dash_mantine_components as dmc
from dash import Input, Output,html

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dmc.Button(
            "Cliquez-moi",
            id="button-1",  # ID du bouton
            variant="filled",
            color="blue",  # Couleur initiale
            size="lg",
        ),
        html.Div(id="output-div"),  # Pour afficher un texte après le clic
    ]
)

@app.callback(
    Output("button-1", "color"),
    Input("button-1", "n_clicks"),
    prevent_initial_call=True
)
def change_button_color(n_clicks):
    if n_clicks is None:
        return "blue"  # Couleur initiale avant tout clic
    return "green"  # Couleur après le clic

if __name__ == "__main__":
    app.run(debug=True)
