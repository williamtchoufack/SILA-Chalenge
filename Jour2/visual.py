import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.animation import FuncAnimation

df = pd.read_csv("Iris.csv") 

print(df.mean(numeric_only=True))
print(df.median(numeric_only=True))
print(df.std(numeric_only=True))
print(df.quantile([0.25, 0.5, 0.75], numeric_only=True))

sns.set(style="whitegrid")

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

sns.histplot(df['SepalLengthCm'], bins=15, kde=True, ax=axs[0, 0], color="green")
axs[0, 0].set_title("Sepal Length")

x = df['SepalLengthCm']
y = df['PetalLengthCm']
axs[0, 1].scatter(x, y, color='blue')
m, b = np.polyfit(x, y, 1)
axs[0, 1].plot(x, m*x + b, color='red')
axs[0, 1].set_title("Sepal vs Petal")

c = df.corr(numeric_only=True)
sns.heatmap(c, annot=True, cmap="coolwarm", ax=axs[1, 0])
axs[1, 0].set_title("Correlations")

line, = axs[1, 1].plot([], [], color="purple")
axs[1, 1].set_xlim(0, len(df))
axs[1, 1].set_ylim(df['SepalLengthCm'].min(), df['SepalLengthCm'].max())
axs[1, 1].set_title("Sepal Length")

xdata, ydata = [], []

def update(frame):
    xdata.append(frame)
    ydata.append(df['SepalLengthCm'][frame])
    line.set_data(xdata, ydata)
    return line,

ani = FuncAnimation(fig, update, frames=len(df), interval=50)

plt.tight_layout()
plt.show()
