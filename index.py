import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_excel("Nutrition data.xlsx")

#data summary
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())



