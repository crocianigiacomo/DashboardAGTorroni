import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Generazione date
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Cereali coltivati
cereali = ["MEDICA","COLZA","FRUMENTO TENERO","FRUMENTO DURO","ORZO","GIRASOLE","MAIS"]

# Leggi csv cereali azienda torroni
df_cereali = pd.read_csv("data\CEREALI_TERRENO_PRODUZIONE.csv", sep=";")

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