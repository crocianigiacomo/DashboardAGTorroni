import pandas as pd
import glob

# creo array vuoto per concatenare file
dfs = []
filenames = glob.glob("data/MeteoCetona2024/*.csv") # creo lista di nomi dei file csv

# leggo tutti i file nella lista
for filename in filenames:
    dfs.append(pd.read_csv(filename, sep=";",usecols=[1,2,3,4,6,14]))

# concateno i file
meteo2024 = pd.concat(dfs)

# imposto data a datetime
meteo2024["DATA"]=pd.to_datetime(meteo2024["DATA"],format="mixed")

# ordino per data crescente
meteo2024.sort_values(by ="DATA",ascending=True,inplace=True)

# sostituisco i valori mancanti con quelli desiderati
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].fillna("sole")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].str.strip()
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("", "sole")

# sostituisco con pioggia tutte le varianti di pioggia
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia temporale", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia nebbia", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia neve", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia temporale nebbia", "pioggia")

# creo un dataframe e lo salvo in csv
df = pd.DataFrame(meteo2024)
df.to_csv("data/meteo2024.csv",index=False)