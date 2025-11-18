import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px

# Lettura dati csv
meteo2024 = pd.read_csv("data/meteo2024.csv", sep=",")
prezziCereali = pd.read_csv("data/PREZZI_CEREALI.csv",sep=";")
produzione = pd.read_csv("data/production_data.csv",sep=",")
vendita = pd.read_csv("data/sales_data.csv",sep=",")
ettari = pd.read_csv("data/CEREALI_TERRENO_PRODUZIONE.csv", sep=";")

cereal_order = ["MEDICA", "COLZA", "FRUMENTO TENERO", "FRUMENTO DURO", "ORZO", "GIRASOLE", "MAIS"] # ORDINE PRESTABILITO CHE UTILIZZERO NEI GRAFICI DELLE PRESTAZIONI

# ASSEGNO COLORI AD OGNI CEREALE PER RENDERE PIÙ IMMEDIATA LETTURA I GRAFICI
colormap = {
    "MEDICA": "#636EFA",
    "COLZA": "#EF553B",
    "FRUMENTO TENERO": "#00CC96",
    "FRUMENTO DURO": "#AB63FA",
    "ORZO": "#FFA15A",
    "GIRASOLE": "#19D3F3",
    "MAIS": "#FF6692"
}

# CALCOLO IL GUADAGNO PER OGNI CEREALE E DI CONSEGUENZA CALCOLO IL GUADAGNO PER ETTARO COLTIVATO
df_gain = vendita.groupby("Prodotto")["Gain"].sum().reset_index().round() # GROUPBY PER SELEZIONARE OGNI CEREALE, SOMMO E ARROTONDO (NON MI INTERESSANO I CENTESIMI)
df = ettari.merge(df_gain, left_on="CEREALE", right_on="Prodotto", how="left") # PER IL CALCOLO DEL GUADAGNO PER ETTARO HO BISOGNO DI DUE CSV DI CONSEGUENZA FACCIO UN MERGE
df["€ per ETTARO"] = (df["Gain"] / df["ETTARI_TERRENO"]).round() # INFINE CALCOLO IL GUADAGNO E ARROTONDO

# GRAFICO PER GUADAGNO PER ETTARO DI OGNI CEREALE
# SCELGO UN GRAFICO A BARRE PER UNA VISUALIZZAZIONE COMPARATIVA VISIVA RAPIDA
fig_land = px.bar(
    df,
    x="CEREALE",
    y="€ per ETTARO",
    labels={"CEREALE": "Tipo di cereale", "€ per ETTARO": "Guadagno (€) per ettaro"}, # RINOMINO I TITOLI DEGLI ASSI
    color="CEREALE",color_discrete_map=colormap, # ASSEGNO IL MAPPING DEI COLORI
    category_orders={"CEREALE": cereal_order}, # ASSEGNO L'ORDINE
    text="€ per ETTARO"
    )

# PICCOLE MODIFICHE AL LAYOUT DEL GRAFICO, SCRITTE BIANCHE E SFONDO SCURO
fig_land.update_layout(
    font_color = "#F5F5F5",
    plot_bgcolor="#46494B",   
    paper_bgcolor="#46494B"   
)

# GRAFICO PER IL GUADAGNO TOTALE PER OGNI CEREALE
# SEMPRE UN GRAFICO A BARRE PER DUE MOTIVI: FACILE CONFRONTO DELL'ALTEZZA DELLE BARRE; VOLUTAMENTE UGUALE A QUELLO DEGLI ETTARI PER PARAGONARE REDDITIVITÀ TOTALE E RELATIVA
fig_cereal = px.bar(
    df_gain,
    x="Prodotto",
    y="Gain",
    labels={"Prodotto": "Tipo di cereale","Gain": "Guadagno totale (€)"}, # RINOMINO ASSI
    color="Prodotto",
    color_discrete_map=colormap, # STESSI COLORI
    category_orders={"Prodotto": cereal_order}, # STESSO ORDINE
    text="Gain"
    )

# SCRITTE CHIARE SFONDO SCURO
fig_cereal.update_layout(
    font_color = "#F5F5F5",
    plot_bgcolor="#46494B",   
    paper_bgcolor="#46494B"   
)

# INIZIALIZZA DASHBOARD
dashboard = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.MINTY,   # SCELGO IL TEMA BOOTSTRAP CHE PIÙ MI PIACE
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"  # AGGIUNGO LIBRERIA ICONE
])


