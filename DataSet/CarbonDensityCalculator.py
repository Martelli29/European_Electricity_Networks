import pandas as pd

df=pd.read_csv("share-elec-produc-by-source-FILTERED.txt")

df["Carbon intensity (gCO2eq/kWh)"]=(df["Coal (% electricity)"]*820+df["Gas (% electricity)"]*490+df["Hydro (% electricity)"]*24+df["Solar (% electricity)"]*44+df["Wind (% electricity)"]*11+df["Oil (% electricity)"]*650+df["Nuclear (% electricity)"]*12+df["Other renewables (% electricity)"]*230)/100

df.to_csv('share-by-source+Carbon_Density.txt', index=False)


ddf=pd.read_csv("share-elec-produc-by-source2020.txt")

ddf["Carbon intensity (gCO2eq/kWh)"]=(ddf["Coal (% electricity)"]*820+ddf["Gas (% electricity)"]*490+ddf["Hydro (% electricity)"]*24+ddf["Solar (% electricity)"]*44+ddf["Wind (% electricity)"]*11+ddf["Oil (% electricity)"]*650+ddf["Nuclear (% electricity)"]*12+ddf["Other renewables (% electricity)"]*230)/100

ddf.to_csv('share-by-source2020+Carbon_Density.txt', index=False)