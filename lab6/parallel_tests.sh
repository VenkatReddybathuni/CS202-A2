#!/bin/bash

# Define the parameter combinations
workers=("1" "auto")
threads=("1" "auto")
modes=("load" "no")

# Loop through each combination
for n in "${workers[@]}"; do
    for t in "${threads[@]}"; do
        for mode in "${modes[@]}"; do
            # Define log filename based on combination
            log_file="parallel_n${n}_t${t}_${mode}.log"
            
            echo "Running tests with -n $n --parallel-threads=$t --dist=$mode"
            echo "Logs will be saved in: $log_file"

            # Run the test suite 3 times for the given combination
            for i in {1..3}; do
                echo "===== Run $i =====" >> "$log_file"
                pytest -n "$n" --parallel-threads="$t" --dist="$mode" tests/ | tee -a "$log_file"
                echo -e "\n" >> "$log_file"
            done
        done
    done
done

echo "All test combinations completed."
