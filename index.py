import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_excel("Nutrition data.xlsx")

#data summary
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())

## Objective 1- To analyze and compare the prevalence of child malnutrition indicators—such as stunting,
##  wasting, and underweight—across districts in India.

#  List of key columns to analyze
key_columns = [
    "Children under 5 years who are stunted (height-for-age)18 (%)",
    "Children under 5 years who are wasted (weight-for-height)18 (%)",
    "Children under 5 years who are underweight (weight-for-age)18 (%)",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)",
    "Children under 5 years who are overweight (weight-for-height)20 (%)"
]

#  Histogram for each indicator
for col in key_columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[col], kde=True, color='skyblue')
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Number of Districts")
    plt.tight_layout()
    plt.show()


