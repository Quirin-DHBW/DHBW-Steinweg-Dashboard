import sys, os
os.chdir(os.path.dirname(sys.argv[0]))

import sqlite3

import pandas as pd

import dash
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_auth

import layout


##########################
## INITIAL APP SETUP #####
##########################

# Dashboard Konfigurationswahl (nach Benutzer)
USER_CONFIGURATION_SELECTION = {
    "Daniela.Düsentrieb@Firma.p" : "Entwickleransicht",
    "Sven.Schau@Firma.p" : "Betrachteransicht",
    "Ludwig.Leistung@Firma.p" : "Poweruseransicht",
    "Connie.Controlling@Fimrma.p" : "Poweruseransicht",
    "Gertholt.Geschäftsführung@Firma.p" : "Poweruseransicht",
    "Andreas.Auditor@Firma.p" : "Betrachteransicht",
    "Franziska.Fachabteilung@Firma.p" : "Betrachteransicht",
    "Sigrid.Systemadmin@Firma.p" : "Entwickleransicht",
}

user_data = {
    "username": "",
    "password": "",
    "configuration": "",
    "is_logged_in": False
}

def auth_function(username, password):
    global user_data
    if user_data["is_logged_in"]: # No need to re-authenticate if already logged in
        #print(user_data)
        print("Layout update...", end="\r")
        return True
    
    elif username in USER_CONFIGURATION_SELECTION.keys() and password == USER_CONFIGURATION_SELECTION[username]:
        print(f"Benutzer {username} authentifiziert mit Konfiguration: {USER_CONFIGURATION_SELECTION[username]}")

        user_data["username"] = username
        user_data["password"] = password
        user_data["configuration"] = USER_CONFIGURATION_SELECTION[username]
        user_data["is_logged_in"] = True

        print(user_data)

        return True
    
    else:
        return False


app = Dash(__name__)
server = app.server  # Für Deployment

auth = dash_auth.BasicAuth(
    app,
    auth_func=auth_function,
    secret_key="iamaverysecretkeyyandiamcoolandyoudontknowiexistyesyes" # Placeholder to silence a warning, as no Flask App exists yet
)


##############################
## DATA LOADING AND PREP #####
##############################

# load DB into dataframe
query = """
SELECT 
    b.buchungs_id,
    b.konto as Einzelkontonummer,
    b.fachbereich as Abteilung,
    a.abteilung,
    a.budget as Budget,
    a.year as Jahr,
    b.bezeichnung as Kostenart,
    b.kategorie as Kategorie,
    b.buchungsdatum,
    b.betrag as Ist
FROM 
    buchungssaetze b
JOIN 
    abteilungen a 
ON 
    b.fachbereich = a.abteilung
"""

conn = sqlite3.connect("data/einzelkonten.db")

df = pd.read_sql_query(query, conn)
df["buchungsdatum"] = pd.to_datetime(df["buchungsdatum"])
df["Monat"] = df["buchungsdatum"].dt.to_period("M").dt.to_timestamp()

conn.close()

# monthly plan/actual
df_kpi_aggregation = df.groupby(["Abteilung", "Kategorie", "Monat", "Jahr"]).agg(
    ist_summe=("Ist", "sum"),
    budget_summe=("Budget", "first")
).reset_index()

# plan/actual comparison
df_kpi_diff = df_kpi_aggregation.copy()
df_kpi_diff["abweichung"] = df_kpi_diff["ist_summe"] - df_kpi_diff["budget_summe"]
df_kpi_diff["budgetüberschreitung"] = df_kpi_diff["abweichung"] > 0

# raw, for drilldowns
df_accounts = df[[
    "buchungs_id", "Abteilung", "Einzelkontonummer", "Kostenart",
    "Kategorie", "buchungsdatum", "Monat", "Ist", "Budget", "Jahr"
]]

# === total KPIs (adjustable year) - for initial functionality ===
current_year = 2024
df_year = df[df["Jahr"] == current_year]

total_ist = df_year["Ist"].sum()
total_budget = df_year.drop_duplicates(subset=["Abteilung", "Jahr"])["Budget"].sum()
abweichung = total_budget - total_ist
abweichung_farbe = "green" if abweichung >= 0 else "red"

# ye olde kostenart_fig, now with new dataset :3
kostenart_fig = px.bar(
    df_kpi_aggregation[df_kpi_aggregation["Jahr"] == current_year],
    x="Kategorie",
    y="ist_summe",
    color="Abteilung",
    barmode="group",
    title="Kostenarten nach Abteilung (Ist-Werte)"
)

