import dash
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


class BasicLayout:
    def __init__(self, user_data):
        self.user_data = user_data

    def layout_function(self,
                        df,
                        totals_container,
                        default_figure,
                        kostenart_fig,
                        headline="Dashboard zur Kostenüberwachung",
                        welcome_message=None,
                        abteilung_dropdown_visible=True,
                        abteilung_default_value=None,
                        abteilung_dropdown_options=None,
                        kostenart_label="Kostenart auswählen:",
                        ist_label="Gesamtkosten",
                        budget_label="Gesamtbudget",
                        abweichung_label="Abweichung",
                        trend_headline="Trendanalyse – Entwicklung der Gesamtkosten"):

        if welcome_message is None:
            welcome_message = f"Willkommen, {self.user_data['username']}!"
        if abteilung_dropdown_options is None:
            abteilung_dropdown_options = [{"label": abt, "value": abt} for abt in sorted(df["Abteilung"].unique())]

        abteilung_dropdown_style = {} if abteilung_dropdown_visible else {"display": "none"}

        return html.Div([
            html.H1(headline),
            html.H2(welcome_message),

            html.Div([
                html.Div([
                    html.H3(ist_label, style={"textAlign": "center"}),
                    html.P(f"{totals_container['total_ist']:,.2f} €", style={"textAlign": "center", "margin": "0"}),
                    html.P(f"Letztes Jahr: {totals_container['total_ist_last_year']:,.2f} € ({totals_container['percent_change_ist']:,.1f}%)", style={"textAlign": "center", "margin": "0"})
                ], style={
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "flex": "1",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center"
                }),

                html.Div([
                    html.H3(budget_label, style={"textAlign": "center"}),
                    html.P(f"{totals_container['total_budget']:,.2f} €", style={"textAlign": "center", "margin": "0"}),
                    html.P(f"Letztes Jahr: {totals_container['total_budget_last_year']:,.2f} € ({totals_container['percent_change_budget']:,.1f}%)", style={"textAlign": "center", "margin": "0"})
                ], style={
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "flex": "1",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center"
                }),

                html.Div([
                    html.H3(abweichung_label, style={"textAlign": "center"}),
                    html.P(f"{totals_container['abweichung']:,.2f} €", style={
                        "textAlign": "center",
                        "color": totals_container["abweichung_farbe"],
                        "margin": "0"
                    }),
                    html.P(f"Letztes Jahr: {totals_container['abweichung_last_year']:,.2f} € ({totals_container['percent_change_abweichung']:,.1f}%)", style={
                        "textAlign": "center",
                        "color": totals_container["abweichung_farbe_last_year"],
                        "margin": "0"
                    })
                ], style={
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "flex": "1",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center"
                })
            ], style={
                "display": "flex",
                "gap": "20px",
                "justifyContent": "space-between",
                "alignItems": "center"
            }),

            html.H2(trend_headline),
            dcc.Graph(id="trend-diagramm", figure=default_figure),

            html.Hr(),

            html.Div([
                dcc.Dropdown(
                    options=abteilung_dropdown_options,
                    value=abteilung_default_value,
                    id="filter-abteilung",
                    placeholder="Alle Abteilungen",
                    style={"width": "250px", **abteilung_dropdown_style}
                ),

                html.Div([
                    html.Label(kostenart_label, style={"marginBottom": "5px", "fontWeight": "bold"}),
                    dcc.Dropdown(
                        options=[{"label": ka, "value": ka} for ka in sorted(df["Kostenart"].unique())],
                        value=None,
                        id="filter-kostenart",
                        placeholder="Alle Kostenarten",
                        style={"width": "200px", "height": "38px", "fontSize": "14px"}
                    )
                ], style={"marginRight": "30px"}),

                html.Div([
                    html.Label("Zeitraum wählen:", style={"marginBottom": "5px", "fontWeight": "bold"}),
                    dcc.DatePickerRange(
                        id="filter-zeitraum",
                        start_date=df["Monat"].min(),
                        end_date=df["Monat"].max(),
                        display_format="YYYY-MM",
                        style={"height": "38px", "fontSize": "14px"}
                    )
                ])
            ], style={
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "flex-end",
                "gap": "30px",
                "marginLeft": "20px",
                "marginBottom": "30px"
            }),

            dcc.Graph(id="kostenart_fig", figure=kostenart_fig)
        ])


class BetrachterLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, df, totals_container, default_figure, kostenart_fig):
        user_name = self.user_data["username"]
        if user_name == "Andreas.Auditor@Firma.p":
            return super().layout_function(
                df, totals_container, default_figure, kostenart_fig,
                headline="Dashboard zur für die Auditoren",
                trend_headline="Trendanalyse – Entwicklung der Gesamtkosten"
            )
        elif user_name == "Franziska.Fachabteilung@Firma.p":
            return super().layout_function(
                df, totals_container, default_figure, kostenart_fig,
                headline="Dashboard für Produktionsabteilung",
                abteilung_dropdown_visible=False,
                abteilung_default_value="Produktion",
                ist_label="Abteilungskosten",
                trend_headline="Kostenverlauf ihrer Abteilung"
            )
        return super().layout_function(df, totals_container, default_figure, kostenart_fig)


class PowerUserLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, df, totals_container, default_figure, kostenart_fig):
        return super().layout_function(
            df, totals_container, default_figure, kostenart_fig,
            headline="Dashboard für Power-User",
            trend_headline="Trendanalyse – Entwicklung der Gesamtkosten"
        )
