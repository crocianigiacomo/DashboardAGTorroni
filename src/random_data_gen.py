import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Generazione date
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Dizionario per mappare numero mese -> nome mese
mesi_dict = {1: 'GENNAIO', 2: 'FEBBRAIO', 3: 'MARZO', 
             4: 'APRILE', 5: 'MAGGIO', 6: 'GIUGNO', 
             7: 'LUGLIO', 8: 'AGOSTO',9: 'SETTEMBRE', 
             10: 'OTTOBRE', 11: 'NOVEMBRE', 12: 'DICEMBRE'}

# Cereali coltivati
cereali = ["MEDICA","COLZA","FRUMENTO TENERO","FRUMENTO DURO","ORZO","GIRASOLE","MAIS"]

# Leggi csv cereali azienda torroni e prezzi mercato di riferimento
df_cereali = pd.read_csv("data\CEREALI_TERRENO_PRODUZIONE.csv", sep=";")
df_prezzi = pd.read_csv("data/PREZZI_CEREALI.csv", sep=";")

# Quantità annue totali prodotte da Torroni
tot_medica = df_cereali['PRODUZIONE_ANNUA'][0]
tot_colza = df_cereali['PRODUZIONE_ANNUA'][1]
tot_frumento_t = df_cereali['PRODUZIONE_ANNUA'][2]
tot_frumento_d = df_cereali['PRODUZIONE_ANNUA'][3]
tot_orzo = df_cereali['PRODUZIONE_ANNUA'][4]
tot_girasole = df_cereali['PRODUZIONE_ANNUA'][5]
tot_mais = df_cereali['PRODUZIONE_ANNUA'][6]

# Crea lista prodotti
prodotti = np.random.choice(cereali,200)

# Crea liste personalizzate in base al prodotto
production_volumes = []
production_dates = []

for i,prodotto in enumerate(prodotti):
    if prodotto == "MEDICA":
        date = start_date+timedelta(days=random.randint(120,240))
        volume = np.random.randint(0,(tot_medica/2))
        tot_medica-=volume
    elif prodotto == "COLZA":
        date = start_date+timedelta(days=random.randint(150,180))
        volume = np.random.randint(0,(tot_colza/2))
        tot_colza-=volume
    elif prodotto == "FRUMENTO TENERO":
        date = start_date+timedelta(days=random.randint(180,210))
        volume = np.random.randint(0,(tot_frumento_t/2))
        tot_frumento_t-=volume
    elif prodotto == "FRUMENTO DURO":
        date = start_date+timedelta(days=random.randint(180,210))
        volume = np.random.randint(0,(tot_frumento_d/2))
        tot_frumento_d-=volume
    elif prodotto == "ORZO":
        date = start_date+timedelta(days=random.randint(180,210))
        volume = np.random.randint(0,(tot_orzo/2))
        tot_orzo-=volume
    elif prodotto == "GIRASOLE":
        date = start_date+timedelta(days=random.randint(240,270))
        volume = np.random.randint(0,(tot_girasole/2))
        tot_girasole-=volume
    elif prodotto == "MAIS":
        date = start_date+timedelta(days=random.randint(270,330))
        volume = np.random.randint(0,(tot_mais/2))
        tot_mais-=volume

    production_volumes.append(volume)
    production_dates.append(date)

production_data = {
    "Prodotto": prodotti,
    "Date": production_dates,
    "ProductionVolume": production_volumes,
}

df = pd.DataFrame(production_data)
df.to_csv("data\production_data.csv",index=False)

# Quantità magazzino
medica = df_cereali['PRODUZIONE_ANNUA'][0]
colza = df_cereali['PRODUZIONE_ANNUA'][1]
frumento_t = df_cereali['PRODUZIONE_ANNUA'][2]
frumento_d = df_cereali['PRODUZIONE_ANNUA'][3]
orzo = df_cereali['PRODUZIONE_ANNUA'][4]
girasole = df_cereali['PRODUZIONE_ANNUA'][5]
mais = df_cereali['PRODUZIONE_ANNUA'][6]

# Creazione andamento delle vendite rimanendo fedeli ai prezzi di mercato e alle quantità di produzione ma randomizzando le richieste
sales_volumes = []
sales_dates = []
sales_prices = []

for i,prodotto in enumerate(prodotti):
    if prodotto == "MEDICA":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(medica/2))
        medica-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "COLZA":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(colza/2))
        colza-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "FRUMENTO TENERO":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(frumento_t/2))
        frumento_t-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "FRUMENTO DURO":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(frumento_d/2))
        frumento_d-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "ORZO":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(orzo/2))
        orzo-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "GIRASOLE":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(girasole/2))
        girasole-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]
    elif prodotto == "MAIS":
        date = start_date+timedelta(days=random.randint(0,360))
        volume = np.random.randint(0,(mais/2))
        mais-=volume
        mese_nome = mesi_dict[date.month]
        price = df_prezzi.loc[df_prezzi["CEREALE"] == prodotto, mese_nome].values[0]


    sales_volumes.append(volume)
    sales_dates.append(date)
    sales_prices.append(price)

sales_data = {
    "Prodotto": prodotti,
    "Date": sales_dates,
    "SalesVolume": sales_volumes,
    "ActualPrice": sales_prices,
}   

df = pd.DataFrame(sales_data)
df.to_csv("data\sales_data.csv",index=False)