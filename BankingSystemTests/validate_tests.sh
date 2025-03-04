#!/bin/bash

# Set directories
EXPECTED_DIR="ExpectedOutput"
OUTPUT_DIR="Outputs"
FAILURES_FILE="test_failures.csv"

# Create CSV Header
echo "Test Case, Expected Output, Actual Output, Difference" > "$FAILURES_FILE"

echo "🔍 Validating test results..."

# Loop through each expected file
for expected_file in "$EXPECTED_DIR"/*.etf; do
    test_name=$(basename "$expected_file" .etf)
    actual_file="$OUTPUT_DIR/$test_name.bto"

    # Check if the actual file exists
    if [ ! -f "$actual_file" ]; then
        echo "$test_name, $expected_file, MISSING FILE, MISSING FILE" >> "$FAILURES_FILE"
        echo "❌ Missing file: $actual_file"
        continue
    fi

    # Compare expected and actual outputs
    if ! diff -q "$expected_file" "$actual_file" > /dev/null; then
        echo "$test_name, $expected_file, $actual_file, Differences found" >> "$FAILURES_FILE"
        echo "❌ Test failed: $test_name"
        diff "$expected_file" "$actual_file" >> "Outputs/${test_name}_diff.log"  # Save diff to a log file
    else
        echo "✅ Test passed: $test_name"
    fi
done

echo "✅ Validation complete. Failures logged in test_failures.csv"

