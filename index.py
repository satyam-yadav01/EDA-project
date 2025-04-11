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



# ---------------- Objective 2 ----------------
# Top and bottom performing districts

indicators = ["Children under 5 years who are stunted (height-for-age)18 (%)",
    "Children under 5 years who are wasted (weight-for-height)18 (%)",
    "Children under 5 years who are underweight (weight-for-age)18 (%)",
    "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)",
    "Children under 5 years who are overweight (weight-for-height)20 (%)"]



for indicator in indicators:
    plt.figure(figsize=(14, 6))

    # Top 10
    top10 = df.nlargest(10, indicator)
    plt.subplot(1, 2, 1)
    sns.barplot(
        data=top10,
        x=indicator,
        y='District Names',
        hue='District Names',
        palette='Reds_r'
    )
    plt.title(f"Top 10 Districts with Highest {indicator.split()[5]} (%)")
    plt.xlabel('Percentage (%)')
    plt.ylabel('District')

    # Bottom 10
    bottom10 = df.nsmallest(10, indicator)
    plt.subplot(1, 2, 2)
    sns.barplot(
        data=bottom10,
        x=indicator,
        y='District Names',
        hue='District Names',
        palette='Greens'
    )
    plt.title(f"Bottom 10 Districts with Lowest {indicator.split()[5]} (%)")
    plt.xlabel('Percentage (%)')
    plt.ylabel('District')

    plt.suptitle(f"{indicator}", fontsize=14)
    plt.tight_layout()
    plt.show()


# ---------------- Objective 3 ----------------
# Explore correlation between indicators

# Correlation heatmap
correlation_matrix = df_short.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Between Child Malnutrition Indicators")
plt.show()

# Pairplot
sns.pairplot(df_short)
plt.suptitle("Pairwise Relationships Between Indicators", y=1.02)
plt.show()

# ---------------- Objective 4 ----------------
# Geographic comparison (State-wise)

state_avg = df.groupby("State/UT")[key_columns].mean().reset_index()

print(state_avg.head())

state_avg_melted = pd.melt(state_avg, id_vars=["State/UT"], var_name="Indicator", value_name="Value")

plt.figure(figsize=(15, 8))
sns.barplot(data=state_avg_melted, x="Value", y="State/UT", hue="Indicator")
plt.title("State-wise Average of Child Malnutrition Indicators")
plt.tight_layout()
plt.show()


# ---------------- Objective 5 ----------------
# Actionable insights for top worst-affected districts

# Step 1: Summary statistics for understanding the overall situation
summary_stats = df[key_columns].describe()
print("🔍 Summary Statistics for All Indicators:\n")
print(summary_stats)

# Step 2: Identify districts with multiple critical indicators (Top 10 for any 2 or more indicators)
critical_districts = []

for indicator in key_columns:
    top10 = df.nlargest(10, indicator)
    critical_districts.extend(top10['District Names'].tolist())

# Count how often each district appears
from collections import Counter
district_counts = Counter(critical_districts)

# Districts appearing more than once in top 10s (critical zones)
hotspot_districts = [district for district, count in district_counts.items() if count > 1]

print("\n Districts appearing in top 10 of more than one malnutrition indicator (Hotspots):\n")
for district in hotspot_districts:
    state = df[df['District Names'] == district]['State/UT'].values[0]
    print(f"- {district}, {state}")

# Step 3: Regions that are consistently better – bottom 10 for all indicators (performers)
good_districts = []

for indicator in key_columns:
    bottom10 = df.nsmallest(10, indicator)
    good_districts.extend(bottom10['District Names'].tolist())

# Count how often each district appears in bottom 10
good_counts = Counter(good_districts)
consistently_good = [district for district, count in good_counts.items() if count > 1]

print("\n Districts performing well in multiple indicators (Consistently Better Performers):\n")
for district in consistently_good:
    state = df[df['District Names'] == district]['State/UT'].values[0]
    print(f"- {district}, {state}")

# Step 4: Recommendations based on findings
print("\n💡 General Recommendations:\n")
print("""
1. Focus targeted intervention programs in hotspot districts appearing in multiple top 10 lists.
2. Strengthen local healthcare and nutrition outreach in districts with high anaemia and underweight prevalence.
3. Study best practices from consistently performing districts and replicate policies where possible.
4. Collaborate with NGOs to conduct focused awareness, education, and supplementation drives.
5. Allocate resources and policy funding regionally, prioritizing high-risk districts.
""")

