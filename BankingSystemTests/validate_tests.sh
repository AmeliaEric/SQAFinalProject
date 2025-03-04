#!/bin/bash

# Set directories
EXPECTED_DIR="ExpectedOutput"
ACTUAL_DIR="Outputs"
FAILURES_FILE="test_failures.csv"

# Create CSV Header
echo "Test Case, Expected Output, Actual Output, Difference" > "$FAILURES_FILE"

echo "Validating test results..."

# Loop through each expected file
for expected_file in "$EXPECTED_DIR"/*.etf; do
    test_name=$(basename "$expected_file" .etf)
    actual_file="$ACTUAL_DIR/$test_name.bto"

    if [ ! -f "$actual_file" ]; then
        echo "$test_name, No output generated, No output generated, MISSING FILE" >> "$FAILURES_FILE"
        echo "❌ Missing file: $actual_file"
        continue
    fi

    # Compare files
    diff_output=$(diff "$expected_file" "$actual_file")

    if [ "$diff_output" != "" ]; then
        echo "$test_name, See $expected_file, See $actual_file, Differences found" >> "$FAILURES_FILE"
        echo "❌ Test failed: $test_name"
    else
        echo "✅ Test passed: $test_name"
    fi
done

echo "Validation complete. Failures logged in test_failures.csv"
#!/bin/bash
EXPECTED_DIR="ExpectedOutput"
OUTPUT_DIR="Outputs"

for expected_file in "$EXPECTED_DIR"/*.etf; do
    test_name=$(basename "$expected_file" .etf)
    actual_file="$OUTPUT_DIR/$test_name.bto"

    echo "Checking test: $test_name"
    diff "$actual_file" "$expected_file"
done
echo "Validation complete!"
