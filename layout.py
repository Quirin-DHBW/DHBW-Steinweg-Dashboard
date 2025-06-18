import dash
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


class BasicLayout:
    def __init__(self, user_data,):
        self.user_data = user_data

    def layout_function(self, 
                        df,
                        total_ist,
                        total_budget,
                        abweichung,
                        abweichung_farbe,
                        default_figure,
                        kostenart_fig):            
        html_layout = html.Div([
                        html.H1("Dashboard zur Kostenüberwachung"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
                        # Trendanalyse
                        html.Div([
                            html.Div([
                                html.H3("Gesamtkosten", style={"textAlign": "center"}),
                                html.P(f"{total_ist:,.2f} €", style={"textAlign": "center", "margin": "0"})
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
                                html.P(f"{total_budget:,.2f} €", style={"textAlign": "center", "margin": "0"})
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
                                html.P(f"{abweichung:,.2f} €", style={
                                    "textAlign": "center",
                                    "color": abweichung_farbe,
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
                        # Hier wird das Diagramm für die Gesamtkosten angezeigt

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

                        dcc.Graph(figure=kostenart_fig)
                    ])

        return html_layout


class BetrachterLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig):
        if self.user_data["username"] == "Andreas.Auditor@Firma.p":
            html_layout= html.Div([
                        html.H1("Dashboard zur für die Auditoren"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
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

                        dcc.Graph(figure=kostenart_fig)
                    ])
        
            
        elif self.user_data["username"] == "Franziska.Fachabteilung@Firma.p":
            eigene_abteilung = "Produktion"


            html_layout= html.Div([
                        html.H1("Dashboard für Produktionsabteilung"),
                        html.H2(f"Willkommen, {self.user_data['username']}!"),
                        
                        html.Div([
                            html.Div([
                                html.H3("Ihre Abteilungskosten"),
                                html.P(f"{total_ist:,.2f} €")
                            ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
                            
                            html.Div([
                                html.H3("Budget"),
                                html.P(f"{total_budget:,.2f} €")
                            ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
                            
                            html.Div([
                                html.H3("Abweichung"),
                                html.P(f"{abweichung:,.2f} €", style={"color": abweichung_farbe})
                            ], style={"padding": "10px", "border": "1px solid #ccc", "width": "25%"}),
                        ], style={"display": "flex", "gap": "20px"}),
                        
                        html.H2("Kostenverlauf ihrer Abteilung"),
                        dcc.Graph(id="trend-diagramm", figure=default_figure),    

                        html.Hr(),
                        html.Div([
                            # Kein sichtbares Abteilungs-Dropdown, aber Standardwert gesetzt
                            dcc.Dropdown(
                                options=[{"label": "Produktion", "value": "Produktion"}],
                                value="Produktion",
                                id="filter-abteilung",
                                style={"display": "none"}  # Versteckt im Layout
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

                        dcc.Graph(figure=kostenart_fig)
                    ])
        return html_layout
    

class PowerUserLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout_function(self, df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig):
        return self.layout_function(df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig)
    
    