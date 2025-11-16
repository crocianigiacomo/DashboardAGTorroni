import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px

# Lettura dati csv necessari
meteo2024 = pd.read_csv("DashboardAGTorroni\data\meteo2024.csv")
prezziCereali = pd.read_csv("DashboardAGTorroni\data\PREZZI_CEREALI.csv")
produzione = pd.read_csv("DashboardAGTorroni\data\production_data.csv")
vendita = pd.read_csv("DashboardAGTorroni\data\sales_data.csv")


# Inizializare Dashboard
dashboard = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Dashboard layout

dashboard.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Torroni Interactive Dashboard",
                        className = "dashboard-title text-center text-primary mb-4"
                    ),
                    width=12
                )
            ]
        ),
        dbc.Row(
            [
                # Selzionatore data
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.DatePickerRange(
                                            id="date-picker",
                                            start_date = meteo2024["DATA"].min(),
                                            end_date = meteo2024["DATA"].max(),
                                            display_format = "DD/MM/YYYY",
                                            className= "d-flex justify-content aling-items-center rounded p-2 bg-light"
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    width = 4,
                ),
                # Totale vendite
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Totale vendite", className="Titolo-vendite"),
                                        html.H2(
                                            f"{vendita["SalesVolume"].sum():,}",
                                            className="testo-vendite"
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    width=4
                ),
                # Totale prodotto
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Totale volume prodotto", className="tot-title"),
                                        html.H2(f"{produzione["ProductionVolume"].sum():,}", className="tot-text")
                                    ]
                                )
                            ]
                        )
                    ],
                    width=4
                )
            ]
        )
    ]
)





if __name__ == "__main__":
    dashboard.run()