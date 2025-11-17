import pandas as pd
import glob

dfs = []
filenames = glob.glob("data\MeteoCetona2024\*.csv")

for filename in filenames:
    dfs.append(pd.read_csv(filename, sep=";",usecols=[1,2,3,4,6,14]))

meteo2024 = pd.concat(dfs)
meteo2024["DATA"]=pd.to_datetime(meteo2024["DATA"],format="mixed")
meteo2024.sort_values(by ="DATA",ascending=True,inplace=True)
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].fillna("sole")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].str.strip()
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("", "sole")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia temporale", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia nebbia", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia neve", "pioggia")
meteo2024["FENOMENI"] = meteo2024["FENOMENI"].replace("pioggia temporale nebbia", "pioggia")

df = pd.DataFrame(meteo2024)
df.to_csv("data\meteo2024.csv",index=False)