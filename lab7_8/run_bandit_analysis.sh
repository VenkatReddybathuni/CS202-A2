#!/bin/bash

# List of repository directories
REPOS=("deepchecks" "oletools" "watchdog")

# Loop through each repository
for REPO in "${REPOS[@]}"; do
    echo "Processing repository: $REPO"
    
    # Navigate to the repository
    cd "$REPO" || { echo "Failed to access $REPO"; exit 1; }

    # Create a results directory for storing reports
    mkdir -p "../bandit_results/$REPO"

    # Get the last 100 non-merge commits and save to a file
    git log --pretty=format:"%H" -n 100 > commits.txt

    # Process each commit
    while read -r commit; do
        echo "Checking out commit: $commit"
        git checkout "$commit" --quiet

        # Run Bandit and save the report
        bandit -r . -f json -o "../bandit_results/$REPO/bandit_report_$commit.json"
        echo "Saved report for commit $commit"

    done < commits.txt

    # Return to the main branch
    git checkout main --quiet

    # Move back to the main directory
    cd ..
done

echo "Bandit analysis completed for all repositories!"



