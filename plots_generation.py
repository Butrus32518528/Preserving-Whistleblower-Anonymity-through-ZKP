import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV logs
mining_time_difficulty = pd.read_csv("mining_time_difficulty.csv", header=None, names=["Block", "Difficulty", "Mining Time"])
mining_time_sensitivity = pd.read_csv("mining_time_sensitivity.csv", header=None, names=["Block", "Sensitivity", "Mining Time"])
total_mining_time = pd.read_csv("total_mining_time.csv", header=None, names=["Block", "Total Mining Time"])

# Plot Mining Time vs. Difficulty Level
plt.figure(figsize=(10, 6))
plt.bar(mining_time_difficulty["Difficulty"], mining_time_difficulty["Mining Time"], color='skyblue')
plt.xlabel("Difficulty Level")
plt.ylabel("Mining Time (s)")
plt.title("Mining Time vs. Difficulty Level")
plt.show()

# Plot Mining Time vs. Sensitivity Level
plt.figure(figsize=(10, 6))
sensitivity_map = {"Highest" : "red", "High": "purple", "Medium": "orange", "Low" : "blue", "V_Low": "green"}
colors = mining_time_sensitivity["Sensitivity"].map(sensitivity_map)
plt.bar(mining_time_sensitivity["Block"], mining_time_sensitivity["Mining Time"], color=colors)
plt.xlabel("Block Number")
plt.ylabel("Mining Time (s)")
plt.title("Mining Time vs. Sensitivity Level")
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=sens)
                    for sens, color in sensitivity_map.items()])
plt.show()

# Plot Total Mining Time per Block
plt.figure(figsize=(10, 6))
plt.plot(total_mining_time["Block"], total_mining_time["Total Mining Time"], marker='o')
plt.xlabel("Block Number")
plt.ylabel("Total Mining Time (s)")
plt.title("Total Mining Time per Block")
plt.show()
