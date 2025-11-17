import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px

# Lettura dati csv
meteo2024 = pd.read_csv("data/meteo2024.csv")
meteo2024["DATA"] = pd.to_datetime(meteo2024["DATA"])

prezziCereali = pd.read_csv("data/PREZZI_CEREALI.csv",sep=";")
produzione = pd.read_csv("data/production_data.csv",sep=",")
vendita = pd.read_csv("data/sales_data.csv",sep=",")
ettari = pd.read_csv("data/CEREALI_TERRENO_PRODUZIONE.csv", sep=";")

cereal_order = ["MEDICA", "COLZA", "FRUMENTO TENERO", "FRUMENTO DURO", "ORZO", "GIRASOLE", "MAIS"]

colormap = {
    "MEDICA": "#636EFA",
    "COLZA": "#EF553B",
    "FRUMENTO TENERO": "#00CC96",
    "FRUMENTO DURO": "#AB63FA",
    "ORZO": "#FFA15A",
    "GIRASOLE": "#19D3F3",
    "MAIS": "#FF6692"
}

df_gain = vendita.groupby("Prodotto")["Gain"].sum().reset_index().round()
df = ettari.merge(df_gain, left_on="CEREALE", right_on="Prodotto", how="left")
df["€ per ETTARO"] = (df["Gain"] / df["ETTARI_TERRENO"]).round()

fig_land = px.bar(
    df,
    x="CEREALE",
    y="€ per ETTARO",
    labels={"CEREALE": "Tipo di cereale", "€ per ETTARO": "Guadagno (€) per ettaro"},
    color="CEREALE",color_discrete_map=colormap,
    category_orders={"CEREALE": cereal_order},
    text="€ per ETTARO"
    )

fig_cereal = px.bar(
    df_gain,
    x="Prodotto",
    y="Gain",
    labels={"Prodotto": "Tipo di cereale","Gain": "Guadagno totale (€)"},
    color="Prodotto",
    color_discrete_map=colormap,
    category_orders={"Prodotto": cereal_order},
    text="Gain"
    )

# Inizializza Dashboard
dashboard = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.MINTY,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
])

