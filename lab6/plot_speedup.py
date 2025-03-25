# import pandas as pd
# import matplotlib.pyplot as plt

# # Load extracted data
# df = pd.read_csv("parallel_results.csv")

# # Replace "auto" with a readable value for plotting
# df.replace("auto", "A", inplace=True)

# # Set your Tseq (from the sequential test logs)
# Tseq = 10.0  # Replace this with your actual computed Tseq value

# # Compute Speedup
# df["Speedup"] = Tseq / df["Tpar"]

# # Plot
# plt.figure(figsize=(10, 6))
# for mode in df["Mode"].unique():
#     subset = df[df["Mode"] == mode]
#     plt.plot(subset.index, subset["Speedup"], marker="o", label=f"Mode: {mode}")

# plt.xlabel("Test Configuration Index")
# plt.ylabel("Speedup (Tseq / Tpar)")
# plt.title("Speedup of Parallel Test Execution")
# plt.legend()
# plt.grid(True)
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load extracted data
df = pd.read_csv("parallel_results.csv")

# Replace "auto" with "A" for readability
df.replace("auto", "A", inplace=True)

# Set your Tseq (replace with your actual computed Tseq)
Tseq = 10.0  # Replace this with your actual computed Tseq

# Compute Speedup
df["Speedup"] = Tseq / df["Tpar"]

# Generate labels for the x-axis
df["Config"] = df.apply(lambda row: f"-n {row['Workers']} | --parallel-threads {row['Threads']} | --dist {row['Mode']}", axis=1)

# Plot settings
plt.figure(figsize=(12, 6))
x = np.arange(len(df))  # X-axis positions
bars = plt.bar(x, df["Speedup"], color=['#4c72b0', '#dd8452', '#55a868', '#c44e52', '#8172b2', '#937860', '#da8bc3', '#8c8c8c'])

# Add labels above bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=10)

# Formatting
plt.xticks(x, df["Config"], rotation=45, ha="right")
plt.ylabel("Speedup (Tseq / Tpar)")
plt.xlabel("Parallelization Configurations")
plt.title("Speedup of Parallel Test Execution")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Show plot
plt.show()
