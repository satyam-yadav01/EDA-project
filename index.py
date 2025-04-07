import pandas as pd

df=pd.read_excel("Nutrition data.xlsx")

#data summary
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())