# Layout
dashboard.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Torroni Interactive Dashboard",
                    className="dashboard-title text-center text-primary mb-4 p-4"
                ),
                width=12
            )
        ),
        dbc.Row(
            [
                # Selezionatore data
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H5(
                                    [
                                        html.I(className="fas fa-calendar text-primary"),
                                        " Seleziona Periodo"
                                    ]
                                ),
                                className="bg-dark text-primary text-center"
                            ),
                            dbc.CardBody(
                                html.Div(
                                    dcc.DatePickerRange(
                                        id="date-picker",
                                        start_date=meteo2024["DATA"].min(),
                                        end_date=meteo2024["DATA"].max(),
                                        display_format="DD/MM/YYYY",
                                    ),
                                    className="d-flex justify-content-center align-items-center",
                                    style={"min-height": "100px"}
                                ),
                                className="p-0"
                            ),
                            dbc.CardFooter(
                                dbc.Button(
                                    "Reset Data",
                                    id="reset-date-btn",
                                    color="primary",
                                    className="w-100"
                                )
                            )
                        ],
                        className="shadow h-100 border border-primary border-4 p-1"
                    ),
                    width=4,
                    className="mb-2"
                ),
                # Totale vendite
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                html.Div(
                                    [
                                        html.I(className="fas fa-shopping-cart fa-2x text-success mb-2"),
                                        html.H5("Totale vendite", className="text-muted mb-3"),
                                        html.H2(
                                            id="totale-vendite",
                                            className="text-primary fw-bold mb-0"
                                        )
                                    ],
                                    className="text-center"
                                ),
                                className="py-4"
                            ),
                            dbc.CardFooter(
                                dcc.Dropdown(
                                    id="select-product-sold",
                                    options=[
                                        {"label": "TUTTI", "value": "TUTTI"},
                                        {"label": "ORZO", "value": "ORZO"},
                                        {"label": "MEDICA", "value": "MEDICA"},
                                        {"label": "COLZA", "value": "COLZA"},
                                        {"label": "FRUMENTO TENERO", "value": "FRUMENTO TENERO"},
                                        {"label": "FRUMENTO DURO", "value": "FRUMENTO DURO"},
                                        {"label": "GIRASOLE", "value": "GIRASOLE"},
                                        {"label": "MAIS", "value": "MAIS"},
                                    ],
                                    value="TUTTI",
                                    clearable=False,
                                    className=" w-100"                                    
                                )
                            )
                        ],
                        className="shadow h-100 border border-success border-4 p-1"
                    ),
                    width=4,
                    className="mb-2"
                ),
                # Totale prodotto
                dbc.Col(
                    dbc.Card(
                        [
                        dbc.CardBody(
                            html.Div(
                                [
                                    html.I(className="fas fa-industry fa-2x text-info mb-2"),
                                    html.H5("Volume Prodotto", className="text-muted mb-3"),
                                    html.H2(
                                        id="tot-produzione",
                                        className="text-info fw-bold mb-0"
                                    )
                                ],
                                className="text-center"
                            ),
                            className="py-4"
                        ),
                        dbc.CardFooter(
                                dcc.Dropdown(
                                    id="select-product-produced",
                                    options=[
                                        {"label": "TUTTI", "value": "TUTTI"},
                                        {"label": "ORZO", "value": "ORZO"},
                                        {"label": "MEDICA", "value": "MEDICA"},
                                        {"label": "COLZA", "value": "COLZA"},
                                        {"label": "FRUMENTO TENERO", "value": "FRUMENTO TENERO"},
                                        {"label": "FRUMENTO DURO", "value": "FRUMENTO DURO"},
                                        {"label": "GIRASOLE", "value": "GIRASOLE"},
                                        {"label": "MAIS", "value": "MAIS"},
                                    ],
                                    value="TUTTI",
                                    clearable=False,
                                    className=" w-100"
                                )
                            )
                        ],
                        className="shadow h-100 border border-info border-4 p-1"
                    ),
                    width=4,
                    className="mb-2"
                )
            ]
        ),
        dbc.Row([], style={"height": "25px"}),

        # SEZIONE METEO
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H2("Condizioni Meteo",className="mb-0 text-center"),
                            className="bg-info text-white "
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5(
                                                [
                                                    html.I(className="fas fa-temperature-half text-info mb-3"),
                                                    " Temperature"
                                                ],
                                                className="text-center"
                                            ),
                                            dcc.Graph(id="temperature-graph", style={"height": "300px"})
                                        ],
                                        xs=12, md=4
                                    ),
                                    dbc.Col(
                                        [
                                            html.H5(
                                                [
                                                    html.I(className="fas fa-droplet text-info mb-3"),
                                                    " Umidità"
                                                ],
                                                className="text-center"
                                            ),
                                            dcc.Graph(id="humidity-graph", style={"height": "300px"})
                                        ],
                                        xs=12, md=4, className="shadow h-100 border-start border-info border-4"
                                    ),
                                    dbc.Col(
                                        [
                                            html.H5(
                                                [
                                                    html.I(className="fas fa-cloud-rain text-info mb-3"),
                                                    " Fenomeni atmosferici"
                                                ],
                                                className="text-center"
                                            ),
                                            dcc.Graph(id="rain-graph", style={"height": "300px"})
                                        ],
                                        xs=12, md=4, className="shadow h-100 border-start border-info border-4"
                                    )
                                ]
                            ),
                            className="p-2"
                        )
                    ],
                    className="shadow h-100 border border-info border-4 p-1"
                ),
                width=12,
                className="mb-3"
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(                            
                            html.H2(
                                [
                                    html.I(className="fas fa-arrow-trend-up text-white"),
                                    " Prestazioni"
                                ],
                                className="text-center bg-primary text-white p-2 m-0 rounded-top"
                            ),
                            className="p-0"
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5(
                                                [
                                                    "Profitti per Area"
                                                ],
                                                className="text-center"
                                             ),
                                            dcc.Graph(figure=fig_land, style={"height": "335px"})
                                        ],
                                        xs=12, md=6
                                    ),
                                    dbc.Col(
                                        [
                                             html.H5(
                                                [
                                                    "Profitti per Cereale"
                                                ],
                                                className="text-center"
                                             ),
                                            dcc.Graph(figure=fig_cereal, style={"height": "335px"})
                                        ],
                                        xs=12, md=6, className="shadow h-100 border-start border-primary border-4"
                                    )
                                ]
                            ),
                            className="p-2"
                        )
                    ],
                    className="shadow h-100 border border-primary border-4 p-1"
                 ),
                 width=12,
                 className="mb-3"
            )
        )
    ],
    fluid=True, className= "bg-dark"
)

