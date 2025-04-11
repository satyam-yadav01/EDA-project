import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df=pd.read_excel("Nutrition data.xlsx")

# Removing whitespace from column names for ease
df.columns = df.columns.str.strip()  

        #data summary
print(df.isnull().sum())

print("Top 5 rows of dataset\n")
print(df.head())

print("Last 5 rows of dataset\n")
print(df.tail())

print("Information about the dataset\n")
print(df.info())

print("Available columns\n")
print(df.columns.tolist(),"\n")

#checking for duplicates
duplicates=df.duplicated().sum()
print(duplicates)

print("Statistical summary\n")
print(df.describe())



#  List of key columns to analyze
key_columns = [
    "Children under 5 years who are stunted (height-for-age)18 (%)",
    "Children under 5 years who are wasted (weight-for-height)18 (%)",
    "Children under 5 years who are underweight (weight-for-age)18 (%)",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)",
    "Children under 5 years who are overweight (weight-for-height)20 (%)"
]

outlier_summary = {}

for col in key_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary[col] = len(outliers)

outlier_summary_df = pd.DataFrame(list(outlier_summary.items()), columns=['Column', 'Outlier_Count'])
print(outlier_summary_df)


# Instead of writing long column names; using short column names
short_names = {
    "Children under 5 years who are stunted (height-for-age)18 (%)":"stunted",
    "Children under 5 years who are wasted (weight-for-height)18 (%)":"wasted",
    "Children under 5 years who are underweight (weight-for-age)18 (%)":"underweight",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)":"anaemic",
    "Children under 5 years who are overweight (weight-for-height)20 (%)":"overweight"
}


# Computing correlation matrix to find the relationship between different features

df_short = df[list(short_names.keys())].rename(columns=short_names)
correlation_matrix = df_short.corr()

# Plotting heatmap

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation between Child Malnutrition Indicators")
plt.show()

# ---------------- Objective 1 ----------------
# Analyzing & comparing the prevalence of malnutrition indicators

# Boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_short)
plt.title("Boxplot: Child Malnutrition Indicators Distribution")
plt.ylabel("Percentage (%)")

plt.tight_layout()
plt.show()

# Histograms
df_short.hist(bins=15, figsize=(15, 10), layout=(2, 3))
plt.suptitle("Histogram: Malnutrition Indicators")
plt.tight_layout()
plt.show()



