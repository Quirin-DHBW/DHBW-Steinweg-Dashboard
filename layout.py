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

            return html_layout


class BetrachterLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout(self, df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig):
        return self.layout_function(df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig)
    

class PowerUserLayout(BasicLayout):
    def __init__(self, user_data):
        super().__init__(user_data)

    def layout(self, df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig):
        return self.layout_function(df, total_ist, total_budget, abweichung, abweichung_farbe, default_figure, kostenart_fig)