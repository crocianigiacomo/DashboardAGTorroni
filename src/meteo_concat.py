import pandas as pd
import glob

dfs = []
filenames = glob.glob("DashboardAGTorroni\data\MeteoCetona2024\*.csv")

for filename in filenames:
    dfs.append(pd.read_csv(filename, sep=";",usecols=[1,2,3,4,6,14]))

meteo2024 = pd.concat(dfs)
meteo2024["DATA"]=pd.to_datetime(meteo2024["DATA"],format="mixed")
meteo2024.sort_values(by ="DATA",ascending=True,inplace=True)
df = pd.DataFrame(meteo2024)
df.to_csv("DashboardAGTorroni\data\meteo2024.csv",index=False)