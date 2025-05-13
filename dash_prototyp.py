import sys, os
os.chdir(os.path.dirname(sys.argv[0]))

import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)
server = app.server  # Für Deployment

# Beispielhafte Daten laden
df = pd.read_csv("data/kosten.csv")
df["Monat"] = pd.to_datetime(df["Monat"])

# Beispielhafte Visualisierung
fig = px.bar(df, x="Kostenart", y="Ist", color="Abteilung", barmode="group")

# === KPI-Berechnungen ===
total_ist = df["Ist"].sum()
total_budget = df["Budget"].sum()
abweichung = total_ist - total_budget
abweichung_farbe = "green" if abweichung <= 0 else "red"

# Gruppieren nach Monat
df_trend = df.groupby("Monat")[["Ist", "Budget"]].sum().reset_index()
# Zeitreihendiagramm
fig_trend = px.line(df_trend, x="Monat", y=["Ist", "Budget"],
                    markers=True, title="Kostenentwicklung über Zeit",
                    labels={"value": "Euro", "variable": "Kategorie"})

# Layout mit KPIs
app.layout = html.Div([
    html.H1("Dashboard zur Kostenüberwachung"),
    
    html.Div([
        html.Div([
            html.H3("Gesamtkosten"),
            html.P(f"{total_ist:,.2f} €")
        ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
        
        html.Div([
            html.H3("Gesamtbudget"),
            html.P(f"{total_budget:,.2f} €")
        ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
        
        html.Div([
            html.H3("Abweichung"),
            html.P(f"{abweichung:,.2f} €", style={"color": abweichung_farbe})
        ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
    ], style={"display": "flex", "gap": "20px"}),
    
    html.H2("Trendanalyse – Entwicklung der Gesamtkosten"),
    dcc.Graph(id="trend-diagramm", figure=fig_trend),    

    html.Hr(),

    dcc.Graph(figure=fig),

    html.Div([
        html.Label("Abteilung auswählen:"),
        dcc.Dropdown(
            options=[{"label": abt, "value": abt} for abt in sorted(df["Abteilung"].unique())],
            value=None,
            id="filter-abteilung",
            placeholder="Alle Abteilungen"
        ),
    
        html.Label("Kostenart auswählen:"),
        dcc.Dropdown(
            options=[{"label": ka, "value": ka} for ka in sorted(df["Kostenart"].unique())],
            value=None,
            id="filter-kostenart",
            placeholder="Alle Kostenarten"
        ),
    
        html.Label("Zeitraum wählen:"),
        dcc.DatePickerRange(
            id="filter-zeitraum",
            start_date=df["Monat"].min(),
            end_date=df["Monat"].max(),
            display_format="YYYY-MM"
        ),
    ], 
    style={"marginBottom": "20px", "width": "60%"})
])

if __name__ == "__main__":
    app.run(debug=True)

# go to 
# http://127.0.0.1:8050/
# to see dashboard


# callback
@app.callback(
    Output("trend-diagramm", "figure"),
    Input("filter-abteilung", "value"),
    Input("filter-kostenart", "value"),
    Input("filter-zeitraum", "start_date"),
    Input("filter-zeitraum", "end_date"),
)
def update_trend(abteilung, kostenart, start, end):
    df_filtered = df.copy(deep=True)

    if abteilung:
        df_filtered = df_filtered[df_filtered["Abteilung"] == abteilung]
    if kostenart:
        df_filtered = df_filtered[df_filtered["Kostenart"] == kostenart]

    df_filtered = df_filtered[
        (df_filtered["Monat"] >= pd.to_datetime(start)) &
        (df_filtered["Monat"] <= pd.to_datetime(end))
    ]

    df_trend = df_filtered.groupby("Monat")[["Ist", "Budget"]].sum().reset_index()

    fig = px.line(df_trend, x="Monat", y=["Ist", "Budget"],
                  markers=True, title="Kostenentwicklung über Zeit",
                  labels={"value": "Euro", "variable": "Kategorie"})

    return fig
