import pandas as pd


df = pd.read_csv('Electricity_Production_TWh_FILTERED.txt')

df["Total (TWh)"] = df["Electricity from coal (TWh)"]+df["Electricity from gas (TWh)"]+df["Electricity from hydro (TWh)"]+df["Electricity from other renewables (TWh)"] + \
    df["Electricity from solar (TWh)"]+df["Electricity from oil (TWh)"] + \
    df["Electricity from wind (TWh)"]+df["Electricity from nuclear (TWh)"]

colonne = ["Electricity from coal (TWh)", "Electricity from gas (TWh)", "Electricity from hydro (TWh)", "Electricity from other renewables (TWh)",
           "Electricity from solar (TWh)", "Electricity from oil (TWh)", "Electricity from wind (TWh)", "Electricity from nuclear (TWh)", "Total (TWh)"]

mean = df.groupby("Entity")[colonne].mean()

mean.to_csv('Electricity_Production_TWh_FINAL.txt')



ddf = pd.read_csv('Electricity_Production_TWh2020.txt')

ddf["Total (TWh)"] = ddf["Electricity from coal (TWh)"]+ddf["Electricity from gas (TWh)"]+ddf["Electricity from hydro (TWh)"]+ddf["Electricity from other renewables (TWh)"] + \
    ddf["Electricity from solar (TWh)"]+ddf["Electricity from oil (TWh)"] + \
    ddf["Electricity from wind (TWh)"]+ddf["Electricity from nuclear (TWh)"]

ddf.to_csv('Electricity_Production_TWh2020_FINAL.txt', index=False)
