import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df=pd.read_excel("Nutrition data.xlsx")

#data summary
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())

##           Objective 1- To analyze and compare the prevalence of child malnutrition indicators—such as stunting,
             ##  wasting, and underweight—across districts in India.

#  List of key columns to analyze
key_columns = [
    "Children under 5 years who are stunted (height-for-age)18 (%)",
    "Children under 5 years who are wasted (weight-for-height)18 (%)",
    "Children under 5 years who are underweight (weight-for-age)18 (%)",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)",
    "Children under 5 years who are overweight (weight-for-height)20 (%)"
]
short_names = {
    "Children under 5 years who are stunted (height-for-age)18 (%)":"stunted",
    "Children under 5 years who are wasted (weight-for-height)18 (%)":"wasted",
    "Children under 5 years who are underweight (weight-for-age)18 (%)":"underweight",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)":"anaemic",
    "Children under 5 years who are overweight (weight-for-height)20 (%)":"overweight"
}

#  Histogram for each indicator
'''for col in key_columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[col], kde=True, color='skyblue')
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Number of Districts")
    plt.tight_layout()
    plt.show()

##          Objective 2- To identify the top and bottom performing districts in terms of key child nutrition indicators, 
            # helping to highlight regions needing urgent attention
for col in key_columns:
    print(f"Top 10 districts with highest {col}:\n", df[['District Names', col]].sort_values(by=col, ascending=False).head(10))
    print(f"Bottom 10 districts with lowest {col}:\n", df[['District Names', col]].sort_values(by=col).head(10))
'''
            ## objective 3- Correlation matrix
# Compute correlation matrix
df_short = df[list(short_names.keys())].rename(columns=short_names)
correlation_matrix = df_short.corr()

# Plot heatmap

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation between Child Malnutrition Indicators")
plt.show()

sns.scatterplot(data=df, x=key_columns[0], y=key_columns[2])
plt.title("Stunting vs Underweight")
plt.xlabel("Stunted (%)")
plt.ylabel("Underweight (%)")
plt.show()

sns.scatterplot(data=df, x=key_columns[1], y=key_columns[2])
plt.title("wasted vs Underweight")
plt.xlabel("wasted (%)")
plt.ylabel("Underweight (%)")
plt.show()

# Calculate average malnutrition rates per state'''
state_avg = df.groupby("State/UT")[key_columns].mean().reset_index()

# Bar plot for state comparison
plt.figure(figsize=(14, 6))
sns.barplot(data=state_avg.sort_values(key_columns[0], ascending=False), x="State/UT", y=key_columns[0])
plt.xticks(rotation=90)
plt.title("Average Stunting (%) by State")
plt.tight_layout()
plt.show()

