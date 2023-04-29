import pandas as pd

df = pd.read_csv('Electricity_Production_TWh_FILTERED.txt')

df["Total (TWh)"] = df["Electricity from coal (TWh)"]+df["Electricity from gas (TWh)"]+df["Electricity from hydro (TWh)"]+df["Electricity from other renewables (TWh)"] + \
    df["Electricity from solar (TWh)"]+df["Electricity from oil (TWh)"] + \
    df["Electricity from wind (TWh)"]+df["Electricity from nuclear (TWh)"]

df.to_csv('Electricity_Production_TWh_FINAL.txt', index=False)

ddf = pd.read_csv('Electricity_Production_TWh2020.txt')

ddf["Total (TWh)"] = ddf["Electricity from coal (TWh)"]+ddf["Electricity from gas (TWh)"]+ddf["Electricity from hydro (TWh)"]+ddf["Electricity from other renewables (TWh)"] + \
    ddf["Electricity from solar (TWh)"]+ddf["Electricity from oil (TWh)"] + \
    ddf["Electricity from wind (TWh)"]+ddf["Electricity from nuclear (TWh)"]

ddf.to_csv('Electricity_Production_TWh2020_FINAL.txt', index=False)
