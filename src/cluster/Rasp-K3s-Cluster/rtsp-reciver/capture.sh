#!/bin/bash

# Infinite loop to run capture.py every 30 seconds
while true
do
    # Get the current working directory
    current_dir=$(pwd)

    # Run the capture.py script
    python3 "$current_dir/capture.py"

    # Sleep for 30 seconds
    sleep 30
done
