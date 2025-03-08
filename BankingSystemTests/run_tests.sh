#!/bin/bash

# Set directories
INPUT_DIR="Input"
OUTPUT_DIR="Outputs"
EXPECTED_TRANSACTION_DIR="ExpectedTransaction"  # Contains .etf files
ACTUAL_OUTPUT_DIR="Outputs"  # Contains .atf files
FAILURES_FILE="test_failures.csv"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Create CSV Header for failures log
echo "Test Case, Expected Output, Actual Output, Difference" > "$FAILURES_FILE"

echo "Starting tests..."

# Run the program on each input file
for input_file in "$INPUT_DIR"/*.inp; do
    test_name=$(basename "$input_file" .inp)  # Extract test name without extension
    echo "\n🔄 Running test: $test_name"

    # Define output files
    TRANSACTION_FILE="$OUTPUT_DIR/$test_name.atf"
    TERMINAL_OUTPUT="$OUTPUT_DIR/$test_name.out"

    # Run the program and save outputs
    python3 TellerSystem.py current_account_file.txt "$TRANSACTION_FILE" < "$input_file" > "$TERMINAL_OUTPUT"
    echo " TellerSystem.py current_account_file.txt "$TRANSACTION_FILE" < "$input_file" > "$TERMINAL_OUTPUT""
    echo "✅ Test $test_name completed."
done

echo "All tests finished!"
echo "Validating test results..."

# Loop through all expected transaction files
for expected_file in "$EXPECTED_TRANSACTION_DIR"/*.etf; do
    test_name=$(basename "$expected_file" .etf)
    actual_file="$ACTUAL_OUTPUT_DIR/$test_name.atf"

    # Check if the actual transaction file exists
    if [ ! -f "$actual_file" ]; then
        echo "$test_name, No output generated, No output generated, MISSING FILE" >> "$FAILURES_FILE"
        echo "❌ Missing file: $actual_file"
        continue
    fi

    # Compare files
    diff_output=$(diff "$expected_file" "$actual_file")

    if [ "$diff_output" != "" ]; then
        echo "$test_name, See $expected_file, See $actual_file, Differences found" >> "$FAILURES_FILE"
        echo "❌ Test failed: $test_name (Transaction Output Mismatch)"
    else
        echo "✅ Test passed: $test_name (Transaction Logs Match)"
    fi
done

echo "Validation complete! Failures logged in $FAILURES_FILE"