#################################
## DYNAMIC GRAPH GENERATION #####
#################################

def get_trend_fig(abteilung=None, kostenart=None, start=None, end=None):
    print("Figure being updated with:", abteilung, kostenart, start, end)

    global df
    df_filtered = df.copy(deep=True)

    #print(df_filtered.head(50))

    try:
        if abteilung != None:
            #print("CHECKING ABTEILUNG")
            df_filtered = df_filtered[df_filtered["Abteilung"] == abteilung]

        if kostenart != None:
            #print("CHECKING KOSTENART")
            df_filtered = df_filtered[df_filtered["Kostenart"] == kostenart]

        df_filtered = df_filtered[
            (df_filtered["Monat"] >= pd.to_datetime(start)) &
            (df_filtered["Monat"] <= pd.to_datetime(end))
        ]

        df_output = df_filtered.groupby("Monat")[["Ist", "Budget"]].sum().reset_index()

        #print(df_output.head(50))
    except Exception as e:
        print("EXCEPTION TRIGGERED, DISPLAYING DEFAULT GRAPH\n", e)
        df_output = df

    fig = px.line(df_output,
                  x="Monat",
                  y=["Ist", "Budget"],
                  markers=True,
                  title="Kostenentwicklung über Zeit",
                  labels={"value": "Euro", "variable": "Kategorie"})
    
    fig.update_layout()

    return fig


default_figure = get_trend_fig()


##################################
## DYNAMIC LAYOUT GENERATION #####
##################################

def gen_layout():
    global default_figure
    global total_ist
    global total_budget
    global abweichung
    global kostenart_fig
    if user_data["is_logged_in"]:
        match user_data["username"]:
            case "Daniela.Düsentrieb@Firma.p":
                layout_obj = layout.BasicLayout(user_data)
            case "Sven.Schau@Firma.p":
                layout_obj = layout.BetrachterLayout(user_data)
            case "Ludwig.Leistung@Firma.p":
                layout_obj = layout.PowerUserLayout(user_data)
            case "Connie.Controlling@Firma.p":
                layout_obj = layout.PowerUserLayout(user_data)
            case "Gertholt.Geschäftsführung@Firma.p":
                layout_obj = layout.PowerUserLayout(user_data)
            case "Andreas.Auditor@Firma.p":
                layout_obj = layout.BetrachterLayout(user_data)
            case "Franziska.Fachabteilung@Firma.p":
                default_figure = get_trend_fig(abteilung="Produktion")
                #total_ist für currrent year
                df_year = df[df["Jahr"] == current_year]
                total_ist    = df_year[df_year["Abteilung"] == "Produktion"]["Ist"].sum()
                total_budget = df_year[df_year["Abteilung"] == "Produktion"].drop_duplicates(subset=["Abteilung", "Jahr"])["Budget"].sum()
                abweichung =  total_budget - total_ist
                layout_obj = layout.BetrachterLayout(user_data)
                kostenart_fig = px.bar(
                    df_kpi_aggregation[
                    (df_kpi_aggregation["Jahr"] == current_year) &
                    (df_kpi_aggregation["Abteilung"] == "Produktion")
                    ],
                    x="Kategorie",
                    y="ist_summe",
                    barmode="group",
                    title="Kostenarten für Produktion (Ist-Werte)"
                )
            case "Sigrid.Systemadmin@Firma.p":
                layout_obj = layout.BasicLayout(user_data)
            case _:
                layout_obj = layout.BasicLayout(user_data)


        print(layout_obj.user_data)

        custom_layout = layout_obj.layout_function(df,
                                                total_ist,
                                                total_budget,
                                                abweichung,
                                                abweichung_farbe,
                                                default_figure,
                                                kostenart_fig)
        
        return custom_layout
    else:
        print("No user data found, using default layout")
        custom_layout = layout.BasicLayout(user_data).layout_function(
            df,
            total_ist,
            total_budget,
            abweichung,
            abweichung_farbe,
            default_figure,
            kostenart_fig
        )
        return custom_layout


################
## APP RUN #####
################

app.layout = gen_layout

app.callback(
        Output("trend-diagramm", "figure"),
        Input("filter-abteilung", "value"),
        Input("filter-kostenart", "value"),
        Input("filter-zeitraum", "start_date"),
        Input("filter-zeitraum", "end_date")
    )(lambda abteilung, kostenart, start, end: get_trend_fig(abteilung, kostenart, start, end))


if __name__ == "__main__":
    app.run(debug=True)

# go to 
# http://127.0.0.1:8050/
# to see dashboard