# CALLBACKS

@dashboard.callback(
    Output("date-picker", "start_date"),
    Output("date-picker", "end_date"),
    Input("reset-date-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_dates(n):
    return meteo2024["DATA"].min(), meteo2024["DATA"].max()

@dashboard.callback(
    Output("totale-vendite", "children"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("select-product-sold","value")
)
def aggiorna_totale_vendite(start_date, end_date,selected_product):
    # Filtraggio per date
    df = vendita[
        (vendita["Date"] >= start_date) &
        (vendita["Date"] <= end_date)
    ]

    # Filtraggio per prodotto
    if selected_product != "TUTTI":
        df = df[df["Prodotto"] == selected_product]

    totale = df["SalesVolume"].sum()

    return f"{totale:,} Q"

@dashboard.callback(
    Output("tot-produzione", "children"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("select-product-produced","value")
)

def aggiorna_totale_produzione(start_date, end_date, selected_product):

    # Filtra il dataframe in base al range selezionato
    df = produzione[
        (produzione["Date"] >= start_date) &
        (produzione["Date"] <= end_date)
    ]

    #Filtra per prodotto
    if selected_product != "TUTTI":
        df = df[df["Prodotto"] == selected_product]

    totale = df["ProductionVolume"].sum()

    return f"{totale:,} Q"

@dashboard.callback(
    Output("temperature-graph", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_temperature_graph(start_date, end_date):
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ]
    
    df_long = filtered_df.melt(
        id_vars=["DATA"],
        value_vars=["TMIN °C", "TMEDIA °C", "TMAX °C"],
        var_name="TIPO",
        value_name="TEMPERATURA"
    )
    
    df_long['TIPO'] = df_long['TIPO'].map({
        'TMIN °C': 'MIN',
        'TMEDIA °C': 'MEDIA',
        'TMAX °C': 'MAX'
    })
    
    fig = px.line(
        df_long,
        x="DATA",
        y="TEMPERATURA",
        color="TIPO",
        color_discrete_map={
            "MIN": "#17a2b8",
            "MEDIA": "#ffc107",
            "MAX": "#dc3545"
        },
        labels={'DATA': '', 'TEMPERATURA': '°C'}
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=20, t=20, b=40),
        hovermode='x unified',
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@dashboard.callback(
    Output("humidity-graph", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_humidity_graph(start_date, end_date):
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ]
    
    fig = px.histogram(
        filtered_df,
        x="UMIDITA %",
        nbins=30,
        color_discrete_sequence=['#17a2b8'],
        labels={'UMIDITA %': 'Umidità %'}
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=20, t=20, b=40)
    )
    
    return fig


@dashboard.callback(
    Output("rain-graph", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_rain_graph(start_date, end_date):
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ].copy()
    
    counts = (
        filtered_df.groupby("FENOMENI").size().reset_index(name="Giorni")
    )
    fig = px.pie(
        counts,
        names="FENOMENI",
        values="Giorni",
        color="FENOMENI",
        color_discrete_map={
            'pioggia': '#17a2b8',
            'nebbia': '#6c757d',
            'sole': '#ffc107',
        }
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=20, t=20, b=40),
        legend=dict(
            title=None,
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ),
    )
    
    return fig


if __name__ == "__main__":
    dashboard.run(debug=True)