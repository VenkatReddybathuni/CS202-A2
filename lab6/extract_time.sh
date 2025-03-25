#!/bin/bash

# Create a file to store results
output_file="parallel_results.csv"
echo "Workers,Threads,Mode,Tpar" > $output_file  # CSV Header

# Iterate over log files and extract execution time
for log in parallel_n*_t*_*.log; do
    workers=$(echo $log | sed -E 's/parallel_n(.*)_t.*/\1/')
    threads=$(echo $log | sed -E 's/parallel_n.*_t(.*)_.*/\1/')
    mode=$(echo $log | sed -E 's/parallel_n.*_t.*_(.*).log/\1/')

    # Extract last 3 execution times
    avg_time=$(grep "passed in" "$log" | tail -n3 | awk '{print $(NF-1)}' | sed 's/s//' | awk '{sum+=$1} END {print sum/3}')
    
    echo "$workers,$threads,$mode,$avg_time" >> $output_file
done

echo "Extraction completed. Data saved in parallel_results.csv."
