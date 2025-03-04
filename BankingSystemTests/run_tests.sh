#!/bin/bash

# Set directories
INPUT_DIR="Input"
OUTPUT_DIR="Outputs"  # Ensure only .out files are saved here

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Run the program on each input file
for input_file in "$INPUT_DIR"/*.inp; do
    test_name=$(basename "$input_file" .inp)  # Extract test name without extension
    echo "Running test: $test_name"

    # Run the program and save only the .out file
    python3 TellerSystem.py current_accounts_file.txt "/dev/null" < "$input_file" > "$OUTPUT_DIR/$test_name.out"

    echo "Test $test_name completed."
done

echo "All tests finished!"

