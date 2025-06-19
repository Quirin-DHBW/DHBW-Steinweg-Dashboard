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
    a.year,
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
    AND strftime('%Y', b.buchungsdatum) = CAST(a.year AS TEXT)
"""

conn = sqlite3.connect("data/einzelkonten.db")

df = pd.read_sql_query(query, conn)
df["buchungsdatum"] = pd.to_datetime(df["buchungsdatum"])
df["Monat"] = df["buchungsdatum"].dt.to_period("M").dt.to_timestamp()
df["Jahr"] = df["buchungsdatum"].dt.year
df["Monatsbudget"] = df["Budget"] / 12

conn.close()


# monthly plan/actual
df_kpi_aggregation = df.groupby(["Abteilung", "Kostenart", "Monat", "Jahr"]).agg(
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
    "Kategorie", "buchungsdatum", "Monat", "Ist", "Monatsbudget", "Budget", "Jahr"
]]

current_year = 2024

# === total KPIs (adjustable year) - for initial functionality ===
def get_total_kpis(df, current_year=2024, abteilung=None):
    df = df.copy(deep=True)

    if abteilung is not None:
        df = df[df["Abteilung"] == abteilung]

    df_year = df[df["Jahr"] == current_year]
    df_last_year = df[df["Jahr"] == current_year - 1]

    total_ist = df_year["Ist"].sum()
    total_budget = df_year.drop_duplicates(subset=["Abteilung", "Jahr"])["Budget"].sum()
    abweichung = total_budget - total_ist
    abweichung_farbe = "green" if abweichung >= 0 else "red"

    total_ist_last_year = df_last_year["Ist"].sum()
    total_budget_last_year = df_last_year.drop_duplicates(subset=["Abteilung", "Jahr"])["Budget"].sum()
    abweichung_last_year = total_budget - total_ist
    abweichung_farbe_last_year = "green" if abweichung >= 0 else "red"

    percent_change_ist = (total_ist / total_ist_last_year) * 100
    percent_change_budget = (total_budget / total_budget_last_year) * 100
    percent_change_abweichung = (abweichung / abweichung_last_year) * 100

    totals_container = {
        "total_ist": total_ist,
        "total_budget": total_budget,
        "abweichung": abweichung,
        "abweichung_farbe": abweichung_farbe,
        "total_ist_last_year": total_ist_last_year,
        "total_budget_last_year": total_budget_last_year,
        "abweichung_last_year": abweichung_last_year,
        "abweichung_farbe_last_year": abweichung_farbe_last_year,
        "percent_change_ist": percent_change_ist,
        "percent_change_budget": percent_change_budget,
        "percent_change_abweichung": percent_change_abweichung
    }

    return totals_container


totals_container = get_total_kpis(df, current_year=current_year)


# ye olde kostenart_fig, now with new dataset :3
kostenart_fig = px.bar(
    df_kpi_aggregation[df_kpi_aggregation["Jahr"] == current_year],
    x="Kostenart",
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

    global df_accounts
    df_filtered = df_accounts.copy(deep=True)

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

        df_output = df_filtered.groupby("Monat").agg({
            "Ist": "sum",
            "Monatsbudget": "first"
        }).reset_index()


        #print(df_output.head(50))
    except Exception as e:
        print("EXCEPTION TRIGGERED, DISPLAYING DEFAULT GRAPH\n", e)
        df_output = df

    fig = px.line(df_output,
                  x="Monat",
                  y=["Ist", "Monatsbudget"],
                  markers=True,
                  title="Kostenentwicklung über Zeit",
                  labels={"value": "Euro", "variable": "Kategorie"})
    
    fig.update_layout()

    return fig


def get_kostenart_fig(abteilung=None, kostenart=None, jahr=None):
    global df_kpi_aggregation
    df_filtered = df_kpi_aggregation.copy(deep=True)

    if abteilung != None:
        df_filtered = df_filtered[df_filtered["Abteilung"] == abteilung]
    if kostenart != None:
        df_filtered = df_filtered[df_filtered["Kostenart"] == kostenart]
    if jahr != None:
        df_filtered = df_filtered[df_filtered["Jahr"] == jahr]
    

    fig = px.bar(
        df_filtered,
        x="Kostenart",
        y="ist_summe",
        color="Abteilung",
        barmode="group",
        title=f"Kostenarten{' für ' + abteilung if abteilung != None else ''} (Ist-Werte)"
    )

    return fig


default_figure = get_trend_fig()
kostenart_fig = get_kostenart_fig(abteilung=None, kostenart=None, jahr=current_year)


##################################
## DYNAMIC LAYOUT GENERATION #####
##################################

def gen_layout():
    global default_figure
    global totals_container
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
                layout_obj = layout.BetrachterLayout(user_data)
                default_figure = get_trend_fig(abteilung="Produktion")
                #total_ist für currrent year
                totals_container = get_total_kpis(df, current_year=current_year, abteilung="Produktion")
                kostenart_fig = get_kostenart_fig(abteilung="Produktion", jahr=current_year)
            case "Sigrid.Systemadmin@Firma.p":
                layout_obj = layout.BasicLayout(user_data)
            case _:
                layout_obj = layout.BasicLayout(user_data)


        print(layout_obj.user_data)

        custom_layout = layout_obj.layout_function(df,
                                                   totals_container,
                                                   default_figure,
                                                   kostenart_fig)
        
        return custom_layout
    else:
        print("No user data found, using default layout")
        custom_layout = layout.BasicLayout(user_data).layout_function(
            df,
            totals_container,
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

app.callback(
        Output("kostenart_fig", "figure"),
        Input("filter-abteilung", "value"),
        Input("filter-kostenart", "value"),
        Input("filter-zeitraum", "end_date")
    )(lambda abteilung, kostenart, end: get_kostenart_fig(abteilung, kostenart, pd.to_datetime(end).year if end else None))


if __name__ == "__main__":
    app.run(debug=True)

# go to 
# http://127.0.0.1:8050/
# to see dashboard

