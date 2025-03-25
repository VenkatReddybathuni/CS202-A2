import os
import json
import pandas as pd

# Base folder where reports are stored
bandit_reports_folder = "bandit_results"

# Initialize a dictionary to store results per repository
repo_results = {}

# Loop through each repository folder
for repo in os.listdir(bandit_reports_folder):
    repo_path = os.path.join(bandit_reports_folder, repo)
    
    if os.path.isdir(repo_path):  # Ensure it's a directory
        results = []
        
        # Loop through each JSON file in the repository folder
        for report_file in sorted(os.listdir(repo_path)):
            if report_file.endswith(".json"):
                commit_id = report_file.replace("bandit_report_", "").replace(".json", "")
                report_path = os.path.join(repo_path, report_file)

                with open(report_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Extract totals from the "_totals" section
                totals = data.get("metrics", {}).get("_totals", {})
                confidence_high = totals.get("CONFIDENCE.HIGH", 0)
                confidence_medium = totals.get("CONFIDENCE.MEDIUM", 0)
                confidence_low = totals.get("CONFIDENCE.LOW", 0)

                severity_high = totals.get("SEVERITY.HIGH", 0)
                severity_medium = totals.get("SEVERITY.MEDIUM", 0)
                severity_low = totals.get("SEVERITY.LOW", 0)

                # Extract unique CWEs from "results" section
                unique_cwes = set()
                for issue in data.get("results", []):
                    if "issue_cwe" in issue and "id" in issue["issue_cwe"]:
                        unique_cwes.add(issue["issue_cwe"]["id"])

                results.append({
                    "commit_id": commit_id,
                    "confidence_high": confidence_high,
                    "confidence_medium": confidence_medium,
                    "confidence_low": confidence_low,
                    "severity_high": severity_high,
                    "severity_medium": severity_medium,
                    "severity_low": severity_low,
                    "unique_cwes": ", ".join(map(str, unique_cwes))  # Store CWEs as a string
                })

        # Convert results to DataFrame and save a CSV for each repository
        df = pd.DataFrame(results)
        csv_filename = os.path.join(bandit_reports_folder, f"{repo}_bandit_analysis.csv")
        df.to_csv(csv_filename, index=False)
        print(f"Analysis completed for {repo}. Results saved to {csv_filename}")
