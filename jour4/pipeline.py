import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_titanic = pd.read_csv("Titanic-Dataset.csv")
df_iris    = pd.read_csv("Iris.csv")

print(df_titanic.head())
print(df_titanic.shape)
print(df_titanic.isnull().sum())

df_titanic['Age'] = df_titanic['Age'].fillna(df_titanic['Age'].median())

Q1  = df_titanic['Fare'].quantile(0.25)
Q3  = df_titanic['Fare'].quantile(0.75)
IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

outliers = df_titanic[(df_titanic['Fare'] < borne_inf) | (df_titanic['Fare'] > borne_sup)]
print(f"\nOutliers détectés sur 'Fare' : {len(outliers)}")


df_titanic['Family_Size'] = df_titanic['SibSp'] + df_titanic['Parch'] + 1

plt.figure(figsize=(8, 5))
sns.histplot(df_titanic['Age'], bins=30, kde=True, color='steelblue')
plt.title("Distribution de l'âge — Titanic")
plt.xlabel("Âge")
plt.tight_layout()
plt.savefig("age_distribution.png")
plt.show()


df_titanic.to_csv("titanic_clean.csv", index=False)
print("\nFichier exporté : titanic_clean.csv")
