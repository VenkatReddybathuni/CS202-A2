export PYNGUIN_DANGER_AWARE=True
find algorithms -name "*.py" | sed 's|/|.|g' | sed 's|.py$||' | grep -v "init" | parallel -j4 "pynguin --project-path=. --module-name={} --output-path=generated_tests"

# Move all generated .py test files from subdirectories to generated_tests/
find generated_tests -type f -name "*.py" -exec mv {} generated_tests/ \;

# Remove any empty directories left behind
find generated_tests -type d -empty -delete


export PYNGUIN_DANGER_AWARE=True
grep -v "100%" coverage.txt | awk '{print $1}' | sed 's|/|.|g' | sed 's|.py$||' | grep -v "init" | parallel -j4 "pynguin --project-path=. --module-name={} --output-path=generated_tests"

# Move all generated .py test files from subdirectories to generated_tests/
find generated_tests -type f -name "*.py" -exec mv {} generated_tests/ \;

# Remove any empty directories left behind
find generated_tests -type d -empty -delete
```Use chat to tell me which framework you'd prefer.
