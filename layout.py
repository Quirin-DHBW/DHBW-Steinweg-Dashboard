import dash
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


class BasicLayout:
    def __init__(self, user_data,):
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
        html_layout = html.Div([
                        html.H1("Dashboard zur Kostenüberwachung"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Gesamtkosten", style={"textAlign": "center"}),
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
                                html.H3("Gesamtbudget", style={"textAlign": "center"}),
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
                                html.H3("Abweichung", style={"textAlign": "center"}),
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
                            }),
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
                        style={"marginBottom": "20px", "width": "60%"}),

                        dcc.Graph(id="kostenart_fig", figure=kostenart_fig)
                    ])

        return html_layout


class BetrachterLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, 
                        df,
                        totals_container,
                        default_figure,
                        kostenart_fig):
        if self.user_data["username"] == "Andreas.Auditor@Firma.p":
            html_layout= html.Div([
                        html.H1("Dashboard zur für die Auditoren"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Gesamtkosten", style={"textAlign": "center"}),
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
                                html.H3("Gesamtbudget", style={"textAlign": "center"}),
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
                                html.H3("Abweichung", style={"textAlign": "center"}),
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
                            }),
                        ], style={
                            "display": "flex",
                            "gap": "20px",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),

                        
                        html.H2("Trendanalyse – Entwicklung der Gesamtkosten"),
                        dcc.Graph(id="trend-diagramm", figure=default_figure),    

                        html.Hr(),

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
                        style={"marginBottom": "20px", "width": "60%"}),

                        dcc.Graph(id="kostenart_fig", figure=kostenart_fig)
                    ])
        
            
        elif self.user_data["username"] == "Franziska.Fachabteilung@Firma.p":
            eigene_abteilung = "Produktion"


            html_layout= html.Div([
                        html.H1("Dashboard für Produktionsabteilung"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
                         html.Div([
                            html.Div([
                                html.H3("Abteilungskosten", style={"textAlign": "center",}),
                                html.P(f"{totals_container['total_ist']:,.2f} €", style={"textAlign": "center", "margin": "0"}),
                                html.P(f"Letztes Jahr: {totals_container['total_ist_last_year']:,.2f} € ({totals_container['percent_change_ist']:,.1f}%)", style={"textAlign": "center", "margin": "0"})
                            ], style={
                                "padding": "10px",
                                "border": "1px solid #ccc",
                                "flex": "1",
                                "display": "flex",
                                "flexDirection": "column",
                                "justifyContent": "center",
                                "fontSize": "20px"
                            }),
                            
                            html.Div([
                                html.H3("Budget", style={"textAlign": "center"}),
                                html.P(f"{totals_container['total_budget']:,.2f} €", style={"textAlign": "center", "margin": "0"}),
                                html.P(f"Letztes Jahr: {totals_container['total_budget_last_year']:,.2f} € ({totals_container['percent_change_budget']:,.1f}%)", style={"textAlign": "center", "margin": "0"})
                            ], style={
                                "padding": "10px",
                                "border": "1px solid #ccc",
                                "flex": "1",
                                "display": "flex",
                                "flexDirection": "column",
                                "justifyContent": "center",
                                "fontSize": "20px"
                            }),
                            
                            html.Div([
                                html.H3("Abweichung", style={"textAlign": "center"}),
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
                                "justifyContent": "center",
                                "fontSize": "20px"
                            }),
                        ], style={
                            "display": "flex",
                            "gap": "20px",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),

                        html.H2("Kostenverlauf ihrer Abteilung"),
                        dcc.Graph(id="trend-diagramm", figure=default_figure),    

                        html.Hr(),

                        html.Div([
                            # Unsichtbarer Abteilungs-Dropdown (für feste Vorauswahl)
                            dcc.Dropdown(
                                options=[{"label": "Produktion", "value": "Produktion"}],
                                value="Produktion",
                                id="filter-abteilung",
                                style={"display": "none"}
                            ),

                            html.Div([
                                html.Label("Kostenart auswählen:", style={ "marginBottom": "5px","fontWeight": "bold"}),
                                dcc.Dropdown(
                                    options=[{"label": ka, "value": ka} for ka in sorted(df["Kostenart"].unique())],
                                    value=None,
                                    id="filter-kostenart",
                                    placeholder="Alle Kostenarten",
                                    style={"width": "200px","height": "38px", "fontSize": "14px"}
                                )
                            ], style={"display":"flex", 
                                      "flexDirection":"column",
                                      "marginRight": "30px",
                                      "justifyContent": "flex-end"
                                      }),

                            html.Div([
                                html.Label("Zeitraum wählen:", style={"marginBottom": "5px", "fontWeight": "bold"}),
                                dcc.DatePickerRange(
                                    id="filter-zeitraum",
                                    start_date=df["Monat"].min(),
                                    end_date=df["Monat"].max(),
                                    display_format="YYYY-MM",
                                    style={"height": "38px", "fontSize": "14px"}
                                )
                                ], style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "flex-end"
                                    })
                        ],
                        style={
                          "display": "flex",
                          "flexDirection": "row",
                          "alignItems": "flex-end",
                          "gap": "30px",
                          "marginLeft": "20px",
                          "marginBottom": "30px"
                        }),

                        dcc.Graph(id="kostenart_fig", figure=kostenart_fig)
                    ])
        return html_layout
    

class PowerUserLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, 
                        df,
                        totals_container,
                        default_figure,
                        kostenart_fig):
        return self.layout_function(df,
                                    totals_container,
                                    default_figure,
                                    kostenart_fig)
    
    