# LAYOUT
dashboard.layout = dbc.Container(
    [
        # TITOLO
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Torroni Interactive Dashboard",
                    className="dashboard-title text-center text-primary mb-4 p-4" # testo centrato con un po'di margine extra sotto e un padding per spaziarlo intorno
                ),
                width=12 # imposto larghezza tutto schermo
            )
        ),
        dbc.Row(
            [
                # Selezionatore data
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader( 
                                html.H3(
                                    [
                                        html.I(className="fas fa-calendar text-primary"), # icona calendario con colore primario
                                        " Seleziona Periodo" # titolo del selezionatore di data
                                    ]
                                ),
                                className="bg-dark text-primary text-center d-flex justify-content-center align-items-center", style={"height": "100px"} # sfondo scuro, testo colore primario,centrato e imposto altezza a 100px per renderlo più proporsionato 
                            ),
                            dbc.CardBody(
                                html.Div(
                                    dcc.DatePickerRange( # selezionatore di data 
                                        id="date-picker",
                                        start_date=meteo2024["DATA"].min(),
                                        end_date=meteo2024["DATA"].max(),
                                        display_format="DD/MM/YYYY",
                                    ),
                                    className="d-flex justify-content-center align-items-center", style={"min-height": "100px", } # testo centrato
                                ),
                                className="p-0", style={"height": "100px"} # azzero il padding
                            ),
                            dbc.CardFooter(
                                dbc.Button( # bottone per reset dei parametri
                                    "Reset Data",
                                    id="reset-date-btn",
                                    color="primary",
                                    className="w-100 fs-3",
                                    style={"height": "80px"}
                                ),
                                style={"height": "100px"}
                            )
                        ],
                        className="shadow h-100 border border-primary border-4 p-1", # aggiungo un po' di ombre per effetto 3d e un bordo su tutti i lati
                    ),
                    width=4, className="mb-2" # ampiezza un terzo
                ),
                # Totale vendite
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                html.Div(
                                    [
                                        html.I(className="fas fa-shopping-cart fa-2x text-success mb-2"), # icona carrello
                                        html.H4("Totale vendite", className="text-muted mb-3"), # titoletto
                                        html.H1(
                                            id="totale-vendite", # quantità 
                                            className="text-primary fw-bold mb-0"
                                        )
                                    ],
                                    className="text-center"
                                ),
                                className="py-4" # padding sopra e sotto
                            ),
                            dbc.CardFooter(
                                dcc.Dropdown( # selezionatore di prodotto
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
                                    value="TUTTI", clearable=False, className="w-100"                                    
                                )
                            )
                        ],
                        className="shadow h-100 border border-success border-4 p-1"                        
                    ),
                    width=4, className="mb-2"
                ),
                # Totale prodotto
                dbc.Col(
                    dbc.Card(
                        [
                        dbc.CardBody(
                            html.Div(
                                [
                                    html.I(className="fas fa-industry fa-2x text-info mb-2"), #icona industria
                                    html.H4("Volume Prodotto", className="text-muted mb-3"), 
                                    html.H1(
                                        id="tot-produzione",
                                        className="text-info fw-bold mb-0"
                                    )
                                ],
                                className="text-center"
                            ),
                            className="py-4"
                        ),
                        dbc.CardFooter(
                                dcc.Dropdown( # altro selezionatore di prodotto
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
                                    value="TUTTI", clearable=False, className=" w-100"
                                )
                            )
                        ],
                        className="shadow h-100 border border-info border-4 p-1"
                    ),
                    width=4, className="mb-2"
                )
            ]
        ),
        dbc.Row([], style={"height": "25px"}), # riga di spaziatura

        # SEZIONE METEO
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H2("Condizioni Meteo",className="mb-0 text-center"), # titolo
                            className="bg-info text-white"
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H4(
                                                [
                                                    html.I(className="fas fa-temperature-half text-info mb-3"), # icona termometro
                                                    " Temperature"
                                                ],
                                                className="text-center text-info"
                                            ),
                                            dcc.Graph(id="temperature-graph", style={"height": "300px"}) # grafico temperature
                                        ],
                                        xs=12, md=4,  className="shadow h-100" # ampiezza modulare in base a schermo
                                    ),
                                    dbc.Col(
                                        [
                                            html.H4(
                                                [
                                                    html.I(className="fas fa-droplet text-info mb-3"), # icona goccia
                                                    " Umidità"
                                                ],
                                                className="text-center text-info"
                                            ),
                                            dcc.Graph(id="humidity-graph", style={"height": "300px"}) # grafico umidità
                                        ],
                                        xs=12, md=4, className="shadow h-100 border-start border-info border-4"
                                    ),
                                    dbc.Col(
                                        [
                                            html.H4(
                                                [
                                                    html.I(className="fas fa-cloud-rain text-info mb-3"), # icona meteo
                                                    " Fenomeni atmosferici"
                                                ],
                                                className="text-center text-info"
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
                width=12, className="mb-3"
            )
        ),
        # Sezione Prestazioni 
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader( # titolo                 
                            html.H2(
                                [
                                    html.I(className="fas fa-arrow-trend-up text-white"), # icona freccia trend
                                    " Prestazioni" 
                                ],
                                className="text-center bg-primary text-white p-2 m-0 rounded-top" # leggermente arrotondato
                            ),
                            className="p-0"
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col( # profitti per area
                                        [
                                            html.H3("Profitti per Area", className="text-center text-primary"), # titoletto
                                            dcc.Graph(figure=fig_land, style={"height": "335px","border-radius": "20px","overflow": "hidden"}) # stile associato al grafico
                                        ],
                                        xs=12, md=6, className="shadow h-100" # ampiezza sempre modulare
                                    ),
                                    dbc.Col( # profitti per cereale
                                        [
                                            html.H3("Profitti per Cereale", className="text-center text-primary"),
                                            dcc.Graph(figure=fig_cereal, style={"height": "335px", "border-radius": "20px","overflow": "hidden"})
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
                 width=12, className="mb-3"
            )
        )
    ],
    fluid=True, className="bg-dark" # cosi ottengo un ampiezza modulare e imposto lo sfondo scuro
)

