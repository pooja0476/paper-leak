# Member 3 - Machine Learning and Historical Data Analysis

## Project: PAPER-LEAK SENTINEL

### Responsibilities
- Prepare examination datasets.
- Clean and validate examination data.
- Calculate centre-wise performance metrics.
- Detect unusual examination patterns using Isolation Forest.
- Compare current and historical examination performance.
- Identify repeated unusual patterns.

## Input Datasets

1. data/historical_scores.csv
2. data/current_scores.csv

### Dataset Columns
- student_id
- centre_id
- exam_id
- exam_date
- score
- max_score

## Python Files

1. src/data_cleaning.py
2. src/feature_engineering.py
3. src/anomaly_detection.py
4. src/historical_analysis.py

## Output Files for Dashboard

| File | Purpose |
|---|---|
| centre_metrics.csv | Centre-wise performance |
| anomaly_results.csv | Anomaly scores and flags |
| historical_comparison.csv | Historical score comparison |
| repeated_patterns.csv | Repeated unusual pattern analysis |

## Machine Learning Model

Isolation Forest is used to identify unusual centre-wise examination performance.

- 1 = Normal
- -1 = Anomaly

Anomaly results are intended for human review and do not prove examination malpractice.

## Sample Finding

Centre C004 showed an unusually high average score of 96.67 compared with its historical average of 76.00.

Its score increased by 20.67 marks.

## Note

The datasets contain fictional sample examination records for project testing.