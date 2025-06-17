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

# Beispielhafte Daten laden
df = pd.read_csv("data/kosten.csv")
df["Monat"] = pd.to_datetime(df["Monat"])

conn = sqlite3.connect("einzelkonten.db")
df_db = pd.read_sql_table("buchungssaetze", conn)

# Beispielhafte Visualisierung
kostenart_fig = px.bar(df, x="Kostenart", y="Ist", color="Abteilung", barmode="group")

# === KPI-Berechnungen ===
total_ist = df["Ist"].sum()
total_budget = df["Budget"].sum()
abweichung = total_ist - total_budget
abweichung_farbe = "green" if abweichung <= 0 else "red"


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
## DYNAMIC LAYOUR GENERATION #####
##################################

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
        layout_obj = layout.BetrachterLayout(user_data)
    case "Sigrid.Systemadmin@Firma.p":
        layout_obj = layout.BasicLayout(user_data)
    case _:
        layout_obj = layout.BasicLayout(user_data)

custom_layout = layout_obj.layout_function(df,
                                           total_ist,
                                           total_budget,
                                           abweichung,
                                           abweichung_farbe,
                                           default_figure,
                                           kostenart_fig)


################
## APP RUN #####
################

app.layout = custom_layout

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

