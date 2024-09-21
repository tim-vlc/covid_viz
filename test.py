import pandas as pd
covid_df = pd.read_csv("owid-covid-data.csv")
small_df = covid_df[["location", "date", "new_cases"]]

print(small_df[small_df["date"]=="2022-07-04"])