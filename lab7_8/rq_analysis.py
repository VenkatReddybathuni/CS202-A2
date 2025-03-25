import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Bandit results directory
BANDIT_RESULTS_DIR = "bandit_results"

# Ensure plots directory exists
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Load all repositories' CSVs
repo_data = {}
for repo_file in os.listdir(BANDIT_RESULTS_DIR):
    if repo_file.endswith("_bandit_analysis.csv"):
        repo_name = repo_file.replace("_bandit_analysis.csv", "")
        repo_data[repo_name] = pd.read_csv(os.path.join(BANDIT_RESULTS_DIR, repo_file))

### **RQ1: High Severity Vulnerabilities - Introduction & Fixes**
print("\nRQ1: Identifying when high-severity vulnerabilities were introduced and fixed...\n")

def analyze_high_severity(repo_name):
    df = repo_data[repo_name].copy()
    df = df.sort_values("commit_id")  # Sort by commit progression
    df["commit_progress"] = range(1, len(df) + 1)

    # Identify introduction and fixes
    introduced = df[df["severity_high"] > 0].set_index("commit_progress")["severity_high"]
    fixed = df[df["severity_high"] == 0].set_index("commit_progress")["severity_high"]

    # Plot high-severity vulnerabilities over commit progress
    plt.figure(figsize=(10, 5))
    plt.plot(introduced, marker='o', linestyle='-', color='red', label="Introduced")
    plt.plot(fixed, marker='x', linestyle='--', color='green', label="Fixed")
    plt.xlabel("Commit Progress (1 to 100)")
    plt.ylabel("Count of High Severity Issues")
    plt.title(f"Introduction vs. Fixes of High Severity Issues in {repo_name}")
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plt.savefig(os.path.join(PLOTS_DIR, f"{repo_name}_high_severity.png"))
    plt.close()

for repo in repo_data.keys():
    analyze_high_severity(repo)

### **RQ2: Patterns in Different Severity Levels**
print("\nRQ2: Comparing patterns of different severity vulnerabilities over commits...\n")

def analyze_severity_patterns(repo_name):
    df = repo_data[repo_name].copy()
    df = df.sort_values("commit_id")  # Sort by commit progression
    df["commit_progress"] = range(1, len(df) + 1)

    # Plot all severity levels
    plt.figure(figsize=(12, 6))
    plt.plot(df["commit_progress"], df["severity_high"], marker="o", label="High Severity", color="red")
    plt.plot(df["commit_progress"], df["severity_medium"], marker="s", label="Medium Severity", color="orange")
    plt.plot(df["commit_progress"], df["severity_low"], marker="^", label="Low Severity", color="blue")
    
    plt.xlabel("Commit Progress (1 to 100)")
    plt.ylabel("Count of Vulnerabilities")
    plt.title(f"Vulnerability Severity Trends in {repo_name}")
    plt.legend()
    plt.grid(True)

    # Save plot
    plt.savefig(os.path.join(PLOTS_DIR, f"{repo_name}_severity_patterns.png"))
    plt.close()

for repo in repo_data.keys():
    analyze_severity_patterns(repo)

### **RQ3: Most Frequent CWE Categories (Per Repository)**
print("\nRQ3: Finding the most frequent CWEs per repository...\n")

def analyze_cwe_per_repo(repo_name):
    df = repo_data[repo_name]
    cwe_counts = {}
    
    for cwe_list in df["unique_cwes"].dropna():
        for cwe in eval(cwe_list):  # Convert string representation of list to actual list
            cwe_counts[cwe] = cwe_counts.get(cwe, 0) + 1

    # Convert to DataFrame for visualization
    cwe_df = pd.DataFrame(sorted(cwe_counts.items(), key=lambda x: x[1], reverse=True), columns=["CWE", "Count"])
    
    # Display top 10 CWEs
    print(f"\nTop 10 Most Frequent CWEs in {repo_name}:")
    print(cwe_df.head(10))
    
    # Plot CWE Frequency
    plt.figure(figsize=(12, 6))
    sns.barplot(x="CWE", y="Count", data=cwe_df.head(10))
    
    plt.xlabel("CWE ID")
    plt.ylabel("Frequency")
    plt.title(f"Top 10 Most Frequent CWEs in {repo_name}")
    plt.xticks(rotation=45)

    # Save plot
    plt.savefig(os.path.join(PLOTS_DIR, f"{repo_name}_top_CWE_frequencies.png"))
    plt.close()

for repo in repo_data.keys():
    analyze_cwe_per_repo(repo)