# CALLBACKS

# selzionatore data
@dashboard.callback(
    Output("date-picker", "start_date"), # data inizio
    Output("date-picker", "end_date"), # data fine
    Input("reset-date-btn", "n_clicks"), # bottone
)

def reset_dates(n):
    return meteo2024["DATA"].min(), meteo2024["DATA"].max()


# totale vendite
@dashboard.callback(
    Output("totale-vendite", "children"), # vendite
    Input("date-picker", "start_date"), # data inzio
    Input("date-picker", "end_date"), # data fine
    Input("select-product-sold","value") # prodotto selezionato
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

    totale = int(df["Gain"].sum()) # somma totale

    return f"{totale:,}".replace(",", ".")+ " €" # formato italiano

# totale quintali prodotti
@dashboard.callback(
    Output("tot-produzione", "children"), #produzione
    Input("date-picker", "start_date"), # data inizo
    Input("date-picker", "end_date"), # data fine
    Input("select-product-produced","value") # prodotto selezionato
)

def aggiorna_totale_produzione(start_date, end_date, selected_product):

    # Filtra per data
    df = produzione[
        (produzione["Date"] >= start_date) &
        (produzione["Date"] <= end_date)
    ]

    # Filtra per prodotto
    if selected_product != "TUTTI":
        df = df[df["Prodotto"] == selected_product]

    totale = df["ProductionVolume"].sum()

    return f"{totale:,} Q"

# temperature
@dashboard.callback(
    Output("temperature-graph", "figure"), # grafico
    Input("date-picker", "start_date"), # data inizio
    Input("date-picker", "end_date") # data fine
)

def update_temperature_graph(start_date, end_date):
    
    # Filtro per data
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ]
    
    # Trasformo in formato lungo ( ho 3 tipologie di temperatura per ogni data)
    df_long = filtered_df.melt(
        id_vars=["DATA"],
        value_vars=["TMIN °C", "TMEDIA °C", "TMAX °C"],
        var_name="TIPO",
        value_name="TEMPERATURA"
    )
    
    # Mappo i nomi
    df_long["TIPO"] = df_long["TIPO"].map({
        "TMIN °C": "TEMP MIN",
        "TMEDIA °C": "TEMP MEDIA",
        "TMAX °C": "TEMP MAX"
    })
    
    # Scelgo grafico a linee per visualizzare andamento e assegno colori intuitivi alle temperature
    fig = px.line(
        df_long,
        x="DATA",
        y="TEMPERATURA",
        color="TIPO",
        color_discrete_map={
            "TEMP MIN": "#17a2b8",
            "TEMP MEDIA": "#ffc107",
            "TEMP MAX": "#dc3545"
        },
        labels={'DATA': '', 'TEMPERATURA': '°C'}
    )
    
    # imposto legenda in alto e orizzontale
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

# umidità
@dashboard.callback(
    Output("humidity-graph", "figure"), # grafico
    Input("date-picker", "start_date"), # data inizio
    Input("date-picker", "end_date") # data fine
)

def update_humidity_graph(start_date, end_date):

    # filtro per data
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ]
    
    # istogramma per avere un idea generale del trend di umidità 
    fig = px.histogram(
        filtered_df,
        x="UMIDITA %",
        nbins=30,
        color_discrete_sequence=['#17a2b8'],
        labels={'UMIDITA %': 'Umidità %'}
    )
    
    # layout del grafico
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=20, t=20, b=40)
    )
    
    return fig

# condizioni metereologiche
@dashboard.callback(
    Output("rain-graph", "figure"), # grafico
    Input("date-picker", "start_date"), # data inizio
    Input("date-picker", "end_date") # data fine
)

def update_rain_graph(start_date, end_date):

    # filtro data
    filtered_df = meteo2024[
        (meteo2024["DATA"] >= start_date) & 
        (meteo2024["DATA"] <= end_date)
    ]
    
    # raggruppo per fenomeni atmosferici
    counts = (
        filtered_df.groupby("FENOMENI").size().reset_index(name="Giorni")
    )

    # grafico a torta per variare un po' stili e per avere un idea generale della quantità dei giorni di pioggia in percentuale
    fig = px.pie(
        counts,
        names="FENOMENI",
        values="Giorni",
        color="FENOMENI",
        color_discrete_map={ # mappo colori per condizioni
            'pioggia': '#17a2b8',
            'nebbia': '#6c757d',
            'sole': '#ffc107',
        }
    )
    
    # stile della legenda e del grafico
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